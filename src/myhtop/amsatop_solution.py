from typing import List

from amsatop import Htop, Process

from myhtop.procfs.proc_fs import ProcFS


class Amsatop(Htop):
    def __init__(self):
        super().__init__()
        self.procfs = ProcFS(proc_path=self.proc_folder)

    def get_processes(self) -> List[Process]:
        return self.procfs.processes

    def get_priorities(self) -> List[Process]:
        return self.procfs.priorities

    def get_hup(self) -> List[Process]:
        return self.procfs.nohup
