# Set Up Info

### Key Links
- Raspberry Pi Install to SD Card: https://www.raspberrypi.org/documentation/installation/installing-images/mac.md
- Wifi Connection: https://styxit.com/2017/03/14/headless-raspberry-setup.html

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
- Blah Blah Blah will continue this later

2. Set up Wifi on the Raspberry Pi so you can SSH

- Disconnect the SD card and plug back in - this will re-register the drive
- cd to the boot folder of the SD drive (this will appear in a boot folder on the macOS)
```bash
cd /Volumes/boot
```
- add an empty ssh file
```bash
touch ssd
```

