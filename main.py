#!/usr/bin/env python3
"""news-image-20261121 v2 — entrypoint (standard library only).

Copies the entry image this repository holds (entry.png, drawn by
draw.py) to the output directory, after validating that it is a whole
PNG within the contest limits. Deterministic: the same bytes every run.
"""
import os
import shutil
import struct
import sys
import zlib

MAX_BYTES = 1048576
MAX_DIM = 1024


def validate_png(path):
    """Check magic, IHDR size, whole-file chunk CRCs, and the size cap."""
    data = open(path, "rb").read()
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png over 1 MiB: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR first")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit("entry.png over 1024x1024: %dx%d" % (width, height))
    pos, seen_iend = 8, False
    while pos < len(data):
        if pos + 8 > len(data):
            raise SystemExit("entry.png truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise SystemExit("entry.png truncated chunk %r" % ctype)
        crc = struct.unpack(">I", data[end - 4:end])[0]
        if zlib.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF != crc:
            raise SystemExit("entry.png bad CRC in chunk %r" % ctype)
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                raise SystemExit("entry.png has trailing bytes after IEND")
            break
        pos = end
    if not seen_iend:
        raise SystemExit("entry.png has no IEND")
    return width, height, len(data)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    width, height, size = validate_png(src)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s %dx%d %d bytes" % (dst, width, height, size))


if __name__ == "__main__":
    main()
