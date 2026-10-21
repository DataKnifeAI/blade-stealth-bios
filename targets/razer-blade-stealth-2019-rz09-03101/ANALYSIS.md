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

## 3. ACPI / EC (from `extract/acpi/DSDT.dsl`)

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

## 4. Open analysis TODOs

- [ ] UEFI volume map inside BIOS region (VBT, DXEs) — needs UEFITool/UEFIExtract  
- [ ] ME HAP / manufacturing mode bits from FD/ME (soft-disable research later)  
- [ ] Trace `MLBX` 0x300 mailbox vs battery/PD  
- [ ] Compare LY320 BIOS 1.05 updater capsule to SPI BIOS region (when downloaded)  
- [ ] `inteltool` GPIO dump on unit  
