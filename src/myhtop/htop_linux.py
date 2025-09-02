from typing import List

from amsatop import Htop, Process


class HtopLinux(Htop):
    def __init__(self):
        super(HtopLinux, self).__init__()

    def get_processes(self) -> List[Process]:
        return []

    def get_priorities(self) -> List[Process]:
        return []

    def get_hup(self) -> List[Process]:
        return []
