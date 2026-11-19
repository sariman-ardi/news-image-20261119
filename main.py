#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261119 bounty.

Copies the pre-drawn entry.png (built by build_image.py) into the output
directory the harness provides. Python standard library only, no network.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    expected = sha256_of(source)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if sha256_of(target) != expected:
        print("copied entry.png does not match the source", file=sys.stderr)
        return 1
    print("wrote", target, os.path.getsize(target), "bytes, sha256", expected[:16])


if __name__ == "__main__":
    sys.exit(main())
