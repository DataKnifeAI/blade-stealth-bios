# coreboot port plan

> **Naming note:** early planning sometimes said “Skylake.” This board is **Ice Lake** (i7-1065G7). Skylake remains on mainline; Ice Lake was removed from master in [CL 72008](https://review.coreboot.org/c/coreboot/+/72008). The EmberROM fork targets **Ice Lake revive + this Blade board**, not a Skylake port.

## Development fork

| Item | Value |
|------|--------|
| Fork | [github.com/DataKnifeAI/coreboot](https://github.com/DataKnifeAI/coreboot) |
| Local clone | `/home/lee/Projects/coreboot` |
| Remotes | `origin` = DataKnifeAI/coreboot; `upstream` = https://review.coreboot.org/coreboot.git |
| Reference branch | [`emberrom/icelake-ref`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake-ref) — tip of upstream `4.19_branch` (**`79a11950acfc55e6f7a2e9c673991c1dafc59f91`**); Ice Lake SoC present |
| WIP branch | [`emberrom/icelake`](https://github.com/DataKnifeAI/coreboot/tree/emberrom/icelake) — `icelake-ref` + cherry-picked [CL 37565 PS16](https://review.coreboot.org/c/coreboot/+/37565) (**`386d05a1f8f27b7dcaaba5f763bca1e5c2e4e5bc`**) |
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

Do **not** treat this as a flashable port. Next work is FSP/blob wiring, `make menuconfig` board select smoke-test, then memory-init / payload bring-up on hardware with external recovery ready.

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
