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
- [x] Confirmed stock issue: **sleep / suspend broken** (GUI); see [ANALYSIS.md](targets/razer-blade-stealth-2019-rz09-03101/ANALYSIS.md)
- [x] Lab characterize on Ubuntu: `rtcwake` deep+s2idle succeed; `_WAK`/`VRTC` ACPI errors; nouveau+i915; lid quirk open
- [ ] Interactive failure mode (blank / lid loop) + s2idle daily trial + nouveau blacklist; retest on CachyOS
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
- [x] Split IFD regions (FD / ME / BIOS) via `tools/ifd_split.py` — **no IFD EC region**
- [x] Capture ACPI tables from running system (`acpidump` — local only)
- [x] First-pass ACPI/EC notes (lid, `_WAK`/`RTEC`/`VRTC`, MLBX 0x300) — [ANALYSIS.md](targets/razer-blade-stealth-2019-rz09-03101/ANALYSIS.md)
- [x] Locate VBT in BIOS region (`$VBT ICELAKE` @ SPI `0xe2c484`; hashes in ANALYSIS) — full DXE/GOP FFS names still need UEFITool
- [~] Optimus ACPI: SSDT11 `HgRpSsdt` + SSDT13 `Opt1Tabl` (`HGON`/`HGOF`/`NGC6`) noted; pin/rail map TBD
- [ ] Compare updater capsule contents vs SPI dump

---

## Phase 3 — coreboot port (first target)

### C0. Fork / tree
- [x] Fork upstream coreboot → [DataKnifeAI/coreboot](https://github.com/DataKnifeAI/coreboot)
- [x] Reference branch [`emberrom/icelake-ref`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake-ref) from upstream `4.19_branch` (`79a11950ac` — Ice Lake SoC present; ICL drop [CL 72008](https://review.coreboot.org/c/coreboot/+/72008) is post–4.19)
- [x] WIP [`emberrom/icelake`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake) reset onto ref + [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) PS16 (`386d05a1f8`, clean cherry-pick; credit Johanna Schander / Mimoja)
- [x] Document fork + Gerrit-upstream workflow + checkout recipe in target [COREBOOT.md](targets/razer-blade-stealth-2019-rz09-03101/COREBOOT.md)

### C1. Research baseline
- [x] Archive / apply [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) PS16 onto 4.19-era tree (see [COREBOOT.md](targets/razer-blade-stealth-2019-rz09-03101/COREBOOT.md)); deeper Mimoja PoC notes still TBD
- [ ] Map Ice Lake FSP / microcode / libgfxinit requirements for 4.19-era build
- [~] EC: ACPI map started (`EC0`, `LIDS`, `MLBX`); confirm IT8320VG + protocol next

### C2. Board bring-up (on DataKnifeAI fork first) — aim P0 parity ([GOALS.md](targets/razer-blade-stealth-2019-rz09-03101/GOALS.md))
- [x] Board skeleton `mb/razer/blade_stealth_icl` from CL 37565 (Mercury White prior art; GTX 03101 still unverified)
- [ ] `make menuconfig` / build smoke-test on `emberrom/icelake` (FSP blobs local; no flash)
- [ ] Memory init + payload boot (SeaBIOS / edk2 / LinuxBoot)
- [ ] eDP + input + NVMe + USB
- [ ] ACPI, lid, battery, thermal, **suspend/resume** — blocked on EC understanding
- [ ] P1 later: Optimus dGPU, Thunderbolt / USB-C PD

### C3. Flash and recovery
- [x] Pre-flash go/no-go checklist — [PREFLASH.md](targets/razer-blade-stealth-2019-rz09-03101/PREFLASH.md) (build / stitch / SHA / 3.3 V / restore / GTX deltas / signoff)
- [~] Owner purchasing external 3.3 V SPI programmer + SOIC-8 clip
- [ ] External dump matches internal SHA `e6929ca0…`; clip photos documented
- [ ] Known-good vendor ROM restore procedure tested via external programmer
- [ ] **STOP before write** until PREFLASH signoff is GO — no `flashrom -w` yet

---

## Phase 4 — EmberROM tooling / upstream

- [ ] Shared helpers under `tools/` (hash log, dump verify, IFD summary)
- [ ] Propose coreboot Gerrit change when cold boot + basics work (develop on [DataKnifeAI/coreboot](https://github.com/DataKnifeAI/coreboot); do not use GitHub PRs for upstream)
- [ ] Link from [dataknife.ai](https://dataknife.ai) catalog when ready
- [ ] Second laptop target (TBD) using [add-target](docs/process/add-target.md)
