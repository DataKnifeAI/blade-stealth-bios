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
| **Sleep / suspend broken** | Owner-confirmed under current temporary Ubuntu. Primary stock-firmware blocker for daily use / CachyOS. |
| Secure Boot | Off on reference unit ([INVENTORY.md](INVENTORY.md)) |
| OS | Ubuntu temporary; destination **CachyOS** |

## Known issue classes (Blade Stealth family)

| Issue | Notes |
|-------|--------|
| Lid / suspend loops | Historical `_LID` quirk; kernels may need `button.lid_init_state=open` or DMI quirk |
| NVRAM / MokList “Volume Full” | After fwupd DBX updates on some Stealth units |
| Locked Secure Boot UX | AMI Aptio V |
| CSM / legacy | Can blank the internal panel |
| Stale BIOS | Last public BIOS 1.05 |

## Suspend debugging checklist (stock)

Reproduce and record on Ubuntu first, then CachyOS:

```bash
# How does it fail? no wake / instant re-suspend / black screen / lid loop?
journalctl -b -p warning..alert | rg -i 'suspend|resume|lid|nvidia|i915|acpi'
cat /sys/power/mem_sleep
# try:
#   echo s2idle | sudo tee /sys/power/mem_sleep
# cmdline candidates:
#   button.lid_init_state=open
#   mem_sleep_default=s2idle
#   nvidia path: proprietary vs nouveau — note which is loaded
```

- [ ] Failure mode written down (no wake vs re-suspend loop vs blank panel)
- [ ] `mem_sleep` / s2idle vs deep tested
- [ ] `button.lid_init_state=open` tested
- [ ] iGPU-only vs hybrid (nouveau / NVIDIA) noted
- [ ] Same tests after CachyOS install

## Working notes

- [ ] Latest CachyOS ISO boot / install result
- [ ] Hybrid graphics under Wayland on CachyOS
- [ ] Thunderbolt / USB-C charge + display
- [ ] fwupd denylist (avoid huge DBX updates — NVRAM risk)
