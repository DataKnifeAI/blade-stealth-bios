# coreboot port plan

## Prior art

| Work | Status | Link |
|------|--------|------|
| `mb/razer`: Blade Stealth Late 2019 [ICL] | Abandoned (2024) | https://review.coreboot.org/c/coreboot/+/37565 |
| Mimoja PoC / LinuxBoot notes | Experimental (2020) | Cold boot unreliable; EC must stay powered |
| Blade Stealth 2016 H2U (Kaby Lake) | Earlier merged reference | Different SoC + ITE8528E Super I/O |

CL 37565 claimed for Mercury White ICL: i7-1065G7, IT8320VG EC, LPDDR4, Titan Ridge, Realtek audio, Type-C switches. **GTX SKU (03101)** shares the Ice Lake platform class but needs its own verification (dGPU power rails, mux, ACPI).

Libreboot does **not** support this board.

## Hard dependencies

1. **Intel FSP / blobs** — Ice Lake still needs proprietary FSP (and typically microcode); “fully libre” is not realistic on this SoC.
2. **ME region** — keep a working ME from the dump unless HAP/soft-disable is proven safe on this unit.
3. **ITE IT8320VG EC** — battery, lid, keys, thermal, USB-PD. Unsupported; reverse-engineering or binary EC reuse required.
4. **Recovery path** — external SPI before first write ([RECOVERY.md](RECOVERY.md)).

## Suggested port order

1. Full dump + IFD map + vendor BIOS extract  
2. Minimal board: memory init → payload → USB/NVMe  
3. Graphics (libgfxinit / FSP GOP) for internal eDP  
4. ACPI tables from `acpidump`, iteratively  
5. EC protocol (longest pole)  
6. dGPU / Optimus last  

## Success bar (owner)

See [GOALS.md](GOALS.md). Target is **feature parity with a proper coreboot laptop port** (P0 daily-driver hardware), not a one-shot payload PoC. GTX Optimus + Thunderbolt are P1 after suspend/EC/display work.

## This target’s role in EmberROM

Board-specific notes for the shared [port process](../../docs/process/port.md). Patches should aim at upstream coreboot when ready. No redistributed vendor ROMs.
