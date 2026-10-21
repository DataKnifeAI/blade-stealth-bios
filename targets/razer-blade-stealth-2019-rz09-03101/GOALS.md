# Goals — RZ09-03101E72

Owner decisions (2026-10-21). Update when scope changes.

## OS

| Item | Decision |
|------|----------|
| Target distro | **CachyOS** (current kernels) |
| Ubuntu on the reference unit | **Temporary** — inventory / dump host only, not the end state |

## Stock-firmware pain (today)

| Issue | Status |
|-------|--------|
| **Sleep / suspend broken** | Confirmed on this unit (stock AMI). Primary “keep usable” bug while coreboot is unfinished. |
| Other CachyOS blockers | TBD once CachyOS is reinstalled / dual-tested |

Suspend workarounds to try on stock (document results in [STOCK_FIRMWARE.md](STOCK_FIRMWARE.md)): `button.lid_init_state=open`, modern kernel DMI quirks, s2idle vs deep, NVIDIA/nouveau runtime PM.

## Flash / risk

| Item | Decision |
|------|----------|
| External SPI programmer | **Will buy** (3.3 V-capable, SOIC-8 clip for W25Q128.V) |
| Writes | Only after external dump matches internal SHA-256 `e6929ca0…` (see [FLASH.md](FLASH.md)) |

## Open-firmware success bar

**Aim: feature parity with a proper coreboot laptop port** — not a minimal “boots payload once” PoC.

| Tier | Features | Priority |
|------|----------|----------|
| **P0 — daily driver** | Cold boot, eDP, keyboard, touchpad, NVMe, USB, battery %, charging, lid, suspend/resume, audio, Wi‑Fi/BT, thermal/fans | Required |
| **P1 — parity stretch** | GTX 1650 Max-Q (Optimus), Thunderbolt 3 / USB-C DP + PD behavior matching stock usefulness | After P0 |
| **P2 — research** | ME neutralize / HAP if safe; maximize open code vs FSP blobs | Opportunistic |

Reality check: Ice Lake still needs **FSP + a working ME region** for a usable port. “Feature parity” means **hardware capability parity with stock via coreboot**, not zero blobs or Libreboot inclusion.

Port plan: [COREBOOT.md](COREBOOT.md). Tasks: [../../TASKS.md](../../TASKS.md).
