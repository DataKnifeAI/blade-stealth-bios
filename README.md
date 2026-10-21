# blade-stealth-bios

Open firmware and CachyOS enablement for the **Razer Blade Stealth 13 Late 2019** (Ice Lake), SKU **RZ09-03101E72**.

Goal: keep this laptop usable on current CachyOS by (1) documenting and fixing stock-firmware / OS blockers, and (2) advancing a [coreboot](https://www.coreboot.org/) port that can eventually replace the vendor AMI Aptio V BIOS with modern, controllable firmware options.

## Hardware

| Field | Value |
|-------|--------|
| Product | Razer Blade Stealth 13" Late 2019 (GTX 1650 Max-Q) |
| SKU | RZ09-03101E72 |
| CPU / iGPU | Ice Lake (e.g. i7-1065G7) + Iris Plus |
| dGPU | NVIDIA GTX 1650 Max-Q |
| EC | ITE IT8320VG (unsupported in coreboot today) |
| Vendor firmware | AMI Aptio V (Razer), last public BIOS ~1.05 |

## Status

Bootstrap. Stock-firmware CachyOS track and coreboot research are in [TASKS.md](TASKS.md). There is **no** flashable open BIOS yet.

Prior art: abandoned coreboot change [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) (Mimoja) — basic RAM init only; missing ACPI, power, and EC.

## Tracks

1. **Stock firmware + CachyOS** — boot, NVRAM, Secure Boot, suspend, GPU, fwupd hygiene so the machine stays usable *now*.
2. **Vendor asset archive** — official BIOS/ME packages for analysis (not committed; see [docs/VENDOR_ASSETS.md](docs/VENDOR_ASSETS.md)).
3. **coreboot port** — revive/extend Ice Lake board support, EC research, recovery plan ([docs/COREBOOT.md](docs/COREBOOT.md)).

## Docs

| Doc | Contents |
|-----|----------|
| [docs/HARDWARE.md](docs/HARDWARE.md) | SKU inventory, chips, flash layout notes |
| [docs/VENDOR_ASSETS.md](docs/VENDOR_ASSETS.md) | What to download from Razer (and what not to) |
| [docs/STOCK_FIRMWARE.md](docs/STOCK_FIRMWARE.md) | CachyOS / AMI BIOS workarounds |
| [docs/COREBOOT.md](docs/COREBOOT.md) | Port plan, blobs, EC, recovery |
| [docs/RECOVERY.md](docs/RECOVERY.md) | Brick recovery / external programmer |
| [TASKS.md](TASKS.md) | Phased work checklist |

## Safety

Flashing firmware can brick the laptop. Internal `flashrom` is often blocked by descriptor locks; plan for an **external SPI programmer** and a verified dump of the original ROM before any write. See [docs/RECOVERY.md](docs/RECOVERY.md).

Proprietary Razer/Intel blobs stay under local `vendor/` / `dumps/` (gitignored). Do not publish full ME/BIOS images.

## License

Apache License 2.0 — see [LICENSE](LICENSE).

Any coreboot board patches contributed upstream remain under coreboot’s license (GPL-2.0). Vendor firmware remains proprietary and is not redistributed from this repository.

Maintained by [DataKnifeAI](https://github.com/DataKnifeAI).
