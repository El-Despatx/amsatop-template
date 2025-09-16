from amsatop import run_ui

from myhtop.amsatop_solution import Amsatop


def main():
    """
    If you haven’t implemented the solution yet and want to see a simulated version of amsatop running
    on your computer, you can modify the following line:
        htop = Amsatop()
    to:
        htop = None

    This will display a "fake" version for testing purposes.
    Additionally, you can adjust the refresh interval to control
    how often the process list updates. If you'd prefer to view a static snapshot of the current processes,
    we recommend setting the refresh value to 120 seconds.
    """
    htop = Amsatop()
    run_ui(htop=htop, refresh=2)


if __name__ == "__main__":
    main()
