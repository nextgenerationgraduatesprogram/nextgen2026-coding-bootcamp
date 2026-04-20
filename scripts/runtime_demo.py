from pathlib import Path
import sys


def main() -> None:
    print(f"__name__ = {__name__}")
    print(f"sys.argv = {sys.argv}")
    print(f"cwd = {Path.cwd()}")
    print(f"results exists? {Path('results').exists()}")


if __name__ == "__main__":
    main()
