#!/usr/bin/env python3
"""Deliver the finished front page for Saturday 21 November 2026.

This is the entry program for the make.fun news-image-20261121
competition. The page itself lives in this repository as entry.png;
the program only carries that exact file to the grader's output
directory and checks the copy byte for byte before it reports
success.

It needs nothing but the Python 3.13 standard library, touches no
network, and writes the same bytes on every run.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def _png_dimensions(data):
    # Width and height live in the IHDR chunk: 8 magic bytes, then a
    # 4-byte length, the 4-byte "IHDR" tag, then width and height as
    # two big-endian 32-bit numbers.
    if len(data) < 29 or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _fail(message):
    print("entry failed: " + message, file=sys.stderr)
    return 1


def run():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        return _fail("entry.png is not in the repository")
    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        return _fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if not data.startswith(PNG_MAGIC):
        return _fail("entry.png is not a PNG file")
    dims = _png_dimensions(data)
    if dims is None:
        return _fail("entry.png has no readable IHDR chunk")
    if dims[0] > MAX_SIDE or dims[1] > MAX_SIDE:
        return _fail("entry.png is %dx%d, over the 1024x1024 limit" % dims)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    if _digest(target) != _digest(source):
        return _fail("the written copy differs from entry.png")
    print("wrote %s (%d bytes)" % (target, len(data)))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
