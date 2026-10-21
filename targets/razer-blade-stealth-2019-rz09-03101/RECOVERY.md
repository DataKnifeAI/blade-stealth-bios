# Recovery

Firmware work on a thin laptop without a documented dual-BIOS is **high risk**. Assume you need an external SPI programmer before the first experimental write.

## Before any flash write

1. Dump the full ROM twice; confirm identical hashes.  
2. Store dumps offline (encrypted backup OK); do not rely only on the laptop disk.  
3. Photograph SPI chip markings (vendor, capacity).  
4. Confirm 1.8 V vs 3.3 V flash before attaching a clip.

## Soft recovery (stock firmware still boots)

| Symptom | Try |
|---------|-----|
| NVRAM / MokList “Volume Full” | UEFI defaults if available; else remove CMOS/RTC battery per service guides; avoid re-applying huge DBX updates |
| Black panel after CSM | Blind key sequence to restore UEFI-only / CSM off (community notes exist for 2019 Stealth) |
| Bad Windows BIOS updater | Bootable recovery media from Razer package if provided; else external flash restore |

## Hard recovery (no POST)

1. External programmer (e.g. CH341A with correct voltage, or a known-good SOIC clip setup).  
2. Write the **verified original dump** back.  
3. Only then retry partial region writes.

Exact chip footprint, clip orientation, and ISP vs desolder steps are **TBD** after opening this RZ09-03101E72 unit — document with photos under this target or `docs/assets/` (no ROM binaries).

Shared process: [flash-recover](../../docs/process/flash-recover.md) · [safety](../../docs/process/safety.md).

## Razer official updater

The BIOS updater on [Answer 4566](https://mysupport.razer.com/app/answers/detail/a_id/4566) is for returning to vendor firmware when the machine still runs an OS or EFI shell capable of running the updater—not a substitute for a SPI backup once coreboot experiments begin.
