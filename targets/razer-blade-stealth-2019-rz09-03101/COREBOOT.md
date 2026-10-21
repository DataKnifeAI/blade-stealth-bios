# coreboot port plan

> **Naming note:** early planning sometimes said “Skylake.” This board is **Ice Lake** (i7-1065G7). Skylake remains on mainline; Ice Lake was removed from master in [CL 72008](https://review.coreboot.org/c/coreboot/+/72008). The EmberROM fork targets **Ice Lake revive + this Blade board**, not a Skylake port.

## Development fork

| Item | Value |
|------|--------|
| Fork | [github.com/DataKnifeAI/coreboot](https://github.com/DataKnifeAI/coreboot) |
| Local clone | `/home/lee/Projects/coreboot` |
| Remotes | `origin` = DataKnifeAI/coreboot; `upstream` = https://review.coreboot.org/coreboot.git |
| Reference branch | [`emberrom/icelake-ref`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake-ref) — tip of upstream `4.19_branch` (**`79a11950acfc55e6f7a2e9c673991c1dafc59f91`**); Ice Lake SoC present |
| WIP branch | [`emberrom/icelake`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake) — `icelake-ref` + [CL 37565 PS16](https://review.coreboot.org/c/coreboot/+/37565) + build fixes (**`cf0b0137f2`**) |
| Upstream contributions | **Gerrit only** — [review.coreboot.org](https://review.coreboot.org/). Do not open GitHub PRs against upstream `coreboot/coreboot`. |

**Workflow:** board bring-up stays on the 4.19-era tree (`emberrom/icelake*`) where `src/soc/intel/icelake` still exists. When cold boot + basics are solid, rebase/port forward toward modern main (post–[CL 72008](https://review.coreboot.org/c/coreboot/+/72008) SoC drop) and propose clean changes via coreboot Gerrit. The GitHub fork is a WIP staging area, not an upstream PR channel.

Ice Lake SoC / CRB code left mainline in [CL 72008](https://review.coreboot.org/c/coreboot/+/72008) (post–4.19). Do not confuse with still-supported Skylake.

### Checkout recipe

```bash
git clone https://github.com/DataKnifeAI/coreboot.git
cd coreboot
git remote add upstream https://review.coreboot.org/coreboot.git
# Reference tree (SoC only, no EmberROM board commit):
git fetch origin emberrom/icelake-ref && git checkout emberrom/icelake-ref
# Board WIP (CL 37565 applied):
git fetch origin emberrom/icelake && git checkout emberrom/icelake
```

### CL 37565 apply status (2026-10-21)

| Item | Status |
|------|--------|
| Source | `git fetch upstream refs/changes/65/37565/16` → `43990910d8876d162a1fb101be4d99d3eeca66c1` |
| Author credit | Johanna Schander / Mimoja — `Signed-off-by: Johanna Schander <coreboot@mimoja.de>` preserved; `(cherry picked from …)` trailer kept |
| Result | **Clean cherry-pick** onto `emberrom/icelake-ref` (no conflicts). Adds `src/mainboard/razer/blade_stealth_icl/` (LY320) |
| Still missing (upstream CL notes) | ACPI/power/advanced init, EC (IT8320VG), graphics bring-up; GTX Max-Q SKU (03101) needs separate verification vs Mercury White prior art |

Do **not** treat this as a flashable port. BIOS-region smoke image builds (below); cold boot / EC / graphics still unproven on hardware.

### Build smoke status (2026-10-21)

| Item | Status |
|------|--------|
| Defconfig | `configs/config.razer_blade_stealth_icl` (SeaBIOS, no IFD/ME stitch) |
| Result | **`Built razer/blade_stealth_icl (LY320)`** — `build/coreboot.rom` **16 MiB** (SHA-256 `f423ffb8f26fa7181a1527dbcbe43013236b067706f80be337ad012333fed807`) |
| Payload | SeaBIOS (board/tree default for x86) |
| Image note | Built **without** IFD — do **not** flash the full chip; BIOS-region-only write would still need IFD/ME preserved |
| Commits | `3bf7b8cf72` host GCC 15+; `cf0b0137f2` board 4.19 adaptations (credit CL 37565 / Mimoja) |

```bash
cd /home/lee/Projects/coreboot
git checkout emberrom/icelake
# Blobs: see FSP / IFD sections below (local only)
make defconfig KBUILD_DEFCONFIG=configs/config.razer_blade_stealth_icl
# Host GCC 15+: build crossgcc with C17 wrappers if GMP configure fails (see below)
export PATH="$PWD/util/crossgcc/xgcc/bin:$PATH"
make -j"$(nproc)"
ls -la build/coreboot.rom   # do not flashrom -w
```

## Ice Lake FSP / microcode (4.19-era)

Board + SoC select `FSP_USE_REPO` + `ADD_FSP_BINARIES` + `FSP_FULL_FD`. Defaults in `src/soc/intel/icelake/Kconfig`:

| Blob | Path |
|------|------|
| Headers | `3rdparty/fsp/IceLakeFspBinPkg/Include` (`CONFIG_FSP_HEADER_PATH`) |
| Combined FD | `3rdparty/fsp/IceLakeFspBinPkg/Fsp.fd` (`CONFIG_FSP_FD_PATH`) |
| Split at build | `python 3rdparty/fsp/Tools/SplitFspBin.py` → `build/Fsp_{T,M,S}.fd` |

**Obtain FSP (local only — never commit):** relative submodule URL `../fsp.git` does **not** resolve on DataKnifeAI/github. Clone Intel FSP into the submodule path:

```bash
cd /home/lee/Projects/coreboot
rm -rf 3rdparty/fsp
git clone --filter=blob:none --sparse https://github.com/intel/FSP.git 3rdparty/fsp
cd 3rdparty/fsp
git sparse-checkout set IceLakeFspBinPkg Tools
# Prefer the coreboot-pinned SHA when present:
git checkout 6f2f17f3d3397cc2f00a644e218980bb33e06f66
```

Recorded smoke build used `Fsp.fd` SHA-256 `1069d03d4b9fd5a6091b3efd358c3000933fbe4c7e691ffdf0f18cf8ee2c5447`.

**Microcode:** SoC selects `MICROCODE_BLOB_UNDISCLOSED` → defconfig uses `CPU_MICROCODE_CBFS_NONE`. For a flashable image later, switch to external bins from `3rdparty/intel-microcode` (CPU id for i7-1065G7) — still local/gitignored.

**Also init for build:** `3rdparty/vboot` (pinned SHA in tree). Host needs `iasl`/`nasm` (via `make crossgcc-i386`, which also builds them) and a working host GCC.

**Host GCC 15/16 note:** GMP 6.2.1 in this crossgcc fails the “long long reliability” test under C23. Build toolchain with C17 wrappers, e.g. `PATH` entries that run `gcc -std=gnu17` / `g++ -std=gnu++17`, then `make crossgcc-i386 CPUS=$(nproc)`. Do **not** leave those wrappers on `PATH` for the coreboot host-tool build (use plain gcc + the `__nonstring` backport on `emberrom/icelake`).

## IFD / ME (full SPI stitch — not in smoke defconfig)

Extracted locally from the vendor dump (gitignored):

| Blob | Local path |
|------|------------|
| Descriptor | `emberrom/vendor/razer-blade-stealth-icl/ifd/descriptor.bin` and `coreboot/3rdparty/blobs/mainboard/razer/blade_stealth_icl/descriptor.bin` |
| ME | `…/me/me.bin` (same under blobs mainboard path) |

```bash
make -C util/ifdtool
./util/ifdtool/ifdtool -x dumps/blade-rz09-03101e72-spi-16m.bin
```

IFD layout on this unit: FD `0–0xfff`, ME `0x1000–0x5fffff`, BIOS `0x600000–0xffffff`; **no EC region** (GbE unused). Board Kconfig still selects `MAINBOARD_USES_IFD_EC_REGION` from CL 37565 — do not enable `HAVE_EC_BIN` until verified. Smoke defconfig leaves `HAVE_IFD_BIN` / `HAVE_ME_BIN` off.

## Prior art

| Work | Status | Link |
|------|--------|------|
| `mb/razer`: Blade Stealth Late 2019 [ICL] | Abandoned (2024) | https://review.coreboot.org/c/coreboot/+/37565 |
| Mimoja PoC / LinuxBoot notes | Experimental (2020) | Cold boot unreliable; EC must stay powered |
| Blade Stealth 2016 H2U (Kaby Lake) | Earlier merged reference | Different SoC + ITE8528E Super I/O |

CL 37565 claimed for Mercury White ICL: i7-1065G7, IT8320VG EC, LPDDR4, Titan Ridge, Realtek audio, Type-C switches. **GTX SKU (03101)** shares the Ice Lake platform class but needs its own verification (dGPU power rails, mux, ACPI) — checklist in [PREFLASH.md](PREFLASH.md) §6. Stock VBT located in SPI dump ([ANALYSIS.md](ANALYSIS.md) §3).

Libreboot does **not** support this board.

## Hard dependencies

1. **Intel FSP / blobs** — Ice Lake still needs proprietary FSP (and typically microcode); “fully libre” is not realistic on this SoC.
2. **ME region** — keep a working ME from the dump unless HAP/soft-disable is proven safe on this unit.
3. **ITE IT8320VG EC** — battery, lid, keys, thermal, USB-PD. Unsupported; reverse-engineering or binary EC reuse required.
4. **Recovery path** — external SPI before first write ([RECOVERY.md](RECOVERY.md)).

## Suggested port order

1. Full dump + IFD map + vendor BIOS extract  
2. Minimal board: memory init → payload → USB/NVMe  
3. Graphics (libgfxinit / FSP GOP) for internal eDP  
4. ACPI tables from `acpidump`, iteratively  
5. EC protocol (longest pole)  
6. dGPU / Optimus last  

## Success bar (owner)

See [GOALS.md](GOALS.md). Target is **feature parity with a proper coreboot laptop port** (P0 daily-driver hardware), not a one-shot payload PoC. GTX Optimus + Thunderbolt are P1 after suspend/EC/display work.

## This target’s role in EmberROM

Board-specific notes for the shared [port process](../../docs/process/port.md). Patches should aim at upstream coreboot (Gerrit) when ready. No redistributed vendor ROMs.
