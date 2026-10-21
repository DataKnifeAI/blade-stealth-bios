# Live inventory — RZ09-03101E72

Public, non-sensitive facts captured from a reference unit for EmberROM / coreboot work.

**Omitted on purpose:** system serial, UUID, disk serials, battery serials, MAC addresses, and all firmware binaries.

Captured: **2026-10-21** · Host OS at capture: Ubuntu 26.04.1 (`7.0.0-30-generic`).

---

## Identity

| Field | Value |
|-------|--------|
| Marketing name | Razer Blade Stealth 13 Late 2019 |
| SKU | **RZ09-03101E72** |
| Board name (DMI) | **LY320** |
| Product version (DMI) | 2.04 |
| Product family | 1A581001 Razer Blade Stealth |
| Chassis | Notebook |
| Support / downloads | [Answer 4566 — RZ09-03101](https://mysupport.razer.com/app/answers/detail/a_id/4566) |

---

## Firmware versions

| Component | Version |
|-----------|---------|
| Setup utility | AMI Aptio Setup Utility **2.20.1275** |
| System BIOS | **1.05** (build **2020-10-06 14:00:26**) |
| BIOS revision (DMI) | 1.5 |
| Firmware revision (DMI) | 1.1 |
| EC FW (Aptio) | **1.01** |
| MCU FW (Aptio) | **1.00.06.00** |
| Intel ME (fwupd) | **13.0.46.1718** |
| CPU microcode (Aptio) | **2E** |
| CPU microcode (runtime) | **0xcc** |
| IGFX GOP (Aptio) | 14.0.1039 |
| Memory RC (Aptio) | 0.0.4.75 |
| UEFI dbx (fwupd) | 20230501 |
| TPM | Intel fTPM 2.0 · **500.5.0.0** |
| Secure Boot | Disabled (on reference unit) |

Vendor BIOS package family on Razer support: **LY320 / BIOSv0105** — [download](https://rzr.to/H1kYs).  
ME updaters listed on Answer 4566 are **v12 / v14**; this unit runs **ME 13** — do not flash mismatched ME packages.

---

## Silicon / peripherals (verified in OS)

| Component | Detail |
|-----------|--------|
| CPU | Intel Core **i7-1065G7** (Ice Lake-U, family 6 model 126 stepping 5) |
| Memory | 16 GiB soldered **LPDDR4** (2× 8 GiB Micron), configured **3733 MT/s** |
| iGPU | Iris Plus G7 **`8086:8a52`** (i915) |
| dGPU | GeForce GTX 1650 Max-Q **`10de:1f91`** (TU117M; nouveau at capture) |
| PCH LPC | Ice Lake-LP **`8086:3482`** |
| SPI controller | **`8086:34a4`** |
| MEI | **`8086:34e0`** |
| Thunderbolt | Ice Lake TB3 root ports + NHI (`8086:8a1d` / `8a1f` / `8a17`) |
| Wi‑Fi | Intel AX201 CNVi **`8086:34f0`** |
| Bluetooth | Intel USB **`8087:0026`** |
| Audio | Realtek **ALC298** (`10ec:0298`, subsystem `1a58:1001`) |
| NVMe | Lite-On CA5-series 512 GB class (`14a4:3500`) — model family only |
| Panel | Sharp **LQ133M1JW41** · 1920×1080 eDP |
| Touchpad | Synaptics HID-I2C **`06CB:CDA3`** |
| Keyboard | USB **`1532:024a`** (Razer Blade Stealth Late 2019) |
| Camera | IMC Networks **`13d3:56d5`** |
| EC (ACPI) | `_SB.PCI0.LPCB.EC0` · `PNP0C09` @ IO **0x62 / 0x66** |
| EC silicon | Believed ITE **IT8320VG** (not exposed as ACPI HID; confirm from SPI/EC analysis) |

Razer PCI subsystem ID seen on onboard devices: **`1a58:1001`**.

---

## SPI flash

| Field | Value |
|-------|--------|
| Chip (flashrom) | Winbond **W25Q128.V** |
| Size | **16 MiB** (16777216 bytes) |
| Package | SOIC-8, not socketed |
| Host lockdown | SPI config locked (`FLOCKDN`); fwupd reports Internal SPI locked |
| Voltage class | **3.3 V** typical for W25Q128.V — confirm on chip marking before external clip |

### IFD regions (from internal probe)

| Region | Range | Host access (internal) |
|--------|-------|-------------------------|
| Flash Descriptor | `0x00000000` – `0x00000fff` | read-only |
| Management Engine | `0x00001000` – `0x005fffff` | read-only |
| BIOS | `0x00600000` – `0x00ffffff` | read-write |

### Internal dump (reference unit)

Full-chip image obtained locally via Linux MTD and `flashrom` (not redistributed here).

```text
sha256: e729ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
size:   16777216
```

Methods that matched on this unit:

```bash
# MTD (read-only node)
sudo dd if=/dev/mtd0ro of=dump.bin bs=1M

# flashrom (laptop board enable required on this unknown board string)
sudo flashrom -p internal:laptop=force_I_want_a_brick -r dump.bin
```

Dump twice; hashes must match. Keep images **offline / gitignored** (`dumps/`). Image sanity checks on the reference dump: IFD signature present, ME `$FPT` / `$MN2`, BIOS `_FVH` volumes.

An external CH341A (3.3 V) + SOIC-8 clip dump is still recommended before any experimental **write**.

---

## Official Razer assets (public links)

| Asset | Link |
|-------|------|
| Drivers & firmware hub | https://mysupport.razer.com/app/answers/detail/a_id/4566 |
| BIOS updater LY320 v1.05 | https://rzr.to/H1kYs |
| ME updater (listed v14 / SA-00391) | https://rzr.to/Wz84HQ |
| ME updater (listed v12 / SA-00459) | https://rzr.to/tfjQCo |

Pull packages into local `vendor/` only; record SHA-256 in [VENDOR_ASSETS.md](VENDOR_ASSETS.md). Never commit updater binaries or SPI images.

---

## Related docs

- [HARDWARE.md](HARDWARE.md) — Aptio + silicon notes  
- [VENDOR_ASSETS.md](VENDOR_ASSETS.md) — what to download  
- [RECOVERY.md](RECOVERY.md) — soft/hard recovery  
- [COREBOOT.md](COREBOOT.md) — port plan  
- [STOCK_FIRMWARE.md](STOCK_FIRMWARE.md) — stock OS enablement  
