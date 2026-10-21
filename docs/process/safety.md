# Safety

Firmware work can brick a laptop. EmberROM assumes **external SPI recovery** is available before any experimental write.

## Rules

1. Dump the full ROM **twice**; hashes must match before you trust the backup.
2. Store dumps offline — not only on the machine under test.
3. Confirm flash voltage (1.8 V vs 3.3 V) and chip package before clipping.
4. Prefer stock-firmware / OS workarounds until a recovery path is proven.
5. Never commit proprietary ROM images, ME regions, or updater binaries to git.

## Risk tiers

| Tier | Examples | Bar before doing it |
|------|----------|---------------------|
| Low | Docs, `acpidump`, vendor package download, OS quirks | None |
| Medium | Internal `flashrom` **read**, IFD parse, capsule extract | Verified offline dump storage |
| High | Any SPI **write**, ME neutralize experiments, EC reflash | External programmer + known-good restore tested |

Board-specific recovery notes live under each `targets/<board>/RECOVERY.md`.
