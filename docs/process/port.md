# Port (open firmware)

Default stack: **coreboot** (+ payload such as edk2 / SeaBIOS / LinuxBoot). Libreboot only applies when a board meets its blob policy — most modern Intel laptops will not.

## Suggested order

1. Board skeleton from dump + reference ports of the same SoC
2. Memory init → payload → storage/USB
3. Internal display (libgfxinit / FSP GOP)
4. ACPI from `acpidump`, iteratively
5. EC (battery, keys, lid, PD) — usually the longest pole
6. Discrete GPU / complex mux last

## Blobs reality check

Modern Intel platforms typically still need FSP and a working ME region. EmberROM aims for **maximum open control**, not a promise of zero blobs on every SoC.

Per-board port notes: `targets/<board>/COREBOOT.md`.
