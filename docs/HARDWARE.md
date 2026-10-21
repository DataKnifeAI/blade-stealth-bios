# Hardware — RZ09-03101E72

## Identity

| Field | Value |
|-------|--------|
| Marketing name | Razer Blade Stealth 13" Late 2019 (GTX) |
| SKU | **RZ09-03101E72** |
| Support page | [Answer 4566 — RZ09-03101 drivers & downloads](https://mysupport.razer.com/app/answers/detail/a_id/4566) |
| SoC generation | Intel Ice Lake-U |
| Discrete GPU | NVIDIA GeForce GTX 1650 Max-Q |

Confirm on the machine:

```bash
sudo dmidecode -s system-product-name
sudo dmidecode -s system-sku-number
sudo dmidecode -s bios-version
cat /sys/class/dmi/id/product_name /sys/class/dmi/id/product_sku
```

## Expected silicon (from prior coreboot / teardown notes)

Subject to verification on this unit:

| Component | Notes |
|-----------|--------|
| CPU | Ice Lake-U (commonly i7-1065G7 on this SKU line) |
| iGPU | Intel Iris Plus |
| dGPU | GTX 1650 Max-Q (Optimus / hybrid) |
| EC | ITE **IT8320VG** — USB-C/PD capable EC; **not** supported in coreboot |
| Thunderbolt | Titan Ridge (TB3) |
| Audio | Realtek (jack + speakers; exact codecs TBD from dump) |
| WLAN | Intel AX201 (per Razer driver package list) |
| SPI flash | Size / model TBD from `flashrom` or external read |

## Why SKU matters

Razer’s Late 2019 Stealth line has multiple variants (Mercury White iGPU-only vs GTX). Firmware capsules and ME major versions can differ. This project targets **RZ09-03101E72** specifically; do not flash another SKU’s BIOS updater without verifying compatibility.
