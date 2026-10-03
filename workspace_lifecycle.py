"""Portable single-profile service lifecycle; never schedules scraper checks."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import urllib.request


class ProfileLock:
    def __init__(self, path: Path, timeout=45):
        self.path, self.timeout, self.file = path, timeout, None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.is_symlink():
            raise ValueError("Profile locks cannot be symbolic links")
        self.file = self.path.open("a+b")
        if self.path.stat().st_size == 0:
            self.file.write(b"0"); self.file.flush()
        until = time.monotonic() + self.timeout
        while True:
            try:
                if os.name == "nt":
                    import msvcrt
                    self.file.seek(0); msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.monotonic() >= until:
                    self.file.close(); self.file = None
                    raise ValueError("Another service owns this profile; inspect it instead of starting a duplicate")
                time.sleep(.1)

    def __exit__(self, *args):
        if self.file:
            if os.name == "nt":
                import msvcrt
                self.file.seek(0); msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
            self.file.close()

    def record(self, value):
        # Windows byte locks deny reads by another process. Keep inspectable
        # ownership metadata outside the locked file and replace it atomically.
        owner = self.path.with_suffix(".owner.json")
        pending = owner.with_suffix(".pending.json")
        pending.write_text(json.dumps(value))
        os.replace(pending, owner)


def instance_id(root: Path, release: str) -> str:
    return hashlib.sha256((str(root.resolve()) + "\n" + release).encode()).hexdigest()[:32]


def health(port: int):
    # Loopback lifecycle probes must never inherit an egress proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(f"http://127.0.0.1:{port}/api/v1/health", timeout=1) as response:
            value = json.loads(response.read(16_000))
        return value if value.get("service") == "jobhound" else {"foreign_service": True}
    except Exception:
        import socket
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=.3):
                return {"foreign_service": True}
        except OSError:
            return None


def touch(root: Path):
    (root / "last-used").touch()


def ensure_service(root, release, port, command, *, env, cwd, timeout=45):
    expected = instance_id(root, release)
    with ProfileLock(root / "startup.lock", timeout=timeout):
        current = health(port)
        if current:
            if current.get("instance_id") != expected or current.get("capabilities", {}).get("profile") != env.get("JOBHOUND_PROFILE", "desktop"):
                raise ValueError("Port belongs to another profile or release. Stop that service explicitly or choose a different port; no process was killed.")
            touch(root)
            return {"status": "already_running", "instance_id": expected}
        root.mkdir(parents=True, exist_ok=True)
        touch(root)
        options = {"start_new_session": True} if os.name != "nt" else {
            "creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP}
        with (root / "service.log").open("ab") as output:
            child = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                     stdout=output, stderr=output, **options)
        until = time.monotonic() + timeout
        while time.monotonic() < until:
            current = health(port)
            if current and current.get("instance_id") == expected:
                return {"status": "started", "instance_id": expected}
            if child.poll() is not None:
                raise ValueError("Service could not start; inspect this profile's service.log. Existing data was retained.")
            time.sleep(.2)
        raise ValueError("Service startup timed out; inspect status/logs before retrying. Existing data was retained.")


def run_service(root, release, port, command, *, env, cwd, idle_seconds=None):
    with ProfileLock(root / "service.lock", timeout=0) as lock:
        if health(port):
            raise ValueError("A listener already owns this port; no duplicate service was started")
        lock.record({"pid": os.getpid(), "instance_id": instance_id(root, release), "port": port})
        request_path = root / "stop-request.json"
        request_path.unlink(missing_ok=True)
        child = subprocess.Popen(command, cwd=cwd, env=env)
        def stop(signum, frame):
            if child.poll() is None:
                child.terminate()
        previous = signal.signal(signal.SIGTERM, stop)
        try:
            while child.poll() is None:
                if request_path.exists():
                    request = json.loads(request_path.read_text())
                    if request == {"pid": os.getpid(), "instance_id": instance_id(root, release)}:
                        stop(None, None)
                    request_path.unlink(missing_ok=True)
                if idle_seconds is not None and (root / "last-used").exists():
                    idle = time.time() - (root / "last-used").stat().st_mtime
                    if idle >= idle_seconds:
                        current = health(port)
                        if current and current.get("instance_id") == instance_id(root, release) and not current.get("busy", True):
                            stop(None, None)
                time.sleep(.5)
            return child.returncode
        except KeyboardInterrupt:
            stop(None, None)
            return child.wait(timeout=30)
        finally:
            signal.signal(signal.SIGTERM, previous)
            if child.poll() is None:
                child.terminate(); child.wait(timeout=30)


def stop_service(root, release, port):
    current = health(port)
    if not current:
        return {"ok": True, "status": "already_stopped"}
    if current.get("busy"):
        raise ValueError("JobHound has active work; wait for its terminal receipt before stopping the service")
    expected = instance_id(root, release)
    record = json.loads((root / "service.owner.json").read_text())
    if current.get("instance_id") != expected or record.get("instance_id") != expected or record.get("pid") != current.get("owner_pid"):
        raise ValueError("Service identity/PID does not match this profile; no process was signalled")
    # Windows SIGTERM can terminate a supervisor before its finally block.
    # An identity-bound file request lets the owning supervisor stop its child
    # through its owning supervisor without signalling a reused PID.
    pending = root / "stop-request.pending.json"
    pending.write_text(json.dumps({"pid": record["pid"], "instance_id": expected}))
    os.replace(pending, root / "stop-request.json")
    until = time.monotonic() + 30
    while time.monotonic() < until:
        if health(port) is None:
            return {"ok": True, "status": "stopped"}
        time.sleep(.2)
    raise ValueError("Service did not stop yet; inspect it before updating. No force-kill was performed.")
