# Using gr-dab with USRP B210

## Basic Commands

### 1. Scan for DAB Channels (Info Command)

This command scans for available DAB channels at a specific frequency:

```bash
cd /home/haaken/Nedlastinger/gr-dab/build
export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache
python3 apps/grdab.exe info --freq 222.064
```

**Parameters:**
- `--freq 222.064` - Frequency in MHz (222.064 MHz = DAB Band III channel 11B)

**What it does:**
- Connects to USRP B210
- Tunes to the specified frequency
- Scans for DAB channels
- Lists available stations with their parameters

**Expected output:**
After 30-60 seconds, you should see a list like:
```
Channels:
BAYERN 1 Nby.Opf: (address: 304, subch_size: 64, protect_level: 1, bit_rate: 64, classic: 0)
PULS: (address: 320, subch_size: 80, protect_level: 1, bit_rate: 80, classic: 0)
...
```

### 2. Receive Audio from a Channel

Once you know the channel parameters from the `info` command, use:

```bash
cd /home/haaken/Nedlastinger/gr-dab/build
export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache
python3 apps/grdab.exe receive \
    --freq 222.064 \
    --address 304 \
    --subch_size 64 \
    --bit_rate 64 \
    --protect_level 1 \
    --audiorate 48000 \
    --skip-xrun-monitor
```

**Parameters:**
- `--freq 222.064` - Frequency in MHz
- `--address 304` - Service address (from info command)
- `--subch_size 64` - Subchannel size (from info command)
- `--bit_rate 64` - Bit rate (from info command)
- `--protect_level 1` - Protection level (from info command)
- `--audiorate 48000` - Audio sample rate (48000 Hz)
- `--skip-xrun-monitor` - Run non-interactively (no user input required)

**What it does:**
- Receives DAB+ audio from the specified channel
- Outputs audio to your default audio device
- Runs for 5 seconds then stops (due to --skip-xrun-monitor)

### 3. Interactive Audio Reception (Curses Interface)

For an interactive interface where you can change channels:

```bash
cd /home/haaken/Nedlastinger/gr-dab/build
export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache
python3 apps/grdab.exe curses --freq 222.064
```

**What it does:**
- Opens an ncurses-based interface
- Shows available channels
- Allows you to select and switch between channels
- Press 'q' to quit

### 4. Adjust Gain and PPM (Calibration)

To find optimal gain and frequency error settings:

```bash
cd /home/haaken/Nedlastinger/gr-dab/build
export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache
python3 apps/grdab.exe adjust
```

**What it does:**
- Opens a GUI for adjusting RF gain, IF gain, BB gain, and PPM
- Helps optimize reception quality
- Settings are saved to `~/.grdab/config.yaml`

## Common Frequencies for DAB

DAB Band III frequencies (common in Europe):
- Channel 5A: 174.928 MHz
- Channel 7A: 188.928 MHz
- Channel 8A: 195.936 MHz
- Channel 9A: 202.928 MHz
- Channel 10A: 209.936 MHz
- Channel 11A: 216.928 MHz
- Channel 11B: 222.064 MHz (used in your example)
- Channel 11C: 227.360 MHz
- Channel 11D: 230.072 MHz
- Channel 12A: 239.200 MHz
- Channel 12B: 243.936 MHz
- Channel 12C: 248.928 MHz

## Troubleshooting

### If you get "list contains invalid format!" error:
- Make sure gr-osmosdr was rebuilt against GNU Radio 3.11
- Check: `python3 -c "import osmosdr; print(osmosdr.__file__)"` should show `/usr/local/lib/python3.12/dist-packages/osmosdr`

### If USRP B210 is not detected:
- Check USB connection: `lsusb | grep -i ettus`
- Check UHD: `uhd_find_devices`
- Make sure you have USB permissions (may need to add user to `plugdev` group)

### If no channels are found:
- Verify you're in range of a DAB transmitter
- Try different frequencies
- Increase gain: use `adjust` command to find optimal settings
- Check antenna connection

### If audio doesn't play:
- Check audio system: `aplay -l` or `pactl list sinks`
- Make sure PulseAudio/ALSA is running
- Try different `--audiorate` values (48000, 44100, 32000)

## Quick Reference

**Scan channels:**
```bash
cd /home/haaken/Nedlastinger/gr-dab/build && export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache && python3 apps/grdab.exe info --freq 222.064
```

**Receive audio (replace parameters from info output):**
```bash
cd /home/haaken/Nedlastinger/gr-dab/build && export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache && python3 apps/grdab.exe receive --freq 222.064 --address 304 --subch_size 64 --bit_rate 64 --protect_level 1 --audiorate 48000 --skip-xrun-monitor
```

**Interactive interface:**
```bash
cd /home/haaken/Nedlastinger/gr-dab/build && export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache && python3 apps/grdab.exe curses --freq 222.064
```
