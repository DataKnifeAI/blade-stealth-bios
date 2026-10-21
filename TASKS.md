# Implementation tasks

Ordered work plan for **EmberROM**. First board target: [razer-blade-stealth-2019-rz09-03101](targets/razer-blade-stealth-2019-rz09-03101/).

Legend: `[ ]` pending · `[~]` in progress · `[x]` done

---

## Phase 0 — Bootstrap

- [x] Create project (formerly `blade-stealth-bios`)
- [x] Rename to **emberrom** — general process + `targets/`
- [x] Hero graphic + README
- [x] Document SKU RZ09-03101E72 Aptio Main inventory (BIOS 1.05, EC 1.01, MCU 1.00.06.00, i7-1065G7)
- [x] Capture OS-side inventory (`dmidecode`, `fwupdmgr`, `lspci`, ME 13.0.46.1718, W25Q128.V, GTX 1650)

---

## Phase 1 — Stock firmware + CachyOS (keep it usable)

### S1. Reproduce failure modes / goals
- [x] Owner goals: CachyOS end-state; Ubuntu temporary; buy external programmer; coreboot **feature parity** (P0) — [GOALS.md](targets/razer-blade-stealth-2019-rz09-03101/GOALS.md)
- [x] Confirmed stock issue: **sleep / suspend broken**
- [ ] Characterize suspend (no wake vs re-suspend loop vs blank; s2idle/deep; lid quirk; GPU path) on Ubuntu, then CachyOS
- [x] Record BIOS / EC / MCU from Aptio Main (ME + Advanced/Security/Boot settings still TBD)
- [x] Record ME version (**13.0.46.1718**) and Secure Boot (**off** on this unit); CSM / TB setup options still TBD from Aptio

### S2. NVRAM / fwupd hygiene
- [ ] Document DBX / MokList “Volume Full” risk on Blade Stealth
- [ ] Recommend fwupd denylist / avoid patterns for this SKU
- [ ] Expand CMOS / NVRAM recovery in target [RECOVERY.md](targets/razer-blade-stealth-2019-rz09-03101/RECOVERY.md)

### S3. Boot and runtime enablement
- [ ] CachyOS install notes (Secure Boot off, CSM off, USB boot)
- [ ] Suspend fix or workaround on stock firmware (see [STOCK_FIRMWARE.md](targets/razer-blade-stealth-2019-rz09-03101/STOCK_FIRMWARE.md))
- [ ] iGPU + GTX 1650 Max-Q hybrid graphics notes for CachyOS
- [ ] Thunderbolt / USB-C power / docking notes

---

## Phase 2 — Vendor assets (local only)

### V1. Collect official packages
- [ ] Download BIOS updater (LY320 / v1.05) from Razer RZ09-03101 page
- [ ] Download matching Intel ME firmware updaters (note ME major version on device)
- [ ] Store under `vendor/` (gitignored); record hashes in target `VENDOR_ASSETS.md`

### V2. Full SPI dump (authoritative)
- [x] Probe internal flashrom — W25Q128.V 16 MiB; FLOCKDN; ME/IFD host-RO; BIOS region RW
- [x] Internal full-chip dump (MTD + flashrom); SHA-256 recorded in target [FLASH.md](targets/razer-blade-stealth-2019-rz09-03101/FLASH.md) / [INVENTORY.md](targets/razer-blade-stealth-2019-rz09-03101/INVENTORY.md)
- [~] External CH341A / Pi dump to cross-check; document clip photos after chassis open
- [ ] Archive verified dump offline (never commit)

### V3. Extract / analyze
- [ ] Split IFD regions (BIOS / ME / EC / flash descriptor)
- [x] Capture ACPI tables from running system (`acpidump` — local only)
- [ ] Compare updater capsule contents vs SPI dump

---

## Phase 3 — coreboot port (first target)

### C1. Research baseline
- [ ] Archive notes from [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) and Mimoja PoC
- [ ] Map Ice Lake FSP / microcode / libgfxinit requirements
- [ ] Document IT8320VG EC: ACPI methods, battery, keyboard, USB-PD

### C2. Board bring-up (out of tree first) — aim P0 parity ([GOALS.md](targets/razer-blade-stealth-2019-rz09-03101/GOALS.md))
- [ ] Board skeleton `mb/razer/blade_stealth_icl` (or revive abandoned patch)
- [ ] Memory init + payload boot (SeaBIOS / edk2 / LinuxBoot)
- [ ] eDP + input + NVMe + USB
- [ ] ACPI, lid, battery, thermal, **suspend/resume** — blocked on EC understanding
- [ ] P1 later: Optimus dGPU, Thunderbolt / USB-C PD

### C3. Flash and recovery
- [~] Owner purchasing external 3.3 V SPI programmer + SOIC-8 clip
- [ ] External dump matches internal SHA; clip photos documented
- [ ] Known-good vendor ROM restore procedure tested via external programmer

---

## Phase 4 — EmberROM tooling / upstream

- [ ] Shared helpers under `tools/` (hash log, dump verify, IFD summary)
- [ ] Propose coreboot Gerrit change when cold boot + basics work
- [ ] Link from [dataknife.ai](https://dataknife.ai) catalog when ready
- [ ] Second laptop target (TBD) using [add-target](docs/process/add-target.md)
