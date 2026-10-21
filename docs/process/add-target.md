# Add a target

1. Create `targets/<vendor>-<product>-<sku-or-year>/`
2. Add at least: `README.md`, `HARDWARE.md`, `VENDOR_ASSETS.md`, `STOCK_FIRMWARE.md`, `COREBOOT.md`, `RECOVERY.md`
3. Link the target from the top-level README and TASKS
4. Follow [inventory](inventory.md) → [dump](dump.md) before any write experiments
5. Keep proprietary files in root `vendor/` / `dumps/` (gitignored), referenced by hash from the target docs
