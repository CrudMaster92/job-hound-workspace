"""Disposable live backend/UI/agent smoke check; no external scraping or private data."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from jobhound import layout, manifest

HERE = Path(__file__).resolve().parent


def main():
    value = manifest()
    root, _, _, _ = layout(HERE / ".jobhound", value["release"])
    if (root / "data" / "jobhound.sqlite3").exists():
        raise RuntimeError("This smoke check requires a fresh test profile")
    service = subprocess.Popen([sys.executable, "jobhound.py", "serve"], cwd=HERE)
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
        tools = subprocess.run([sys.executable, "jobhound.py", "tools"], cwd=HERE, check=True, capture_output=True, text=True)
        discovered = json.loads(tools.stdout)
        assert discovered["ok"] and discovered["tool_count"] > 0
        status = subprocess.run([sys.executable, "jobhound.py", "status"], cwd=HERE, check=True, capture_output=True, text=True)
        assert json.loads(status.stdout)["ok"]
        print(json.dumps({"ok": True, "checks": ["live_backend", "bundled_ui", "typed_tools", "live_status"],
                          "tool_count": discovered["tool_count"], "release": value["release"]}))
    finally:
        # Stop the child backend as well as its launcher, on this disposable run.
        if service.poll() is None:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/PID", str(service.pid), "/T", "/F"], check=False, capture_output=True)
            else:
                # The launcher forwards SIGTERM below.
                service.terminate()
            service.wait(timeout=20)


if __name__ == "__main__":
    main()

