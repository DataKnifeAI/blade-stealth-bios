# Flash & SPI dump — RZ09-03101E72

Board-specific flash layout, dump methods, and programmer notes. Soft/hard recovery procedures: [RECOVERY.md](RECOVERY.md). Public identity / versions: [INVENTORY.md](INVENTORY.md).

**Never commit** full ROM images, ME regions, or updater binaries. Keep local under repo-root `dumps/` (gitignored).

---

## Chip

| Field | Value |
|-------|--------|
| Soft ID | Winbond **W25Q128.V** |
| Size | **16 MiB** (16777216 bytes) |
| Package | SOIC-8, not socketed ([CL 37565](https://review.coreboot.org/c/coreboot/+/37565) board_info) |
| Voltage | **3.3 V** class — confirm marking before clipping |
| Host SPI | Ice Lake-LP `8086:34a4`; MTD name `BIOS` |

---

## IFD map (this unit)

| Region | Range | Size | Host (internal) |
|--------|-------|------|-----------------|
| Flash Descriptor | `0x00000000` – `0x00000fff` | 4 KiB | read-only |
| Management Engine | `0x00001000` – `0x005fffff` | ~6 MiB | read-only |
| BIOS | `0x00600000` – `0x00ffffff` | ~10 MiB | read-write |

SPI configuration lockdown (`FLOCKDN=1`). fwupd reports Internal SPI “firmware has been locked”.

---

## Reference dump (internal)

Captured 2026-10-21 on the reference unit. Image itself is **local only**.

```text
sha256: e729ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
size:   16777216
```

Two independent methods produced **identical** hashes:

### A. Linux MTD

```bash
sudo dd if=/dev/mtd0ro of=dump1.bin bs=1M status=progress
sudo dd if=/dev/mtd0ro of=dump2.bin bs=1M status=progress
sha256sum dump1.bin dump2.bin   # must match
```

### B. flashrom (internal)

Laptop board string is unknown to flashrom; board enable is required for read:

```bash
sudo flashrom -p internal:laptop=force_I_want_a_brick -r dump1.bin
sudo flashrom -p internal:laptop=force_I_want_a_brick -r dump2.bin
sha256sum dump1.bin dump2.bin
```

Sanity on the reference image: IFD signature at `0x10`, ME `$FPT` / `$MN2`, BIOS `_FVH` volumes.

**Still recommended before any write:** external CH341A / Pi SPI dump, compare SHA-256 to the hash above.

---

## External programmer (recommended before writes)

### Hardware

| Item | Notes |
|------|--------|
| CH341A **v1.6+** with **3.3 V / 5 V** switch | Set **3.3 V** only |
| SOIC-8 / SOP-8 test clip + **25-series** adapter | Red wire = pin 1 |
| Optional host | Raspberry Pi 4 (USB-C + RJ45 + Wi‑Fi) or Zero 2 W over SSH |

Example kit style: search Amazon for `CH341A SOIC8 clip 3.3V`. Prefer boards with a physical voltage selector. Avoid generic 5 V–only modules.

### Laptop prep

1. Shut down completely; unplug AC.  
2. Disconnect internal battery if practical.  
3. Open bottom cover; locate SOIC-8 flash; photograph markings.  
4. Clip with pin‑1 (dot/notch) aligned to clip pin‑1 / red stripe.  
5. Host PC/Pi runs flashrom — Blade stays **off**.

### SOIC-8 SPI pinout

| Pin | Signal |
|-----|--------|
| 1 | CS# |
| 2 | DO (MISO) |
| 3 | WP# |
| 4 | GND |
| 5 | DI (MOSI) |
| 6 | CLK |
| 7 | HOLD# |
| 8 | VCC (3.3 V) |

### Dump (CH341A)

```bash
sudo flashrom -p ch341a_spi -c "W25Q128.V"   # probe
sudo flashrom -p ch341a_spi -c "W25Q128.V" -r ext-1.bin
sudo flashrom -p ch341a_spi -c "W25Q128.V" -r ext-2.bin
sha256sum ext-1.bin ext-2.bin
# compare to e729ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
```

### Dump (Raspberry Pi GPIO SPI)

```bash
# enable SPI via raspi-config; short wires; start slow
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=512 -r ext-1.bin
```

### Write (high risk — only with verified backup offline)

```bash
# Prefer region-limited layout once IFD tools are set up.
# Full-chip example — DO NOT run until restore dump is verified offline:
# sudo flashrom -p ch341a_spi -c "W25Q128.V" -w known-good.bin -v
```

See [safety](../../docs/process/safety.md) risk tiers. Internal host **writes** to ME/IFD are blocked; plan on **external** programmer for full-chip restore.

---

## Razer vendor restore (OS still boots)

| Asset | Link |
|-------|------|
| Hub | [Answer 4566](https://mysupport.razer.com/app/answers/detail/a_id/4566) |
| BIOS LY320 v1.05 | https://rzr.to/H1kYs |

Vendor updater ≠ full SPI backup. Prefer SPI restore once coreboot experiments start.
