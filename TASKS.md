# Implementation tasks

Ordered work plan. Mirror as GitHub Issues when the remote exists; keep this file updated as tasks complete.

Legend: `[ ]` pending · `[~]` in progress · `[x]` done

---

## Phase 0 — Bootstrap

- [x] Create `DataKnifeAI/blade-stealth-bios` repository layout
- [x] Apache-2.0 LICENSE, README, docs skeleton, TASKS
- [x] Document SKU RZ09-03101E72 (Ice Lake) and vendor download page
- [x] Create GitHub repo under DataKnifeAI + push `main`
- [ ] Capture live machine inventory (`dmidecode`, `/sys/class/dmi`, `fwupdmgr`, BIOS version)

---

## Phase 1 — Stock firmware + CachyOS (keep it usable)

### S1. Reproduce CachyOS failure modes
- [ ] Document exact failure: ISO boot, install, post-install (NVRAM full, Secure Boot, GPU, suspend, …)
- [ ] Record current BIOS / ME / EC versions and UEFI settings that matter

### S2. NVRAM / fwupd hygiene
- [ ] Document DBX / MokList “Volume Full” risk on Blade Stealth
- [ ] Recommend fwupd denylist / avoid patterns for this SKU
- [ ] CMOS / NVRAM recovery steps in [docs/RECOVERY.md](docs/RECOVERY.md)

### S3. Boot and runtime enablement
- [ ] Installer boot notes (Secure Boot, CSM off, USB-C vs USB-A)
- [ ] Kernel cmdline / quirks still needed on modern CachyOS kernels
- [ ] iGPU + GTX 1650 Max-Q hybrid graphics notes for CachyOS
- [ ] Thunderbolt / USB-C power / docking notes

---

## Phase 2 — Vendor assets (local only)

### V1. Collect official packages
- [ ] Download BIOS updater (LY320 / v1.05) from Razer RZ09-03101 page
- [ ] Download matching Intel ME firmware updaters (note ME major version on device)
- [ ] Store under `vendor/` (gitignored); record hashes in `docs/VENDOR_ASSETS.md`

### V2. Full SPI dump (authoritative)
- [ ] Determine if internal flashrom read works (descriptor / HAP / HWP)
- [ ] If locked: external programmer procedure + clip pinout notes
- [ ] Dump full ROM; verify checksums; archive offline (never commit)

### V3. Extract / analyze
- [ ] Split IFD regions (BIOS / ME / EC / flash descriptor)
- [ ] Extract VBT, ACPI tables from running system (`acpidump`)
- [ ] Compare updater capsule contents vs SPI dump

---

## Phase 3 — coreboot port

### C1. Research baseline
- [ ] Archive notes from [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) and Mimoja PoC
- [ ] Map Ice Lake FSP / microcode / libgfxinit requirements
- [ ] Document IT8320VG EC: ACPI methods, battery, keyboard, USB-PD

### C2. Board bring-up (out of tree first)
- [ ] Board skeleton `mb/razer/blade_stealth_icl` (or revive abandoned patch)
- [ ] Memory init + payload boot (SeaBIOS / edk2 / LinuxBoot)
- [ ] ACPI, lid, battery, thermal — blocked on EC understanding

### C3. Flash and recovery
- [ ] Dual-BIOS / external flash workflow documented and tested on spare chip if possible
- [ ] Known-good vendor ROM restore procedure

---

## Phase 4 — Upstream / packaging

- [ ] Propose coreboot Gerrit change when cold boot + basics work
- [ ] Optional: build scripts / docs only in this repo; no proprietary redistributes
- [ ] Link from [dataknife.ai](https://dataknife.ai) catalog when public
