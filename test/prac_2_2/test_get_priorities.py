from test.conftest import with_proc_fs
from amsatop import Process, TaskType

from myhtop.amsatop_solution import Amsatop


# First, test the 2.1 but with priorities!

@with_proc_fs(proc_fs_path="test/prac_2_1/empty")
def test_prio_empty_proc_fs(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert len(processes) == 0


@with_proc_fs(proc_fs_path="test/prac_2_1/one")
def test_prio_two_processes_two_threads(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=17571, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=17573, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=17574, command='python3', type=TaskType.THREAD, priority=20),
                              Process(pid=17575, command='python3', type=TaskType.THREAD, priority=20)}


@with_proc_fs(proc_fs_path="test/prac_2_1/two")
def test_prio_one_kthread_one_process_and_one_thread(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=2, command='kthreadd', type=TaskType.KTHREAD, priority=20),
                              Process(pid=66665, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=66667, command='python3', type=TaskType.THREAD, priority=20), }


@with_proc_fs(proc_fs_path="test/prac_2_1/three")
def test_prio_one_thread_has_just_died(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=17571, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=17573, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=17575, command='python3', type=TaskType.THREAD, priority=20)}

# Now, have some fun with priorities!

@with_proc_fs(proc_fs_path="test/prac_2_2/four")
def test_prio_one_process_without_nice_other_with_nice_positive(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=17862, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=17864, command='python3', type=TaskType.PROCESS, priority=39)}


@with_proc_fs(proc_fs_path="test/prac_2_2/five")
def test_prio_one_process_without_nice_other_with_nice_negative(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=20846, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=20847, command='python3', type=TaskType.PROCESS, priority=10)}

@with_proc_fs(proc_fs_path="test/prac_2_2/six")
def test_prio_one_process_without_nice_one_thread_with_nice(amsatop: Amsatop):
    processes = amsatop.get_priorities()
    assert set(processes) == {Process(pid=24171, command='python3', type=TaskType.PROCESS, priority=20),
                              Process(pid=24172, command='python3', type=TaskType.THREAD, priority=10)}
