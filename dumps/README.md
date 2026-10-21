# dumps/ (local only)

Full SPI ROM dumps live here. Contents are **gitignored** — never commit firmware images.

## This workstation (pulled from blade via SSH)

| File | Notes |
|------|--------|
| `blade-rz09-03101e72-spi-16m.bin` | Canonical 16 MiB internal dump (Winbond W25Q128.V) |
| `SHA256SUMS` | Hashes from the Blade (lists duplicate reads too) |
| `README.txt` | Dump notes from the Blade |
| `logs/` | flashrom internal read logs |

```text
sha256: e6929ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
size:   16777216
```

Verify:

```bash
sha256sum blade-rz09-03101e72-spi-16m.bin
# expect e6929ca00f6ef95d70a6340f986bd5a55968166adf70f602ee92d7be1d09fde1
```

ACPI extracts: `../extract/acpi/` (also gitignored).

Board flash map: [../targets/razer-blade-stealth-2019-rz09-03101/FLASH.md](../targets/razer-blade-stealth-2019-rz09-03101/FLASH.md).  
Process: [../docs/process/dump.md](../docs/process/dump.md).
