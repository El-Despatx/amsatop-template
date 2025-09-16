import os
import sys
import shutil
import time
from pathlib import Path

# Files in /proc/<pid>/ that we want
KEEP_FILES = {
    "stat",
    "status",
    "exe",
    "auxv",
}

# Names of files to explicitly skip (memory / mapping etc.)
SKIP_FILES = {
    "pagemap",
    "mem",
    "maps",
    "smaps",
    "stack",
    "clear_refs",
    "kcore",
    "io",  # optionally skip io
    # etc, add as needed
}

def get_all_threads(pid):
    task_dir = Path("/proc") / pid / "task"
    threads = []
    try:
        for entry in task_dir.iterdir():
            if entry.name.isdigit():
                threads.append(entry.name)
    except Exception as e:
        print(f"[WARN] Could not list tasks for PID {pid}: {e}", file=sys.stderr)
    return threads

def get_child_pids(pid):
    children_path = Path("/proc") / pid / "task" / pid / "children"
    try:
        text = children_path.read_text()
        children = text.split()
        return children
    except Exception as e:
        # Might not exist or unreadable
        return []

def get_process_tree(start_pids):
    """
    Return set of all PIDs & thread‐IDs to copy,
    for the given starting PIDs, including children processes recursively,
    and all threads of each process.
    """
    result = set()
    queue = list(start_pids)
    while queue:
        pid = queue.pop(0)
        if pid in result:
            continue
        result.add(pid)
        # Add children
        child_pids = get_child_pids(pid)
        for c in child_pids:
            if c not in result:
                queue.append(c)
        # Add threads (TIDs)
        threads = get_all_threads(pid)
        for t in threads:
            if t not in result:
                result.add(t)
    return result

def copy_file(src: Path, dest: Path):
    try:
        if src.is_symlink():
            # replicate symlink
            target = os.readlink(src)
            dest.symlink_to(target)
        elif src.is_file():
            # Copy small files entirely
            shutil.copy2(src, dest)
        else:
            # Other types (device, etc.), skip or replicate if needed
            print(f"[INFO] Skipping special file {src}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] Error copying file {src} -> {dest}: {e}", file=sys.stderr)

def copy_tasks_dir(pid: str, target_root: Path):
    """
    Copy /proc/<pid>/task/ and relevant files under each task/<tid>/ from KEEP_FILES
    """
    task_base = Path("/proc") / pid / "task"
    if not task_base.exists():
        print(f"[INFO] No task dir for PID {pid}", file=sys.stderr)
        return
    for tid_entry in task_base.iterdir():
        if not tid_entry.name.isdigit():
            continue
        tid = tid_entry.name
        dest_tid_dir = target_root / pid / "task" / tid
        try:
            dest_tid_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"[WARN] Could not create dest dir {dest_tid_dir}: {e}", file=sys.stderr)
            continue
        # For each tid, copy the KEEP_FILES if present
        for fname in KEEP_FILES:
            src_f = tid_entry / fname
            if src_f.exists():
                dest_f = dest_tid_dir / fname
                print(f"[INFO] Copying task file {src_f} -> {dest_f}", file=sys.stderr)
                copy_file(src_f, dest_f)
        # Possibly also status or stat in the thread directory? Only if needed.

def copy_proc_entries(pid_or_tid: str, target_root: Path):
    """
    Copy files stat, status, exe, auxv for /proc/<pid_or_tid>
    Also copy its tasks directory (threads).
    Avoid copying memory / pagemap etc.
    """
    src_root = Path("/proc") / pid_or_tid
    if not src_root.exists():
        print(f"[INFO] /proc/{pid_or_tid} not found; skipping", file=sys.stderr)
        return

    # prepare dest dir
    dest_root = target_root / pid_or_tid
    try:
        dest_root.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[WARN] Could not create destination {dest_root}: {e}", file=sys.stderr)
        return

    # Copy the KEEP_FILES at this level
    for fname in KEEP_FILES:
        src_f = src_root / fname
        if src_f.exists():
            dest_f = dest_root / fname
            print(f"[INFO] Copying {src_f} -> {dest_f}", file=sys.stderr)
            copy_file(src_f, dest_f)
        else:
            # maybe exe is a symlink or special
            # treat exe specially: if it's a symlink
            if fname == "exe":
                try:
                    # symlink handling
                    if (src_root / fname).is_symlink():
                        dest_link = dest_root / fname
                        target = os.readlink(src_root / fname)
                        dest_link.symlink_to(target)
                        print(f"[INFO] Copying symlink exe {src_root / fname} -> {dest_link}", file=sys.stderr)
                except Exception as e:
                    print(f"[WARN] Cannot copy exe link for {pid_or_tid}: {e}", file=sys.stderr)

    # Copy tasks (threads) for this pid
    copy_tasks_dir(pid_or_tid, target_root)

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <output_root_dir> <pid1> [pid2 pid3 ...]", file=sys.stderr)
        sys.exit(1)

    target_root = Path(sys.argv[1])
    start_pids = sys.argv[2:]
    for pid in start_pids:
        if not pid.isdigit():
            print(f"PID {pid} is not numeric; exiting", file=sys.stderr)
            sys.exit(1)

    try:
        target_root.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[ERROR] Cannot create output root {target_root}: {e}", file=sys.stderr)
        sys.exit(1)

    all_ids = get_process_tree(start_pids)
    print(f"[INFO] Will copy these IDs (PIDs + threads): {sorted(all_ids, key=lambda x: int(x))}", file=sys.stderr)

    for pid_or_tid in sorted(all_ids, key=lambda x: int(x)):
        print(f"[INFO] Processing /proc/{pid_or_tid}", file=sys.stderr)
        copy_proc_entries(pid_or_tid, target_root)
        # so we can see progress
        time.sleep(0.05)
    print("[INFO] Done.")

if __name__ == "__main__":
    main()

