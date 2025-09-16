"""
This file sets up a "fake" /proc filesystem, mimicking some of the special behavior normally handled by the Linux kernel.

Note to students:
You probably shouldn’t read this. Seriously, it doesn't contain
any part of the actual solution, but it will leave you with more questions than answers.

It works using a FUSE (Filesystem in Userspace) implementation (some advanced Linux wizardry that lets us build filesystems without touching kernel code).
"""

import functools
import json
import os
import time
import uuid
from multiprocessing import Process

import pytest
from fuse import Operations, FUSE

from myhtop.amsatop_solution import Amsatop


@pytest.fixture
def amsatop(request, tmp_path):
    proc_fs_path = getattr(request.function, "_proc_fs_path", None)
    if proc_fs_path is None:
        pytest.skip("Test is not decorated with with_amsatop")
    mountpoint = tmp_path / uuid.uuid4().hex
    os.mkdir(str(mountpoint))
    process = use_proc_fs(path=proc_fs_path, mountpoint=str(mountpoint))
    amsatop = Amsatop()
    amsatop.proc_folder = str(mountpoint)
    yield amsatop
    kill_proc_fs(process, str(mountpoint))
    os.rmdir(str(mountpoint))


def with_proc_fs(proc_fs_path: str):
    def decorator(fn):
        @pytest.mark.usefixtures("amsatop")
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper._proc_fs_path = proc_fs_path
        return wrapper

    return decorator


class ProcFileSystemTest(Operations):
    def __init__(self, root):
        self.root = root
        self.proc_json_path = os.path.join(self.root, "proc.json")
        self.allowed_pids = self._load_proc_json()

    def _load_proc_json(self):
        try:
            with open(self.proc_json_path, "r") as f:
                data = json.load(f)
                processes = data.get("processes", [])
                kthreads = data.get("kthreads", [])
                # Convert all to strings since directory names are strings
                return set(str(pid) for pid in processes + kthreads)
        except Exception as e:
            print(f"Error loading proc.json: {e}")
            return set()

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        entries = [".", ".."]

        if path == "/":
            try:
                all_entries = os.listdir(full_path)
            except Exception as e:
                print(f"Error reading directory {full_path}: {e}")
                all_entries = []

            # Only show allowed entries (from processes + kthreads)
            filtered = [
                e
                for e in all_entries
                if e in self.allowed_pids and os.path.isdir(os.path.join(full_path, e))
            ]
            entries.extend(filtered)
        else:
            # Non-root paths: show real directory content
            if os.path.isdir(full_path):
                entries.extend(os.listdir(full_path))

        for entry in entries:
            yield entry

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict(
            (key, getattr(st, key))
            for key in (
                "st_atime",
                "st_ctime",
                "st_gid",
                "st_mode",
                "st_mtime",
                "st_nlink",
                "st_size",
                "st_uid",
            )
        )

    def readlink(self, path):
        full_path = self._full_path(path)
        target = os.readlink(full_path)
        return target

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def read(self, path, size, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, size)

    def release(self, path, fh):
        return os.close(fh)


def __fuse_mount_procfs(path: str, mountpoint: str):
    FUSE(ProcFileSystemTest(path), mountpoint, foreground=True, ro=True)


def use_proc_fs(path: str, mountpoint: str | None = None):
    mountpoint = mountpoint if mountpoint is not None else path
    p = Process(target=__fuse_mount_procfs, args=(path, mountpoint))
    p.start()
    # Very dirty hack to assert that the FUSE filesystem is mounted...
    time.sleep(1)
    os.environ["PROC_FS"] = mountpoint
    return p


def kill_proc_fs(fuse_process: Process, mountpoint: str):
    fuse_process.terminate()
    fuse_process.join(timeout=3)
