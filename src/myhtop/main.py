from amsatop import run_ui

from myhtop.amsatop_solution import Amsatop


def main():
    # NOTE: You can change it to htop=None if you don't have the solution implemented
    # and you want to see a "fake" version of amsatop running
    # htop = Amsatop()
    htop = Amsatop()
    run_ui(htop=htop, refresh=2)


if __name__ == "__main__":
    main()
