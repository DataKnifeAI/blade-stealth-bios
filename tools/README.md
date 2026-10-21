# tools/

Board-agnostic helpers for EmberROM.

| Tool | Purpose |
|------|---------|
| [`ifd_split.py`](ifd_split.py) | Split an Intel SPI dump by Flash Descriptor regions; write `ifd.json` + region bins |

```bash
python3 tools/ifd_split.py dumps/blade-rz09-03101e72-spi-16m.bin -o extract/ifd
```

Region binaries under `extract/` are gitignored — commit hashes/notes in target `ANALYSIS.md` only.
