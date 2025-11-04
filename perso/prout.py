#!/usr/bin/env python3
from argparse import ArgumentParser
import sys
import os
from pathlib import Path
import subprocess
import shlex
import itertools


def _media_info(path_list, template=None, handle_ouput=None):
    template = template or Path(os.path.dirname(os.path.abspath(__file__))).joinpath("prout.txt")
    media_info_cmd = f"mediainfo --Inform={template.as_uri()} {" ".join(f.expanduser().absolute().as_posix() for f in path_list)}"

    proc = subprocess.run(shlex.split(media_info_cmd), encoding='utf-8', stdout=subprocess.PIPE)

    if handle_ouput:
        yield from handle_ouput(proc.stdout)
        return

    current_record = None
    for line in proc.stdout.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith("Path:"):
            current_record = { "path": line[5:] }
        if line.startswith("Video:"):
            if not current_record:
                continue
            [duration, width, height] = line[6:].split(",")
            current_record.update(duration=duration, width=width, height=height)
            yield current_record
        current_record = None

META_PATTERN = r"<meta_([dwh])_(\d+)_([dwh])_(\d+)_([dwh])_(\d+)_>"

def main():
    parser = ArgumentParser()
    parser.add_argument("--file-names")
    args = parser.parse_args()

    paths = [Path(f) for f in args.file_names.split(",") if f.strip()]
    paths = paths or [Path.cwd()]

    dirs = []
    files = []
    for f in paths:
        f = f.expanduser().absolute()
        if f.is_dir():
            dirs.append(f)
        else:
            files.append(f)

    for batch in itertools.batched(files, n=10):
        print("batch")
        for rec in _media_info(batch):
            print(rec)


if __name__ == "__main__":
    main()
    sys.exit(0)
