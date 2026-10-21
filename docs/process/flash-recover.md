# Flash & recover

## Flash

- Only after [safety.md](safety.md) high-tier bar is met
- Prefer writing a single region when the IFD allows it; otherwise full-chip with verified image
- Verify readback after write
- Dump twice and match hashes **before** any write; keep an offline copy

## Recover

1. Soft: UEFI defaults, CMOS clear, vendor updater (if OS/EFI still runs)
2. Hard: external SPI restore of the pristine dump

Document board-specific clip photos and pinouts under `targets/<board>/` or `docs/assets/` — never commit ROM binaries.

## First target (Razer Blade Stealth Late 2019)

Board-specific IFD map, internal/external dump commands, and recovery:  
[`targets/razer-blade-stealth-2019-rz09-03101/FLASH.md`](../../targets/razer-blade-stealth-2019-rz09-03101/FLASH.md) ·  
[`RECOVERY.md`](../../targets/razer-blade-stealth-2019-rz09-03101/RECOVERY.md) ·  
[`INVENTORY.md`](../../targets/razer-blade-stealth-2019-rz09-03101/INVENTORY.md).
