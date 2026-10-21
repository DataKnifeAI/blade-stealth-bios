# Target: Razer Blade Stealth Late 2019 (RZ09-03101)

First EmberROM board target — Ice Lake Blade Stealth, SKU **RZ09-03101E72** (board **LY320**).

| Doc | Contents |
|-----|----------|
| [GOALS.md](GOALS.md) | OS target, suspend bug, programmer, coreboot parity bar |
| [ANALYSIS.md](ANALYSIS.md) | Suspend labs, IFD split, VBT/GOP offsets, ACPI/EC findings |
| [INVENTORY.md](INVENTORY.md) | Public Razer / live capture (SKU, firmware, SPI hash — no serials/blobs) |
| [FLASH.md](FLASH.md) | SPI chip, IFD map, dump/write commands, programmer notes |
| [PREFLASH.md](PREFLASH.md) | **Ordered go/no-go gates before any SPI write** |
| [RECOVERY.md](RECOVERY.md) | Soft/hard recovery |
| [HARDWARE.md](HARDWARE.md) | Aptio inventory, silicon notes |
| [VENDOR_ASSETS.md](VENDOR_ASSETS.md) | What to download from Razer |
| [STOCK_FIRMWARE.md](STOCK_FIRMWARE.md) | CachyOS / AMI workarounds (suspend) |
| [COREBOOT.md](COREBOOT.md) | Port plan + prior art |

**Quick facts:** BIOS **1.05** · EC **1.01** · ME **13.0.46.1718** · W25Q128.V 16 MiB · GTX 1650 Max-Q verified.  
**Goals:** CachyOS end-state · stock **suspend broken** · external programmer incoming · **coreboot feature parity** (P0 daily driver).

Support hub: [Answer 4566](https://mysupport.razer.com/app/answers/detail/a_id/4566) · BIOS updater: [LY320 v1.05](https://rzr.to/H1kYs).

Shared process: [../../docs/process/](../../docs/process/). Org tasks: [../../TASKS.md](../../TASKS.md).
