# Vendor assets — what to get from Razer

Official download hub for this board:

**[Razer Blade Stealth 13" GTX1650 (2019) \| RZ09-03101](https://mysupport.razer.com/app/answers/detail/a_id/4566)**

## Short answer

**Yes — pull the firmware packages, not the Windows device drivers.**

For an open-BIOS / coreboot effort you need **firmware images and flash layout**, not Intel/NVIDIA Windows installers. The most important artifact is still a **full SPI dump from your own laptop**; Razer’s updaters are secondary (analysis, comparison, sometimes extractable regions).

## Need (keep local under repo-root `vendor/` — gitignored)

| Asset | Why | Source on Answer 4566 |
|-------|-----|------------------------|
| **BIOS updater** (`LY320-BIOSv0105` / guide + package) | AMI capsule / PEI/DXE modules, VBT clues, version baseline | “Razer Blade Stealth 13” (2019) BIOS Update” ~v1.05 |
| **Intel ME firmware updater** matching the ME major on the device | ME region reference; HAP / soft-disable research | INTEL-SA-00391 / SA-00459 packages (ME **v12** vs **v14** — pick what matches `me_status` / fwupd) |
| **EC firmware** (if published separately) | Keyboard, battery, USB-PD, power sequencing — hard blocker for coreboot | Often bundled inside BIOS; check updater contents. Separate EC packages exist for *other* Stealth years — verify for 03101 |

Also capture (not from Razer):

| Asset | Why |
|-------|-----|
| **Full SPI ROM dump** from RZ09-03101E72 | Authoritative IFD + ME + BIOS + EC regions for rebuild / restore |
| **`acpidump` / SSDT/DSDT** from CachyOS or Windows | Porting ACPI and EC methods |
| **`inteltool` / GPIO / PIRQ dumps** | Board config for coreboot |

## Do not need for BIOS conversion

Windows-only packages on that page are **OS drivers**, not flash ingredients:

- Intel Chipset / Serial IO / DPTF (Windows)
- Intel Iris / NVIDIA GTX 1650 / GeForce Experience
- Intel AX201 Wi‑Fi / Bluetooth (Windows)
- Thunderbolt 3 Windows driver

Linux (CachyOS) uses in-kernel or distro packages for those. They do not help build coreboot.

## Handling rules

1. Download into repo-root `vendor/` (gitignored). Record SHA-256 here when collected.
2. **Never commit** full BIOS/ME/EC images or updater EXEs to this repo.
3. Prefer documenting **extraction steps + hashes** so others can fetch from Razer.
4. Before applying any official updater, back up NVRAM/boot state — Blade Stealth models have hit **NVRAM Volume Full** after DBX/fwupd updates.

## Hash log (fill in when downloaded)

```text
# date | sha256 | filename | notes
```

## Related pages

- Same family (non-GTX / early 2019) may list different BIOS/EC — do not mix blindly.
- ME security advisories packaged by Razer are useful for **version archaeology**, not as a substitute for a device dump.
