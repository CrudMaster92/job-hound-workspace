"""Disposable live backend/UI/agent smoke check; no external scraping or private data."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from jobhound import layout, manifest, extract_checked, MAX_ARCHIVE_BYTES

HERE = Path(__file__).resolve().parent


def stage_preview_archive(test_home, value, archive):
    """CI stages the exact checked-in asset; installation still uses the launcher."""
    archive = Path(archive)
    if archive.is_dir():
        archive = archive / f"jobhound-{value['release']}.tar.gz"
    if archive.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError("Preview archive exceeds installation limit")
    digest = hashlib.sha256()
    with archive.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
    if digest.hexdigest() != value["sha256"]:
        raise ValueError("Preview archive checksum differs from release manifest")
    _, runtime, _, _ = layout(test_home, value["release"])
    if runtime.exists():
        raise ValueError("Preview staging requires a fresh runtime directory")
    runtime.mkdir(parents=True)
    extract_checked(archive, runtime)
    (runtime / "verified.json").write_text(json.dumps({"sha256": value["sha256"]}))


def main():
    value = manifest()
    test_home = Path(os.getenv("JOBHOUND_SMOKE_HOME", str(Path.home() / ".local/share/jobhound-smoke")))
    root, _, _, _ = layout(test_home, value["release"])
    common = [sys.executable, str(HERE / "jobhound.py"), "--home", str(test_home)]
    if (root / "data" / "jobhound.sqlite3").exists():
        raise RuntimeError("This smoke check requires a fresh test profile")
    if os.getenv("JOBHOUND_SMOKE_ARCHIVE"):
        stage_preview_archive(test_home, value, os.environ["JOBHOUND_SMOKE_ARCHIVE"])
        subprocess.run(common + ["install"], cwd=HERE, check=True)
    if os.getenv("JOBHOUND_SMOKE_PRESET_SNAPSHOT") == "1":
        _, _, app, python = layout(test_home, value["release"])
        probe = subprocess.run([str(python), str(HERE / "preset_snapshot_probe.py")], cwd=app, check=True)
    service = subprocess.Popen(common + ["serve"], cwd=HERE)
    try:
        for _ in range(60):
            if service.poll() is not None:
                raise RuntimeError("Service stopped before it became ready")
            try:
                with urllib.request.urlopen("http://127.0.0.1:4176/api/v1/health", timeout=2) as response:
                    assert response.status == 200
                break
            except OSError:
                time.sleep(1)
        else:
            raise RuntimeError("Backend readiness timed out")
        with urllib.request.urlopen("http://127.0.0.1:4176", timeout=10) as response:
            assert b"<html" in response.read().lower()
        tools = subprocess.run(common + ["tools"], cwd=HERE, check=True, capture_output=True, text=True)
        discovered = json.loads(tools.stdout)
        assert discovered["ok"] and discovered["tool_count"] == 111
        status = subprocess.run(common + ["status"], cwd=HERE, check=True, capture_output=True, text=True)
        assert json.loads(status.stdout)["ok"]
        checks = ["live_backend", "bundled_ui", "typed_tools", "live_status"]
        if os.getenv("JOBHOUND_SMOKE_PUBLIC_BOARD") == "1":
            with urllib.request.urlopen("http://127.0.0.1:4176/api/v1/public-board/status", timeout=300) as response:
                board = json.load(response)
            assert board["state"] in {"ready", "stale"}, board.get("error")
            with urllib.request.urlopen("http://127.0.0.1:4176/api/v1/public-board/jobs?limit=3", timeout=120) as response:
                page = json.load(response)
            assert page["total"] > 0 and 0 < len(page["items"]) <= 3
            assert all(item["id"] and item["source_url"] for item in page["items"])
            called = subprocess.run(common + ["call", "search_public_jobs", "--arguments", '{"query":{"limit":3}}'], cwd=HERE, check=True, capture_output=True, text=True)
            envelope = json.loads(called.stdout)
            assert envelope["ok"] and not envelope["result"]["isError"]
            result = envelope["result"]
            agent_page = result.get("structuredContent") or json.loads(result["content"][0]["text"])
            assert [item["id"] for item in agent_page["items"]] == [item["id"] for item in page["items"]]
            checks += ["live_public_feed", "packaged_shared_query_engine", "human_agent_public_job_ids"]
        print(json.dumps({"ok": True, "checks": checks,
                          "tool_count": discovered["tool_count"], "release": value["release"]}))
    finally:
        subprocess.run(common + ["stop"], cwd=HERE, check=True, capture_output=True)
        service.wait(timeout=30)


if __name__ == "__main__":
    main()
