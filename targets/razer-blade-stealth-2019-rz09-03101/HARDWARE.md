# Hardware — RZ09-03101E72

## Identity

| Field | Value |
|-------|--------|
| Marketing name | Razer Blade Stealth 13 Late 2019 |
| SKU | **RZ09-03101E72** |
| Product version (DMI) | 2.04 |
| Support page | [Answer 4566 — RZ09-03101 drivers & downloads](https://mysupport.razer.com/app/answers/detail/a_id/4566) |
| SoC generation | Intel Ice Lake-U (ULT) |
| Discrete GPU | NVIDIA GeForce GTX 1650 Max-Q (expected on this SKU; confirm in OS) |

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
| Microcode Revision | **2E** |
| GT Info | GT2 (**0x8A52**) — Iris Plus |
| IGFX GOP Version | **14.0.1039** |
| Memory RC Version | **0.0.4.75** |
| Total Memory | **16384 MB** (16 GiB) |

Setup tabs present: Main, Advanced, Chipset, Security, Boot, Save & Exit.

Still useful from a booted OS (not yet recorded here):

```bash
sudo dmidecode -t bios -t system -t baseboard
fwupdmgr get-devices || true
cat /sys/class/dmi/id/bios_version /sys/class/dmi/id/product_sku
```

## Silicon notes

| Component | Status on this unit |
|-----------|---------------------|
| CPU | **Verified** i7-1065G7 Ice Lake-U |
| iGPU | **Verified** GT2 device id 0x8A52 (Iris Plus) |
| dGPU | Expected GTX 1650 Max-Q for RZ09-03101 — confirm with `lspci` |
| EC | Firmware **1.01** in Aptio; silicon still believed ITE **IT8320VG** (confirm via dump / LPC ID) |
| MCU | Separate MCU FW **1.00.06.00** (likely USB-C/PD or related controller — TBD) |
| Thunderbolt | Titan Ridge class on Late 2019 Stealth — confirm in OS |
| SPI flash | Size / model TBD from `flashrom` or external read |

## Why SKU matters

Razer’s Late 2019 Stealth line has multiple variants (Mercury White iGPU-only vs GTX). Firmware capsules and ME major versions can differ. This target is **RZ09-03101E72** specifically; do not flash another SKU’s BIOS updater without verifying compatibility.

Vendor BIOS **1.05** (2020-10-06) matches the public Razer “BIOS v0105 / LY320” package family on Answer 4566 — prefer that updater if restoring stock firmware.
