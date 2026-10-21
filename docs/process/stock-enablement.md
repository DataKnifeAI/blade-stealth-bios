# Stock enablement

Keep the laptop usable on **vendor firmware** while the open port is unfinished — especially for current distros (CachyOS, etc.).

## Typical work

- Document why the latest distro fails (ISO boot, Secure Boot, NVRAM full, GPU, suspend)
- fwupd / DBX hygiene on constrained NVRAM platforms
- Kernel cmdline and quirks still required on modern kernels
- Hybrid graphics, Thunderbolt, power / lid behavior

Board-specific notes: `targets/<board>/STOCK_FIRMWARE.md`.
