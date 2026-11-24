#!/usr/bin/env python3
"""news-23 b140 heroes-scene: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
which the grader points at an empty output directory. Validates the PNG header
manually (struct): signature, IHDR 1024x1024, bit depth 8, colour type 2/6,
compression/filter/interlace 0, IHDR CRC, per-chunk CRCs, non-empty IDAT payload,
IEND as the final chunk with no trailing data, size between 10_000 and 1 MiB.
Refuses an empty, in-repo, or file MAKEFUN_OUTPUT_DIR, refuses to overwrite the
source image, and re-reads the output to confirm it is byte-identical.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "a259d241dff95de53f3f8f6e61a215785809583d87c651bc1db75860ea8982f2"  # entry.png, filled in after final render
MIN_SIZE = 10_000
MAX_SIZE = 1_048_576


def fail(msg):
    print("main.py: error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo_abs = os.path.dirname(os.path.abspath(__file__))
    if os.path.commonpath([out_dir_abs, repo_abs]) == repo_abs:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")
    with open(src, "rb") as f:
        data = f.read()
    if not (MIN_SIZE <= len(data) <= MAX_SIZE):
        fail("entry.png size %d out of range" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    # Chunk walk: length (4) + type (4) + data (len) + CRC (4).
    # First chunk must be IHDR, 13 bytes: width, height, bit depth,
    # colour type, compression, filter, interlace.
    pos = 8
    if len(data) < 8 + 25:
        fail("PNG too small for IHDR")
    clen = struct.unpack(">I", data[pos:pos + 4])[0]
    ctype = data[pos + 4:pos + 8]
    if ctype != b"IHDR" or clen != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[pos + 8:pos + 21]
    width, height, depth, ctype_n, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        fail("IHDR size is %dx%d, expected 1024x1024" % (width, height))
    if depth != 8 or ctype_n not in (2, 6):
        fail("IHDR bit depth %d colour type %d unsupported" % (depth, ctype_n))
    if comp != 0 or filt != 0 or inter != 0:
        fail("IHDR compression/filter/interlace must all be 0")
    crc_stored = struct.unpack(">I", data[pos + 21:pos + 25])[0]
    if zlib.crc32(ctype + ihdr) & 0xFFFFFFFF != crc_stored:
        fail("bad CRC in chunk IHDR")
    pos += 8 + clen + 4
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            fail("truncated chunk %s" % ctype.decode("latin-1", "replace"))
        cdata = data[pos + 8:pos + 8 + clen]
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(ctype + cdata) & 0xFFFFFFFF != crc_stored:
            fail("bad CRC in chunk %s" % ctype.decode("latin-1", "replace"))
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if pos + 12 != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            pos += 12
            break
        pos += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small (%d bytes)" % idat_total)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % sha)
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output is not byte-identical to source")
    print("entry.png %d bytes sha256 %s -> %s" % (len(data), sha, dst))


if __name__ == "__main__":
    main()
