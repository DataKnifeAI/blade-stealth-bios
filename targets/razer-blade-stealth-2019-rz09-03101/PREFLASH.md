# Pre-flash gate — RZ09-03101E72

Ordered **go/no-go** checklist before any SPI **write** (coreboot or restore).  
This SKU is **GTX 1650 Max-Q** (not Mercury White iGPU-only). Prior art [CL 37565](https://review.coreboot.org/c/coreboot/+/37565) is Mercury White — treat as a starting board skeleton only.

**Do not flash** until every gate below is checked or explicitly waived with reason.  
Related: [FLASH.md](FLASH.md) · [RECOVERY.md](RECOVERY.md) · [COREBOOT.md](COREBOOT.md) · [ANALYSIS.md](ANALYSIS.md) · [safety](../../docs/process/safety.md).

---

## Status legend

| Mark | Meaning |
|------|---------|
| `[x]` | Done on reference unit / docs |
| `[~]` | In progress / partial |
| `[ ]` | Open — **blocks write** unless waived |

---

## Ordered gates

### 1. Successful coreboot build

- [x] `emberrom/icelake` builds `mb/razer/blade_stealth_icl` (SeaBIOS + FSP + microcode)
- [x] Image size **16777216**; BIOS region IFD `0x600000–0xffffff` (~10 MiB)
- [x] No flash of intermediate/broken images “just to try”

**Today:** stitched ROM built locally — SHA-256 `3debd24dee9a2479b39802d1a789c578cea0b364f9d5ed5ac690438d417ec0f0` (`out/blade_stealth_icl-stitched-16m.rom`). Still **not** flash-ready (gates 3–7).

### 2. Image stitch plan (FD + ME + CBFS/BIOS)

Documented plan before composing a write image:

| Piece | Source | Notes |
|-------|--------|--------|
| Flash Descriptor | Vendor dump FD region | Stock IFD / locks preserved (`DO_NOT_TOUCH_DESCRIPTOR_REGION`) |
| ME | Vendor dump ME region | ME **13.0.46.1718** region SHA `90a73b66…` |
| BIOS / CBFS | coreboot build output | Stitched into BIOS region by ifdtool during `make` |

- [x] Stitch recipe: defconfig `HAVE_IFD_BIN`/`HAVE_ME_BIN` + `util/scripts/build-razer-blade-stealth-icl.sh` ([COREBOOT.md](COREBOOT.md))
- [x] Dry-run: stitched size **16777216**; FD/ME SHAs match dump; `ifdtool -t` exit 0
- [x] Plan prefers **BIOS-region-only** external write first; full-chip OK when FD+ME in image match dump (they do)

IFD map and split tool: [FLASH.md](FLASH.md) · [`tools/ifd_split.py`](../../tools/ifd_split.py) · local `extract/ifd/`.

### 3. External SPI dump matches internal SHA

Reference internal dump (authoritative hash):

```text
sha256: e6929ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
size:   16777216
```

- [x] Internal dump captured (MTD + flashrom); hash recorded
- [ ] External CH341A / Pi dump **twice**; both match each other
- [ ] External SHA-256 **equals** `e6929ca0…` (full 64 hex)
- [ ] Offline copy of known-good dump stored off the laptop under test
- [ ] Clip / chip photos filed (markings, pin‑1) — no binaries in git

### 4. Programmer 3.3 V + clip verified

- [ ] Programmer is **3.3 V** class (CH341A v1.6+ with voltage switch, or Pi SPI) — **not 5 V**
- [ ] SOIC-8 clip + 25-series adapter; pin‑1 (red) aligned to chip pin‑1
- [ ] Probe OK: `flashrom -p … -c "W25Q128.V"` identifies Winbond W25Q128.V
- [ ] Laptop fully off; AC unplugged; battery disconnected if practical

### 5. Restore test plan (write original dump back)

Prove recovery **before** any experimental coreboot write:

- [ ] Procedure written: external write of known-good `e6929ca0…` image → verify readback SHA
- [ ] Optional: practice restore once while stock firmware still boots (high confidence)
- [ ] Soft path still available: Razer LY320 BIOS **1.05** updater ([FLASH.md](FLASH.md)) — does **not** replace full SPI restore

### 6. GTX 03101 vs Mercury White (CL 37565) deltas

Short checklist — must be reviewed before first experimental flash (even iGPU-only bring-up can poke wrong GPIOs/rails):

| Check | Why | Status |
|-------|-----|--------|
| dGPU present `10de:1f91` @ PCI `57:00.0` | Mercury White has no GTX | [x] Verified live |
| Optimus ACPI (`Opt1Tabl` / `HgRpSsdt`) | Power on/off / GC6 | [~] SSDT11/13 present (`HGON`/`HGOF`/`NGC6` on `RP09.PEGP`); full GPIO/rail map TBD |
| dGPU power / enable GPIOs vs CL 37565 empty `gpio.h` | Wrong drive → rail damage or brick-feel hang | [ ] Not verified |
| PCIe RP / CLKREQ for dGPU vs Mercury White `devicetree.cb` | CL enables many RPs generically; confirm GTX path | [ ] Not verified |
| eDP VBT from **this** dump (not another SKU) | Panel/timing | [x] Located — see [ANALYSIS.md](ANALYSIS.md) |
| First flash scope | Prefer **iGPU + keep dGPU off/safe**; Optimus is P1 | [ ] Policy agreed at signoff |

### 7. Go / no-go signoff

Fill at the moment of first write attempt:

| Field | Value |
|-------|--------|
| Date | |
| Operator | |
| Image to write (path + SHA-256) | |
| Stitch recipe ref | |
| External dump SHA (must be `e6929ca0…`) | |
| Restore test | `[ ]` practiced / `[ ]` procedure-only waiver |
| GTX delta review | `[ ]` done |
| **Decision** | **GO** / **NO-GO** |
| Notes / waivers | |

**NO-GO** if any of: build unverified, stitch undefined, external dump mismatch, 5 V programmer, no restore plan, GTX rail/GPIO unknowns waived without risk acceptance.

---

## Quick “still open” summary

| Gate | State |
|------|-------|
| 1 Build | **Done** (stitched 16 MiB locally) |
| 2 Stitch plan | **Done** (IFD+ME+CBFS; BIOS-region-first) |
| 3 External dump = internal SHA | Open (internal done) |
| 4 3.3 V programmer + clip | Open (hardware incoming) |
| 5 Restore test | Open |
| 6 GTX vs Mercury White | Partial (presence + Optimus SSDTs; rails/GPIO open) |
| 7 Signoff | Not started |

**STOP:** no `flashrom -w` / external write until signoff is **GO**.
