# Extract

Turn dumps and vendor updaters into analyzable pieces — still local, still not committed.

## From SPI dump

- Parse Intel Flash Descriptor (IFD): BIOS / ME / Gigabit / EC / platform data regions as present
- Note unlock / HAP / write-protect state if tools report it
- Keep a pristine full image for restore

## From vendor updaters

- Download official BIOS/ME/EC packages into local `vendor/`
- Record SHA-256 in the target’s `VENDOR_ASSETS.md`
- Extract capsules / PEI-DXE volumes for comparison against the SPI BIOS region

## Do not extract-for-redistribute

ME, EC, and full BIOS images stay private. Public docs should list **versions, hashes, and URLs**, not blobs.
