from typing import List

from amsatop import Htop, Process

# TODO: Delete when needed
from myhtop.procfs.teachers_solution import AmsatopTeachersSolution


class Amsatop(Htop):
    def __init__(self):
        super().__init__()

    def get_processes(self) -> List[Process]:
        raise NotImplementedError("Prac-2.1 implementation needed")

    def get_priorities(self) -> List[Process]:
        raise NotImplementedError("Prac-2.2 implementation needed")

    def get_hup(self) -> List[Process]:
        raise NotImplementedError("Prac-2.3 implementation needed")


Amsatop = AmsatopTeachersSolution
