from amsatop import Process, TaskType

from myhtop.amsatop_solution import Amsatop
from test.conftest import with_proc_fs


@with_proc_fs(proc_fs_path="test/prac_2_1/empty")
def test_empty_proc_fs(amsatop: Amsatop):
    processes = amsatop.get_processes()
    assert len(processes) == 0


@with_proc_fs(proc_fs_path="test/prac_2_1/one")
def test_two_processes_two_threads(amsatop: Amsatop):
    processes = amsatop.get_processes()
    assert set(processes) == {Process(pid=17571, command='python3', type=TaskType.PROCESS, priority=None),
                              Process(pid=17573, command='python3', type=TaskType.PROCESS, priority=None),
                              Process(pid=17574, command='python3', type=TaskType.THREAD, priority=None),
                              Process(pid=17575, command='python3', type=TaskType.THREAD, priority=None)}


@with_proc_fs(proc_fs_path="test/prac_2_1/two")
def test_one_kthread_one_process_and_one_thread(amsatop: Amsatop):
    processes = amsatop.get_processes()
    assert set(processes) == {Process(pid=2, command='kthreadd', type=TaskType.KTHREAD, priority=None),
                              Process(pid=66665, command='python3', type=TaskType.PROCESS, priority=None),
                              Process(pid=66667, command='python3', type=TaskType.THREAD, priority=None),}
