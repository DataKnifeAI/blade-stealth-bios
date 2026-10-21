# Recovery — RZ09-03101E72

Firmware work on a thin laptop without dual-BIOS is **high risk**. Assume an external SPI programmer before the first experimental write.

Dump layout, flashrom commands, and programmer notes: **[FLASH.md](FLASH.md)**.  
Live Razer / silicon facts: **[INVENTORY.md](INVENTORY.md)**.

Shared process: [flash-recover](../../docs/process/flash-recover.md) · [safety](../../docs/process/safety.md).

---

## Before any flash write

1. Dump the full ROM **twice**; hashes must match.  
2. Store dumps **offline** (not only on the laptop under test).  
3. Photograph SPI chip markings. Soft ID: Winbond **W25Q128.V** 16 MiB.  
4. Confirm **3.3 V** (not 5 V) on the programmer before clipping.  
5. Prefer matching the reference internal dump hash when possible:

```text
sha256: e6929ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
```

---

## Soft recovery (stock firmware still boots)

| Symptom | Try |
|---------|-----|
| NVRAM / MokList “Volume Full” | UEFI load defaults if available; else CMOS/RTC clear per service guides; avoid re-applying huge DBX / fwupd updates |
| Black panel after CSM | Blind restore to UEFI-only / CSM off (community notes for 2019 Stealth) |
| Bad Windows BIOS updater | Razer package recovery media if provided; else external SPI restore of known-good dump |
| Need stock BIOS again (OS/EFI works) | Official LY320 **BIOS v1.05** updater — [rzr.to/H1kYs](https://rzr.to/H1kYs) from [Answer 4566](https://mysupport.razer.com/app/answers/detail/a_id/4566) |

Reference unit notes: Secure Boot was **off**; UEFI dbx **20230501**; ME **13.0.46.1718** — do not flash ME **v12/v14** packages from Answer 4566 without confirming they match this major.

---

## Hard recovery (no POST)

1. External programmer (CH341A @ **3.3 V**, or Raspberry Pi `linux_spi`) + SOIC-8 clip.  
2. Write the **verified original dump** back (full chip or layout-limited regions).  
3. Verify readback; only then retry experimental images.  
4. Internal host flashrom **cannot** freely rewrite ME/IFD (`FLOCKDN`, region locks) — external path is authoritative for brick recovery.

Clip orientation, footprint photos, and ISP vs desolder steps: document under this target or `docs/assets/` after chassis open (**no ROM binaries**).

---

## Quick command cheatsheet

```bash
# Internal read (reference unit; laptop force required)
sudo flashrom -p internal:laptop=force_I_want_a_brick -r dump.bin

# Or MTD
sudo dd if=/dev/mtd0ro of=dump.bin bs=1M

# External CH341A
sudo flashrom -p ch341a_spi -c "W25Q128.V" -r dump.bin

# Always dump twice and compare
sha256sum dump1.bin dump2.bin
```

Details: [FLASH.md](FLASH.md).
