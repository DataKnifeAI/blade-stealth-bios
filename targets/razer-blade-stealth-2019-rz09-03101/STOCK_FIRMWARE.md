# Stock firmware + CachyOS

Keep this laptop usable on **vendor AMI BIOS** while the EmberROM / coreboot port is unfinished. Shared process: [stock-enablement](../../docs/process/stock-enablement.md). Goals: [GOALS.md](GOALS.md).

## Known firmware on this unit

| Component | Version |
|-----------|---------|
| AMI Aptio Setup | 2.20.1275 |
| System BIOS | **1.05** (build 2020-10-06 14:00:26) |
| EC FW | **1.01** |
| MCU FW | **1.00.06.00** |
| IGFX GOP | 14.0.1039 |
| CPU microcode (setup) | 2E |
| Intel ME (fwupd) | **13.0.46.1718** |

Matches Razer’s public BIOS **v1.05** package for RZ09-03101 — no newer stock BIOS advertised for this SKU.

## Confirmed on this unit

| Issue | Notes |
|-------|--------|
| **Sleep / suspend broken** | Owner-confirmed (GUI / daily use). Lab `rtcwake` **deep** and **s2idle** both *complete* with RTC wake — see [ANALYSIS.md](ANALYSIS.md). |
| Deep resume AML | `ACPI Error: AE_NOT_EXIST` while running `\_WAK` (ties to `EC0.RTEC` / missing SystemCMOS `VRTC` handler) |
| Boot EC AML | `EC0.RTEC` / `EC0._REG` abort every boot (same `VRTC`) |
| GPU path | **nouveau** + **i915**; eDP on i915; lid quirk already `[open]` |
| Secure Boot | Off on reference unit ([INVENTORY.md](INVENTORY.md)) |
| OS | Ubuntu temporary; destination **CachyOS** |

### Stock workaround candidates (unproven for GUI)

```text
mem_sleep_default=s2idle
# optional still: button.lid_init_state=open  (already default quirk on this DMI)
# try iGPU-only: blacklist nouveau
```

## Known issue classes (Blade Stealth family)

| Issue | Notes |
|-------|--------|
| Lid / suspend loops | Historical `_LID` quirk; kernels may need `button.lid_init_state=open` or DMI quirk |
| NVRAM / MokList “Volume Full” | After fwupd DBX updates on some Stealth units |
| Locked Secure Boot UX | AMI Aptio V |
| CSM / legacy | Can blank the internal panel |
| Stale BIOS | Last public BIOS 1.05 |

## Suspend debugging checklist (stock)

Lab progress in [ANALYSIS.md](ANALYSIS.md). Still need **interactive** failure mode:

- [x] `rtcwake` deep + s2idle (both succeed with RTC)
- [x] Note `_WAK` / `VRTC` ACPI errors
- [x] Note nouveau+i915; lid quirk open
- [ ] Owner: describe GUI failure (blank panel / no wake / lid re-suspend loop)
- [ ] Try `mem_sleep_default=s2idle` for daily use
- [ ] Try blacklist nouveau (iGPU-only)
- [ ] Lid-close behavior with logind
- [ ] Retest on CachyOS

## Working notes

- [ ] Latest CachyOS ISO boot / install result
- [ ] Hybrid graphics under Wayland on CachyOS
- [ ] Thunderbolt / USB-C charge + display
- [ ] fwupd denylist (avoid huge DBX updates — NVRAM risk)
