# gr-dab - GNU Radio Digital Audio Broadcasting Module

GNU Radio module for receiving DAB and DAB+ digital radio.

## Features

- DAB/DAB+ signal reception
- Support for multiple SDR devices (USRP B210, RTL-SDR, HackRF, etc.)
- Channel scanning and audio decoding
- Interactive curses-based interface
- Command-line tools for automation

## Requirements

- GNU Radio 3.11
- gr-osmosdr (built against GNU Radio 3.11)
- FAAD2 library (libfaad-dev)
- Python 3.12+
- CMake 3.8+

## Installation

```bash
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig
```

## Usage with USRP B210

### Scan for DAB Channels

```bash
python3 apps/grdab.exe info --freq 222.064
```

### Receive Audio

```bash
python3 apps/grdab.exe receive \
    --freq 222.064 \
    --address 304 \
    --subch_size 64 \
    --bit_rate 64 \
    --protect_level 1 \
    --audiorate 48000 \
    --skip-xrun-monitor
```

### Interactive Interface

```bash
python3 apps/grdab.exe curses --freq 222.064
```

See [USAGE_USRP_B210.md](USAGE_USRP_B210.md) for detailed usage instructions.

## Building gr-osmosdr for GNU Radio 3.11

If you have GNU Radio 3.11 installed but gr-osmosdr was built for 3.10, you'll need to rebuild it:

```bash
git clone https://github.com/osmocom/gr-osmosdr.git
cd gr-osmosdr
mkdir build && cd build
cmake ../ -DCMAKE_PREFIX_PATH=/usr/local
make -j$(nproc)
sudo make install
sudo ldconfig
```

See [rebuild_gr_osmosdr.md](rebuild_gr_osmosdr.md) for detailed instructions.

## Files

- `uff_to_gr_complex.py` - Converter script for DABstar UFF files to GNU Radio complex float format
- `USAGE_USRP_B210.md` - Usage guide for USRP B210
- `rebuild_gr_osmosdr.md` - Guide for rebuilding gr-osmosdr

## License

GPL-3.0-or-later

## Credits

- Original code by Andreas Müller, 2011
- Audio reception completion by Moritz Luca Schmid, 2017 (Google Summer of Code)
