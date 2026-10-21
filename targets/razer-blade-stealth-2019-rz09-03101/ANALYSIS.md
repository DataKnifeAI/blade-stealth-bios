# Analysis notes — RZ09-03101E72

Started 2026-10-21 on the reference unit (Ubuntu 26.04 temporary) + local SPI/ACPI extracts. Binaries stay gitignored under `dumps/` and `extract/`.

## 1. Suspend characterization (stock AMI)

Host at test: Ubuntu 26.04.1 · kernel `7.0.0-30-generic` · Secure Boot off · **nouveau** + **i915** loaded · lid quirk `button.lid_init_state=[open]`.

| Check | Result |
|-------|--------|
| `/sys/power/mem_sleep` | `s2idle [deep]` (deep default) |
| Lid device | `/proc/acpi/button/lid/LID0/state` = open |
| logind `HandleLidSwitch` | `suspend` |
| Suspend stats before tests | success=0 fail=0 (no prior attempts this boot) |

### Controlled `rtcwake` tests

| Mode | Command | Kernel result | Notes |
|------|---------|---------------|-------|
| **S3 deep** | `rtcwake -m mem -s 45` with `mem_sleep=deep` | **success** (stats 1/0) | Entered S3; resumed via RTC |
| **s2idle** | `rtcwake -m mem -s 30` with `mem_sleep=s2idle` | **success** (stats 2/0) | Resumed via RTC |

So “sleep is broken” is **not** “kernel cannot enter/leave mem sleep at all” under RTC wake. User-facing breakage is likely **resume quality** (panel / GPU / lid loop / desktop), not hard suspend entry failure.

### ACPI errors tied to sleep

**Boot (every boot observed):**

```text
ACPI Error: No handler for Region [VRTC] ... [SystemCMOS]
ACPI Error: Aborting method \_SB.PCI0.LPCB.EC0.RTEC ...
ACPI Error: Aborting method \_SB.PCI0.LPCB.EC0._REG ...
```

**On deep (S3) resume:**

```text
ACPI Error: AE_NOT_EXIST, While executing method \_WAK
```

s2idle resume did **not** log the `_WAK` AE_NOT_EXIST in the short journal slice.

`_WAK` → `RWAK` → `EC0.RTEC()` reads CMOS via OperationRegion `VRTC` / SystemCMOS. Missing CMOS handler → RTEC/`_REG` fail at boot and `_WAK` fails after S3. That is a strong stock-firmware / AML defect on this platform under Linux.

### Graphics after deep resume (SSH view)

| Device | Role | runtime_status after deep |
|--------|------|-----------------------------|
| card1 `8086:8a52` i915 | eDP (connected) | active |
| card0 `10de:1f91` nouveau | GTX 1650 Max-Q | suspended |

eDP still `connected`. GUI/blank-screen behavior needs a local confirmation (not visible over SSH).

### Next suspend experiments (owner / local)

- [ ] Lid close: does it re-suspend loop? (`logind` will suspend on lid)
- [ ] Desktop suspend (GNOME/KDE) without RTC — panel come back?
- [ ] Blacklist nouveau / use iGPU-only; retest deep
- [ ] Force `mem_sleep_default=s2idle` on cmdline; daily-driver trial
- [ ] Compare on CachyOS once installed

---

## 2. IFD / SPI extract

Tool: [`tools/ifd_split.py`](../../tools/ifd_split.py)  
Source: `dumps/blade-rz09-03101e72-spi-16m.bin`  
Full image SHA-256: `e6929ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1`

| Region | Range | Size | SHA-256 (region) | Markers |
|--------|-------|------|------------------|---------|
| FD | `0x000000`–`0x000fff` | 4 KiB | `1b51b551…717137` | IFD `0x0FF0A55A` |
| ME | `0x001000`–`0x5fffff` | ~6.0 MiB | `90a73b66…f1f8a3` | `$FPT` `$MN2` `$CPD` |
| BIOS | `0x600000`–`0xffffff` | 10 MiB | `559d00f2…05b57c` | `_FVH` UEFI volumes |
| GbE / PD / EC (IFD) | — | unused | — | **No IFD EC region** |

EC firmware is **not** a separate IFD region on this descriptor (typical for ITE EC with own flash or code inside BIOS/EC mailbox). Confirm IT8320VG via EC protocol / physical silk, not IFD slot 8.

Local split output (gitignored): `extract/ifd/`.

---

## 3. UEFI volumes / VBT (BIOS region)

Tools available on analysis host: `python3`, `strings` (no `binwalk` / UEFIExtract installed).  
Source region: `extract/ifd/01_bios_00600000-00ffffff.bin`  
BIOS region SHA-256: `559d00f2c1359b88cce51aeb252f35b7e470ccfdeaf4c2f3073450131505b57c`  
SPI base for BIOS: **`0x00600000`**.

### Firmware volumes (`_FVH`)

Ten length-aligned volumes (FFS2 `8c8ce578-8a3d-4f1c-9935-896185c32dd3`). Hashes truncated in table; full digests recorded locally if needed — **no volume binaries in git**.

| # | SPI offset | BIOS offset | Size | SHA-256 (prefix) |
|---|------------|-------------|------|------------------|
| 0 | `0x00600000` | `0x00000000` | `0x30000` | `f06d104fada30d6d…` |
| 1 | `0x00670000` | `0x00070000` | `0x4a0000` | `325e8334fc33aaf6…` |
| 2 | `0x00b10000` | `0x00510000` | `0x200000` | `82d56121392102e1…` |
| 3 | `0x00d10000` | `0x00710000` | `0xd0000` | `31a5c7c56e5622a2…` |
| 4 | `0x00de0000` | `0x007e0000` | `0xa0000` | `4f5bf9404c9f2f91…` |
| 5 | `0x00e80000` | `0x00880000` | `0x8d000` | `deeea1857505b143…` |
| 6 | `0x00e80070` | `0x00880070` | `0x5a000` | `c5349ae2bdec6444…` (nested) |
| 7 | `0x00f0d000` | `0x0090d000` | `0x6000` | `7983aa5c1caffe34…` |
| 8 | `0x00f13000` | `0x00913000` | `0x6d000` | `47874a7d04d0c157…` |
| 9 | `0x00f80000` | `0x00980000` | `0x80000` | `bd86b743431762d5…` |

FV **#4** (`0x00de0000`, 640 KiB) holds the VBT FREEFORM file among ~33 FFS entries (mostly PEIMs).

### Intel VBT (`$VBT ICELAKE`)

| Field | Value |
|-------|--------|
| Signature | `$VBT ICELAKE` (20-byte padded) |
| SPI offset | **`0x00e2c484`** |
| BIOS-region offset | `0x0082c484` |
| VBT version | 100 |
| Header size | 48 |
| **VBT size** | **6380** bytes (`0x18ec`) |
| Checksum byte | `0xfd` |
| BDB | `BIOS_DATA_BLOCK` @ +48; BDB version **230**; `bdb_size` 6331 |
| **VBT SHA-256** | `e64e219bc94ff587e7a45b5512d7a8f836f66bc266bd3df663c7d83fbf47d14d` |

Containing FFS (type **FREEFORM** `0x02`):

| Field | Value |
|-------|--------|
| GUID | `dcb132e7-27d2-40ff-9c3f-9f280b3d10f5` |
| SPI / BIOS | `0x00e2c468` / `0x0082c468` |
| FFS size | `0x1a1c` (6684) |
| **FFS SHA-256** | `454ac7c0d619134604ece2b7c1000bb2960c3faa3c9655925c4194b09bb42042` |
| Parent FV SHA-256 | `4f5bf9404c9f2f91f4c44632835a91e1bb58835a43951d5b8a1a523faff0a1b0` |

Same GUID also appears at SPI `0x00f9e3e4` inside FV #9 — looks like a **variable/default store reference** (`BBRR****` UTF-16), not a second VBT payload.

### GOP-related notes

- Aptio Main reports **IGFX GOP Version 14.0.1039** (runtime inventory) — that version string was **not** found as ASCII in the BIOS region.
- No discrete NVIDIA VBIOS / `ATOMBIOS` / `NVIDIA` markers in the SPI BIOS region (expected for Optimus: dGPU ROM is on the GPU, not the board flash).
- A bare `PCIR` hit at `0x00f1fa71` is a **false positive** inside code (not a PCI option ROM header).
- Without UEFIExtract/binwalk, GOP DXE module names were not fully enumerated; next pass: UEFITool on the BIOS region (local only) to name the Intel GOP driver FFS.

coreboot bring-up should extract/reuse this VBT (or regenerate via inteltool + panel EDID) for eDP — do **not** borrow a Mercury White VBT blindly.

---

## 4. ACPI / EC (from `extract/acpi/DSDT.dsl`)

| Item | Finding |
|------|---------|
| Embedded controller | `\_SB.PCI0.LPCB.EC0` · `PNP0C09` · IO **0x62/0x66** · GPE **0x6E** |
| EC memory | `OperationRegion (ERAM, EmbeddedControl, 0x00, 0xFF)` |
| Stub lid | `LID0` with `_STA=0` (disabled) earlier in tree |
| Real lid | `EC0.LID0` · `_STA=0x0F` · `_LID` returns external `LIDS` |
| S3 object | `_S3` package present (`0x05,…`) — platform advertises S3 |
| Prepare/wake | `_PTS` → `RPTS` / `SPTS` / `NPTS`; `_WAK` → `NWAK` / `SWAK` / `RWAK` |
| Wake EC hook | `RWAK` calls `EC0.RTEC()` (RTC→EC sync via broken `VRTC`) |
| Extra EC IO | `MLBX` @ IO **0x300–0x303** (mailbox-style; useful for reverse-engineering) |

### coreboot implications

1. Must implement EC0 + lid/`LIDS` correctly or suspend/lid will stay broken under open firmware too.  
2. Reimplement or avoid AMI `VRTC`/RTEC path — do not depend on SystemCMOS region the way stock AML does.  
3. No IFD EC slice to “keep as blob region”; EC is a separate bring-up problem (ITE).  
4. Keep ME region from dump for first boots; BIOS region replaced by coreboot+payload.

---

### Optimus / dGPU ACPI (GTX SKU)

Stock tables under `extract/acpi/` (local):

| Table | OEM / creator | Relevance |
|-------|---------------|-----------|
| SSDT11 | `HgRpSsdt` / HgRef | `HGON` / `HGOF` |
| SSDT13 | `Opt1Tabl` / OptRf1 | Optimus: `RP09.PEGP`, `NGC6`, `_ON` / related |

DSDT also declares `PEG0`–`PEG3` / `GFX0`. Mercury White (CL 37565 prior art) should **not** be assumed to share these power paths — verify GPIOs/rails before enabling dGPU in coreboot ([PREFLASH.md](PREFLASH.md) §6).

---

## 5. Open analysis TODOs

- [x] Locate VBT in BIOS region (offsets + hashes above)  
- [ ] UEFITool/UEFIExtract full DXE map (name Intel GOP driver FFS)  
- [ ] Decompile SSDT11/13; map HGON/HGOF pins vs CL 37565 `gpio.h`  
- [ ] ME HAP / manufacturing mode bits from FD/ME (soft-disable research later)  
- [ ] Trace `MLBX` 0x300 mailbox vs battery/PD  
- [ ] Compare LY320 BIOS 1.05 updater capsule to SPI BIOS region (when downloaded)  
- [ ] `inteltool` GPIO dump on unit  
