#!/usr/bin/env python3
"""The World - Saturday 21 November 2026.

Entry program for the make.fun news-image-20261121 competition. The
finished front page is bundled in this repository as entry.png; this
program's only job is to deliver that exact image to the output path
the grader expects, and to refuse to finish if the copy is not
byte-identical to the bundled original.

Standard library only. No network, no randomness: run it twice and
the two outputs are the same bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("bundled entry.png is missing from the repository", file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size > 1048576:
        print("bundled entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    if sha256_of(SOURCE) != sha256_of(TARGET):
        print("output does not match the bundled image", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (TARGET, os.path.getsize(TARGET)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
