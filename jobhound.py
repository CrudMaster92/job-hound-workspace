#!/usr/bin/env python3
"""Install a pinned JobHound release and operate it through shared contracts."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit
import urllib.request
import venv

HERE = Path(__file__).resolve().parent
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
MAX_EXPANDED_BYTES = 250 * 1024 * 1024


def manifest():
    value = json.loads((HERE / "release.json").read_text(encoding="utf-8"))
    if value.get("format") != "jobhound-agent-workspace" or value.get("version") != 1:
        raise ValueError("Unsupported release manifest")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}", value["release"]):
        raise ValueError("Invalid release identifier")
    if not re.fullmatch(r"[a-f0-9]{64}", value["sha256"]):
        raise ValueError("Invalid release checksum")
    url = urlsplit(value["archive_url"])
    if url.scheme != "https" or url.hostname != "github.com" or url.username or url.password:
        raise ValueError("Release archive must use credential-free GitHub HTTPS")
    if not url.path.startswith("/CrudMaster92/job-hound-workspace/releases/download/"):
        raise ValueError("Release archive must belong to this repository")
    return value


def layout(home, release):
    root = Path(home).expanduser().resolve()
    runtime = root / "releases" / release
    python = runtime / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return root, runtime, runtime / "app", python


def extract_checked(archive, destination):
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        if sum(item.size for item in members) > MAX_EXPANDED_BYTES or len(members) > 10000:
            raise ValueError("Release exceeds extraction limits")
        for item in members:
            parts = Path(item.name).parts
            target = (destination / item.name).resolve()
            if not parts or parts[0] != "app" or "\\" in item.name or not target.is_relative_to(destination.resolve()):
                raise ValueError("Unsafe release path")
            if not (item.isfile() or item.isdir()):
                raise ValueError("Release links and special files are forbidden")
        for item in members:
            target = destination / item.name
            if item.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with bundle.extractfile(item) as source, target.open("xb") as output:
                    while chunk := source.read(65536):
                        output.write(chunk)


def install(value, root, runtime, app, python):
    ready = runtime / "ready.json"
    if ready.exists():
        previous = json.loads(ready.read_text())
        if previous.get("sha256") != value["sha256"]:
            raise ValueError("Installed release checksum differs; use a new release identifier")
        return {"ok": True, "status": "already_installed", "release": value["release"], "home": str(root)}
    if app.exists():
        # A dependency installation may have stopped after verified extraction.
        verified = runtime / "verified.json"
        if not verified.exists() or json.loads(verified.read_text()).get("sha256") != value["sha256"]:
            raise ValueError("Unverified installation exists; inspect it and choose a fresh --home")
    else:
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="jobhound-", dir=root) as temporary:
            temporary = Path(temporary)
            archive = temporary / "release.tar.gz"
            request = urllib.request.Request(value["archive_url"], headers={"User-Agent": "JobHound-workspace-installer"})
            with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
                if urlsplit(response.geturl()).hostname not in {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"}:
                    raise ValueError("Unexpected release download origin")
                count = 0
                digest = hashlib.sha256()
                while chunk := response.read(65536):
                    count += len(chunk)
                    if count > MAX_ARCHIVE_BYTES:
                        raise ValueError("Release archive exceeds download limit")
                    digest.update(chunk)
                    output.write(chunk)
            if digest.hexdigest() != value["sha256"]:
                raise ValueError("Release checksum mismatch")
            unpacked = temporary / "unpacked"
            unpacked.mkdir()
            extract_checked(archive, unpacked)
            runtime.mkdir(parents=True, exist_ok=True)
            (unpacked / "app").rename(app)
            (runtime / "verified.json").write_text(json.dumps({"sha256": value["sha256"]}))
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(runtime / "venv")
    subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check", "-c", str(app / "runtime-constraints.txt"), str(app) + "[browser]"],
                   check=True, stdout=sys.stderr, stderr=sys.stderr)
    ready.write_text(json.dumps({"sha256": value["sha256"], "release": value["release"]}))
    return {"ok": True, "status": "installed", "release": value["release"], "home": str(root)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(HERE / ".jobhound"), help="Choose a durable third-party workspace location.")
    parser.add_argument("--port", type=int, default=4176, help="Loopback port; 4176 keeps the test instance separate.")
    parser.add_argument("--network-mode", choices=("direct", "environment"),
                        default=os.getenv("JOBHOUND_EXTERNAL_NETWORK_MODE", "direct"),
                        help="Opt in to the workspace proxy/CA environment for external job/feed requests.")
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("install", "doctor", "serve", "status", "tools"):
        commands.add_parser(name)
    call = commands.add_parser("call")
    call.add_argument("tool")
    call.add_argument("--arguments", default="{}")
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 11):
            raise ValueError("Python 3.11 or later is required")
        if not 1024 <= args.port <= 65535:
            raise ValueError("port must be between 1024 and 65535")
        if args.network_mode not in {"direct", "environment"}:
            raise ValueError("network-mode must be direct or environment")
        value = manifest()
        root, runtime, app, python = layout(args.home, value["release"])
        ready = (runtime / "ready.json").exists() and python.exists()
        api_url = f"http://127.0.0.1:{args.port}/api/v1"
        if args.action == "install":
            result = install(value, root, runtime, app, python)
        elif args.action == "doctor":
            result = {"ok": True, "installed": ready, "release": value["release"], "home": str(root),
                      "data_path": str(root / "data"), "api_url": api_url,
                      "python": sys.version.split()[0], "platform": sys.platform,
                      "external_network_mode": args.network_mode,
                      "node_available": shutil.which("node") is not None,
                      "public_board_query_engine_present": all((app / "web/src/shared/job-board-ui" / name).is_file() for name in ("query.mjs", "query-runner.mjs")),
                      "preset_catalog_snapshot_present": (app / "server/preset_snapshot/snapshot.json").is_file(),
                      "native_audio_capture": sys.platform == "win32",
                      "proxy_environment_present": any(os.getenv(key) for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy")),
                      "private_artifact_mount": "unverified", "restart_durability": "unverified",
                      "background_service_uptime": "unverified",
                      "mcp": {"command": str(python), "args": ["-m", "server.mcp_server"], "cwd": str(app),
                              "env": {"JOBHOUND_API_URL": api_url}}}
        else:
            if not ready:
                raise ValueError("Run install first; use the same --home for every command")
            env = {**os.environ, "JOBHOUND_API_URL": api_url, "JOBHOUND_DB_PATH": str(root / "data" / "jobhound.sqlite3"), "JOBHOUND_LAN": "0", "JOBHOUND_EXTERNAL_NETWORK_MODE": args.network_mode}
            if args.action == "serve":
                command = [str(python), "-m", "uvicorn", "server.app:app", "--host", "127.0.0.1", "--port", str(args.port)]
            else:
                command = [str(python), "-m", "server.workspace_cli", "--api-url", api_url, args.action]
                if args.action == "call":
                    command += [args.tool, "--arguments", args.arguments]
            child = subprocess.Popen(command, cwd=app, env=env)
            def stop_child(signum, frame):
                if child.poll() is None:
                    child.terminate()
            signal.signal(signal.SIGTERM, stop_child)
            try:
                return child.wait()
            except KeyboardInterrupt:
                stop_child(None, None)
                return child.wait(timeout=20)
    except Exception as exc:
        result = {"ok": False, "error": {"code": "workspace_setup_failed", "message": str(exc)},
                  "next_step": "Inspect the error. Keep the same test profile; do not retry monitor creation blindly."}
    print(json.dumps(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

