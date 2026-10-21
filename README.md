# EmberROM

![EmberROM — a SPI flash chip in charcoal ash with amber embers tracing open firmware along the pins](docs/assets/emberrom-hero.jpg)

**EmberROM** — keep the last glow of a vendor ROM, then forge open firmware from it.

Process and tooling to port **vendor laptop BIOS/UEFI** to open firmware ([coreboot](https://www.coreboot.org/) and related stacks), while keeping machines usable on modern Linux along the way. Board work lives under `targets/`; shared process docs live under `docs/process/`.

## First target

| Field | Value |
|-------|--------|
| Board | [Razer Blade Stealth 13 Late 2019](targets/razer-blade-stealth-2019-rz09-03101/) |
| SKU | RZ09-03101E72 |
| CPU | Ice Lake i7-1065G7 |
| Stock BIOS | AMI Aptio 2.20.1275 · System BIOS **1.05** · EC **1.01** |
| Goal OS | [CachyOS](https://cachyos.org/) on current kernels |

There is **no** flashable open BIOS yet. Stock-firmware enablement and coreboot research run in parallel — see [TASKS.md](TASKS.md).

## Process

```text
inventory → dump SPI → extract/analyze → keep usable (stock) → port (coreboot) → flash → recover
```

| Stage | Doc |
|-------|-----|
| Safety | [docs/process/safety.md](docs/process/safety.md) |
| Inventory | [docs/process/inventory.md](docs/process/inventory.md) |
| Dump | [docs/process/dump.md](docs/process/dump.md) |
| Extract | [docs/process/extract.md](docs/process/extract.md) |
| Stock enablement | [docs/process/stock-enablement.md](docs/process/stock-enablement.md) |
| Port | [docs/process/port.md](docs/process/port.md) |
| Flash & recover | [docs/process/flash-recover.md](docs/process/flash-recover.md) |
| Add a target | [docs/process/add-target.md](docs/process/add-target.md) |

## Layout

```text
emberrom/
  docs/process/     # board-agnostic workflow
  docs/assets/      # heroes, photos (no ROM binaries)
  targets/<board>/  # per-laptop notes, status, vendor links
  tools/            # shared helpers (later)
  vendor/           # local proprietary updaters (gitignored)
  dumps/            # local SPI dumps (gitignored)
```

## Principles

- **Freedom-respecting** — prefer open firmware and user-controlled boot paths when the silicon allows.
- **Recoverable** — no experimental write without a verified dump and an external flash plan.
- **No blob redistribution** — document hashes and download steps; keep ME/BIOS/EC images local.
- **Maintainable** — one shared process; targets carry only board-specific truth.

## Related prior art

- [coreboot](https://www.coreboot.org/) / [Libreboot](https://libreboot.org/) (supported boards only)
- Abandoned Ice Lake Stealth work: [coreboot CL 37565](https://review.coreboot.org/c/coreboot/+/37565)

## License

Apache License 2.0 — see [LICENSE](LICENSE).

coreboot patches contributed upstream remain under coreboot’s license (GPL-2.0). Vendor firmware stays proprietary and is not redistributed from this repository.

Maintained by [DataKnifeAI](https://github.com/DataKnifeAI).
