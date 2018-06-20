# Set Up Info

### Key Links
- Raspberry Pi Install to SD Card: https://www.raspberrypi.org/documentation/installation/installing-images/mac.md

### Mac OS Install:
---
1. Install the Operating System on an SD Card

Let's use the command line to do this install:

- Plug in SD Card
- Run the follwoing Command:

```bash
diskutil list
```
- Find the disk from the list (It should be something like disk2 not disk2s1)
- Unmount the disk

```bash
diskutil unmountDisk /dev/disk<disk# from diskutil>
```
