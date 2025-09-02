from amsatop import run_ui

from myhtop.htop_linux import HtopLinux


def main():
    run_ui(htop=HtopLinux())


if __name__ == "__main__":
    main()
