#!/usr/bin/env python3
"""Split an Intel SPI image by Flash Descriptor regions (no external deps)."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

REGION_NAMES = {
    0: "fd",
    1: "bios",
    2: "me",
    3: "gbe",
    4: "pd",
    5: "res1",
    6: "res2",
    7: "res3",
    8: "ec",
    9: "res5",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_ifd(img: bytes) -> dict:
    if len(img) < 0x1000:
        raise SystemExit("image too small for IFD")
    # Signature at FLVALSIG (0x10): 0x0FF0A55A
    sig = struct.unpack_from("<I", img, 0x10)[0]
    if sig != 0x0FF0A55A:
        # Some dumps start with signature at 0x0
        sig0 = struct.unpack_from("<I", img, 0x0)[0]
        if sig0 != 0x0FF0A55A:
            raise SystemExit(f"bad IFD signature: 0x{sig:08x} (offset 0x10)")
        base = 0
    else:
        base = 0

    flmap0 = struct.unpack_from("<I", img, base + 0x14)[0]
    nr = (flmap0 >> 24) & 0x7
    # Region base/limit registers start at 0x40 (FLREG0)
    regions = []
    for i in range(max(nr + 1, 9)):
        reg = struct.unpack_from("<I", img, base + 0x40 + 4 * i)[0]
        base_blocks = reg & 0x7FFF
        limit_blocks = (reg >> 16) & 0x7FFF
        unused = base_blocks == 0x7FFF or limit_blocks < base_blocks
        start = base_blocks << 12
        end = (limit_blocks << 12) + 0xFFF
        regions.append(
            {
                "id": i,
                "name": REGION_NAMES.get(i, f"reg{i}"),
                "flreg": f"0x{reg:08x}",
                "start": start,
                "end": end,
                "size": 0 if unused else end - start + 1,
                "unused": unused,
            }
        )
    return {
        "signature": f"0x{sig:08x}",
        "flmap0": f"0x{flmap0:08x}",
        "nr": nr,
        "image_size": len(img),
        "image_sha256": sha256(img),
        "regions": regions,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="directory for region binaries")
    ap.add_argument("--json", action="store_true", help="print machine-readable summary")
    args = ap.parse_args()

    img = args.image.read_bytes()
    meta = parse_ifd(img)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "ifd.json").write_text(json.dumps(meta, indent=2) + "\n")
        for r in meta["regions"]:
            if r["unused"] or r["size"] <= 0:
                continue
            chunk = img[r["start"] : r["end"] + 1]
            name = f"{r['id']:02d}_{r['name']}_{r['start']:08x}-{r['end']:08x}.bin"
            path = args.out / name
            path.write_bytes(chunk)
            r["sha256"] = sha256(chunk)
            r["file"] = name
        (args.out / "ifd.json").write_text(json.dumps(meta, indent=2) + "\n")

    if args.json:
        json.dump(meta, sys.stdout, indent=2)
        print()
        return

    print(f"image: {args.image} ({meta['image_size']} bytes)")
    print(f"sha256: {meta['image_sha256']}")
    print(f"IFD sig: {meta['signature']}  FLMAP0: {meta['flmap0']}  NR={meta['nr']}")
    print(f"{'id':>2}  {'name':<6}  {'start':>10}  {'end':>10}  {'size':>10}  notes")
    for r in meta["regions"]:
        if r["unused"]:
            print(f"{r['id']:2d}  {r['name']:<6}  {'—':>10}  {'—':>10}  {'—':>10}  unused")
            continue
        note = r.get("file", "")
        print(
            f"{r['id']:2d}  {r['name']:<6}  0x{r['start']:08x}  0x{r['end']:08x}  "
            f"{r['size']:>10}  {note}"
        )


if __name__ == "__main__":
    main()
