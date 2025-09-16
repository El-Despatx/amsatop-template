from test.conftest import with_proc_fs
from amsatop import Process, TaskType

from myhtop.amsatop_solution import Amsatop

# First, test the 2.1 but with nohup!

@with_proc_fs(proc_fs_path="test/prac_2_1/empty")
def test_hup_empty_proc_fs(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0


@with_proc_fs(proc_fs_path="test/prac_2_1/one")
def test_hup_two_processes_two_threads(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0


@with_proc_fs(proc_fs_path="test/prac_2_1/two")
def test_hup_one_kthread_one_process_and_one_thread(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert set(processes) == {Process(pid=2, command='kthreadd', type=TaskType.KTHREAD, priority=20)}


@with_proc_fs(proc_fs_path="test/prac_2_1/three")
def test_hup_one_thread_has_just_died(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0

# Then, test the 2.2 but now with nohup!

@with_proc_fs(proc_fs_path="test/prac_2_2/four")
def test_hup_one_process_without_nice_other_with_nice_positive(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0


@with_proc_fs(proc_fs_path="test/prac_2_2/five")
def test_hup_one_process_without_nice_other_with_nice_negative(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0

@with_proc_fs(proc_fs_path="test/prac_2_2/six")
def test_hup_one_process_without_nice_one_thread_with_nice(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert len(processes) == 0

# Finally, really test the nohup filter

@with_proc_fs(proc_fs_path="test/prac_2_3/seven")
def test_hup_one_nothing_one_ignores_one_handles(amsatop: Amsatop):
    processes = amsatop.get_hup()
    assert set(processes) == {Process(pid=30601, command='python3', type=TaskType.PROCESS, priority=20)}
