# Dump

Goal: a **complete SPI ROM image** that can restore the machine.

## Preferred order

1. Try internal read (`flashrom` with the correct chip / programmer backend) if the descriptor allows it.
2. If locked: external programmer + SOIC clip (or desolder).
3. Dump twice; compare SHA-256.
4. Park files under local `dumps/` (gitignored). Record hashes in the target docs.

## Also capture (not SPI)

- `acpidump` / decompiled DSDT+SSDTs
- Optional: `inteltool`, GPIO, HDA verb, VBT extracts once tools are chosen

See [extract.md](extract.md) for splitting IFD regions after the dump exists.
