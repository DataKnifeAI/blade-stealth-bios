# Hardware — RZ09-03101E72

## Identity

| Field | Value |
|-------|--------|
| Marketing name | Razer Blade Stealth 13 Late 2019 |
| SKU | **RZ09-03101E72** |
| Board (DMI) | **LY320** |
| Product version (DMI) | 2.04 |
| Family | 1A581001 Razer Blade Stealth |
| Support page | [Answer 4566 — RZ09-03101 drivers & downloads](https://mysupport.razer.com/app/answers/detail/a_id/4566) |
| SoC generation | Intel Ice Lake-U (ULT) |
| Discrete GPU | NVIDIA GeForce GTX 1650 Max-Q (**verified**) |

## Live inventory (Aptio Setup Utility)

Captured from **Main** tab on this unit (Administrator access). Serial number intentionally omitted from the public repo.

| Field | Value |
|-------|--------|
| Setup utility | AMI Aptio Setup Utility **2.20.1275** (© 2020 American Megatrends) |
| System BIOS Version | **1.05** |
| BIOS build date/time | **10/06/2020 14:00:26** |
| EC FW Version | **1.01** |
| MCU FW Version | **1.00.06.00** |
| Manufacturer | Razer |
| Product Name | Razer Blade Stealth 13 Late 2019 |
| Processor | Intel Core **i7-1065G7** @ 1.30 GHz (reported speed 1500 MHz in setup) |
| Topology | 4 cores / 8 threads |
| Microcode Revision (Aptio) | **2E** |
| GT Info | GT2 (**0x8A52**) — Iris Plus |
| IGFX GOP Version | **14.0.1039** |
| Memory RC Version | **0.0.4.75** |
| Total Memory | **16384 MB** (16 GiB) |

Setup tabs present: Main, Advanced, Chipset, Security, Boot, Save & Exit.

## Live inventory (booted OS)

Captured 2026-10-21 on Ubuntu 26.04.1 (`7.0.0-30-generic`). Serial numbers omitted.

| Field | Value |
|-------|--------|
| SMBIOS | 3.2.0 |
| BIOS (DMI) | Razer **1.05** (2020-10-06); ROM size **16 MB**; UEFI; BIOS rev 1.5 / FW rev 1.1 |
| Secure Boot | **Disabled** (`mokutil`) |
| CPU | i7-1065G7, family 6 model 126 stepping 5; runtime microcode **0xcc** |
| Memory | 2× 8 GiB soldered **LPDDR4** Micron @ **3733 MT/s** configured |
| ME | **13.0.46.1718** (fwupd); device `8086:34e0` (`mei_me`) |
| TPM | Intel fTPM 2.0 — version **500.5.0.0** |
| UEFI dbx | **20230501** (fwupd) |
| SPI flash | Winbond **W25Q128.V** 16 MiB (`flashrom -p internal`); exposed as MTD `BIOS` 16777216 |
| Panel | Sharp **LQ133M1JW41** (EDID SHP, 1920×1080 eDP) |
| Touchpad | Synaptics HID over I2C `06CB:CDA3` |
| Keyboard | USB `1532:024a` Razer Blade Stealth (Late 2019) |
| Audio | Realtek **ALC298** (`10ec:0298`, subsystem `1a58:1001`) |
| Wi‑Fi / BT | Intel AX201 CNVi `8086:34f0` / USB BT `8087:0026` |
| Storage | Lite-On **CA5-8D512** 512 GB NVMe (`14a4:3500`) |
| Camera | IMC Networks `13d3:56d5` |
| EC (ACPI) | `_SB.PCI0.LPCB.EC0` — `PNP0C09` @ IO 0x62/0x66; silicon still believed ITE **IT8320VG** (not in DSDT HID; confirm from dump) |

### PCI map (short)

| Addr | Device |
|------|--------|
| 00:00.0 | Host bridge `8086:8a12` |
| 00:02.0 | Iris Plus G7 `8086:8a52` (i915) |
| 00:07.0 / 00:07.1 | Ice Lake TB3 root ports `8086:8a1d` / `8a1f` |
| 00:0d.0 / 00:0d.2 | TB3 xHCI + NHI `8086:8a13` / `8a17` (thunderbolt) |
| 00:14.3 | AX201 Wi‑Fi `8086:34f0` |
| 00:16.0 | MEI `8086:34e0` |
| 00:1f.0 | LPC `8086:3482` (Ice Lake-LP) |
| 00:1f.5 | SPI controller `8086:34a4` |
| 57:00.0 | GTX 1650 Max-Q `10de:1f91` (nouveau; Optimus 3D) |
| 58:00.0 | NVMe Lite-On CA5 |

### flashrom / IFD (internal programmer)

Probe OK; chipset Ice Lake U Premium. **SPI config lockdown** (`FLOCKDN=1`). fwupd reports Internal SPI “firmware has been locked”.

| Region | Range | Access (host) |
|--------|-------|----------------|
| Flash Descriptor | `0x00000000–0x00000fff` | read-only |
| ME | `0x00001000–0x005fffff` (~6 MiB) | read-only |
| BIOS | `0x00600000–0x00ffffff` (~10 MiB) | read-write |

Implication: a **full** pristine dump for restore/coreboot needs an **external SPI programmer**. Internal `flashrom` may not freely read ME/IFD; do not rely on vendor updater alone once experiments begin.

Local (gitignored) ACPI tables: capture under machine-local `dumps/` / analysis dirs — DSDT + SSDT1–13 present (`acpidump`).

## Silicon notes

| Component | Status on this unit |
|-----------|---------------------|
| CPU | **Verified** i7-1065G7 Ice Lake-U |
| iGPU | **Verified** GT2 `8086:8a52` (Iris Plus G7) |
| dGPU | **Verified** TU117M GTX 1650 Max-Q `10de:1f91` |
| EC | FW **1.01**; ACPI EC0 standard ports; ITE **IT8320VG** still unconfirmed in silicon ID |
| MCU | Separate MCU FW **1.00.06.00** (USB-C/PD related — TBD) |
| Thunderbolt | **Verified** Ice Lake integrated TB3 NHI + dual root ports |
| SPI flash | **Verified** Winbond W25Q128.V 16 MiB; 3.3 V class typical for this part — confirm on chip marking before clipping |
| ME | **Verified** major **13** (`13.0.46.1718`) |

## Why SKU matters

Razer’s Late 2019 Stealth line has multiple variants (Mercury White iGPU-only vs GTX). Firmware capsules and ME major versions can differ. This target is **RZ09-03101E72** specifically; do not flash another SKU’s BIOS updater without verifying compatibility.

Vendor BIOS **1.05** (2020-10-06) matches the public Razer “BIOS v0105 / LY320” package family on Answer 4566 — prefer that updater if restoring stock firmware. Board name **LY320** matches that updater family.
