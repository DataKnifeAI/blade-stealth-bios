# Stock firmware + CachyOS

Keep this laptop usable on **vendor AMI BIOS** while the EmberROM / coreboot port is unfinished. Shared process: [stock-enablement](../../docs/process/stock-enablement.md).

## Known firmware on this unit

| Component | Version |
|-----------|---------|
| AMI Aptio Setup | 2.20.1275 |
| System BIOS | **1.05** (build 2020-10-06 14:00:26) |
| EC FW | **1.01** |
| MCU FW | **1.00.06.00** |
| IGFX GOP | 14.0.1039 |
| CPU microcode (setup) | 2E |

Matches Razer’s public BIOS **v1.05** package for RZ09-03101 — no newer stock BIOS advertised for this SKU.

## Known issue classes (Blade Stealth family)

| Issue | Notes |
|-------|--------|
| Lid / suspend loops | Historical `_LID` quirk; modern kernels usually include DMI fix. Fallback: `button.lid_init_state=open` |
| NVRAM / MokList “Volume Full” | After fwupd DBX updates on some Stealth units; can block boot until CMOS clear |
| Locked Secure Boot UX | AMI Aptio V; limited key management compared to OEM “Setup Mode” docs |
| CSM / legacy | Enabling CSM can blank the internal panel until settings are restored blindly |
| Stale BIOS | Last public BIOS 1.05 — few modern UEFI knobs |

## Capture baseline (on the machine)

```bash
sudo dmidecode -t bios -t system
fwupdmgr get-devices || true
efibootmgr -v || true
cat /sys/class/tpm/tpm0/tpm_version_major 2>/dev/null
```

Document the exact CachyOS failure (ISO boot vs install vs day-2) in a GitHub issue and link it from [TASKS.md](../../TASKS.md) S1.

## Working notes

Fill in as reproduced on RZ09-03101E72:

- [ ] Latest CachyOS ISO boot result
- [ ] Secure Boot on/off requirements
- [ ] Hybrid graphics (iGPU / GTX 1650 Max-Q) behavior under Wayland
- [ ] Suspend / hibernate
- [ ] Thunderbolt / USB-C charge + display
