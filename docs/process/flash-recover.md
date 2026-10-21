# Flash & recover

## Flash

- Only after [safety.md](safety.md) high-tier bar is met
- Prefer writing a single region when the IFD allows it; otherwise full-chip with verified image
- Verify readback after write

## Recover

1. Soft: UEFI defaults, CMOS clear, vendor updater (if OS/EFI still runs)
2. Hard: external SPI restore of the pristine dump

Document board-specific clip photos and pinouts under `targets/<board>/` or `docs/assets/` — never commit ROM binaries.
