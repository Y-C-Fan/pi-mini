"""命令行入口。P0 只提供 --version 与 --roadmap。"""

from __future__ import annotations

import argparse
import sys

from pi_mini import DONE, ROADMAP, __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pi-mini", description="mini Pi agent harness")
    parser.add_argument("-V", "--version", action="store_true", help="print version")
    parser.add_argument("--roadmap", action="store_true", help="print learning roadmap")
    parser.add_argument("-p", "--print", dest="prompt", metavar="PROMPT", help="one-shot prompt (P0)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.version:
        print(f"pi-mini {__version__}")
        return 0

    if args.roadmap:
        for stage, title in ROADMAP:
            mark = "x" if stage in DONE else " "
            print(f"[{mark}] {stage} {title}")
        return 0

    if args.prompt is not None:
        print("P0 not implemented yet. Read PLAN.md section P0.", file=sys.stderr)
        return 2

    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
