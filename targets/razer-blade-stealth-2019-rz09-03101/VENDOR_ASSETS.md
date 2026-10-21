# Vendor assets — RZ09-03101 / LY320

Official download hub:

**[Razer Blade Stealth 13" GTX1650 (2019) \| RZ09-03101](https://mysupport.razer.com/app/answers/detail/a_id/4566)**

Live unit facts (versions, SPI hash): [INVENTORY.md](INVENTORY.md) · dump/recovery: [FLASH.md](FLASH.md).

## Short answer

**Pull firmware packages, not Windows device drivers.**

The authoritative image is still a **full SPI dump from this laptop** ([FLASH.md](FLASH.md)). Razer updaters are for analysis, comparison, and stock restore when the machine still boots.

## Download links (public)

| Asset | Version / notes | Link |
|-------|-----------------|------|
| **BIOS updater** | LY320 · **v1.05** (`BIOSv0105`) — matches this unit | [https://rzr.to/H1kYs](https://rzr.to/H1kYs) |
| BIOS update guide (PDF) | Linked from Answer 4566 | Via hub above |
| ME updater INTEL-SA-00391 | Listed as **ME v14** (`14.0.48.1605`) | [https://rzr.to/Wz84HQ](https://rzr.to/Wz84HQ) |
| ME updater INTEL-SA-00459 | Listed as **ME v12** (`12.0.81.1753`) | [https://rzr.to/tfjQCo](https://rzr.to/tfjQCo) |

**ME caution:** this unit runs **ME 13.0.46.1718**. Answer 4566 currently lists **v12 / v14** only — fine to download for archaeology; **do not flash** an ME updater that does not match major **13** without a verified SPI backup and a deliberate plan.

## Need (local `vendor/` — gitignored)

| Asset | Why |
|-------|-----|
| BIOS updater LY320 v1.05 | Capsule / PEI-DXE / VBT clues; stock restore |
| ME package matching major on device | Region reference; HAP / soft-disable research |
| EC firmware (if separate) | Often inside BIOS; hard blocker for coreboot |

Also capture (not from Razer):

| Asset | Why | Status |
|-------|-----|--------|
| Full SPI ROM dump | IFD + ME + BIOS restore / rebuild | Internal dump done — see [FLASH.md](FLASH.md) hash |
| `acpidump` / DSDT+SSDTs | ACPI + EC methods | Captured locally (not in git) |
| `inteltool` / GPIO / PIRQ | coreboot board config | TBD |

## Do not need for BIOS conversion

Windows-only packages on Answer 4566 (skip for EmberROM):

- Intel Chipset / Serial IO / DPTF
- Intel Iris / NVIDIA GTX 1650 / GeForce Experience
- Intel AX201 Wi‑Fi / Bluetooth
- Thunderbolt 3 Windows driver

## Handling rules

1. Download into repo-root `vendor/` (gitignored). Record SHA-256 below.  
2. **Never commit** BIOS/ME/EC images or updater EXEs.  
3. Document **versions, hashes, and URLs** only.  
4. Before applying any official updater, back up NVRAM/boot state — Blade Stealth models have hit **NVRAM Volume Full** after DBX/fwupd updates.

## Hash log

```text
# date       | sha256 | filename | notes
# 2026-10-21 | e729ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1 | (local SPI dump) | internal MTD/flashrom — see FLASH.md; binary not in git
#            | (pending) | LY320-BIOSv0105* | download from rzr.to/H1kYs
```

## Related

- Same family (Mercury White / early 2019) may differ — do not mix SKUs blindly.  
- SPI dump + recovery: [FLASH.md](FLASH.md) · [RECOVERY.md](RECOVERY.md).
