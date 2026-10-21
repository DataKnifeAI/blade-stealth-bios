# Inventory

Capture what the machine *is* before changing firmware.

## From firmware setup (UEFI/BIOS)

Record (omit serial numbers from public docs):

- Product name, SKU, board / product version
- System BIOS version + build date
- EC / MCU versions if shown
- CPU model, microcode revision, iGPU / GOP strings
- Setup utility vendor (AMI, Insyde, Phoenix, …) and version
- Tabs that matter later: Security (Secure Boot), Boot (CSM), ME/TB if exposed

## From a booted OS

```bash
sudo dmidecode -t bios -t system -t baseboard
cat /sys/class/dmi/id/product_name /sys/class/dmi/id/product_sku /sys/class/dmi/id/bios_version
fwupdmgr get-devices || true
efibootmgr -v || true
lspci -nn
```

Store results in the target’s `HARDWARE.md`.
