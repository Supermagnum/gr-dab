# Rebuilding gr-osmosdr for GNU Radio 3.11

## Current Situation

- **Installed gr-osmosdr**: Version 0.2.5 (built for GNU Radio 3.10.9)
- **Current GNU Radio**: Version 3.11.0.0git-1032-gab049f6e (installed in /usr/local)
- **Issue**: Version mismatch causing "list contains invalid format!" error
- **Library dependencies**: gr-osmosdr links against libgnuradio-runtime.so.3.10.9

## Solution: Build gr-osmosdr from Source Against GNU Radio 3.11

### Step 1: Install Build Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    git \
    cmake \
    build-essential \
    libboost-all-dev \
    libcppunit-dev \
    liblog4cpp5-dev \
    python3-dev \
    swig \
    libuhd-dev \
    libsoapysdr-dev \
    libairspy-dev \
    libhackrf-dev \
    librtlsdr-dev \
    libbladerf-dev \
    libfreesrp-dev \
    libxtrx-dev \
    pkg-config

# Optional SDR device support (install if available):
# libredpitaya-dev - Red Pitaya SDR support (may not be available in all repos)
```

### Step 2: Clone gr-osmosdr Repository

```bash
cd ~
git clone --depth 1 https://github.com/osmocom/gr-osmosdr.git
cd gr-osmosdr
```

### Step 3: Configure Build for GNU Radio 3.11

The build system should automatically detect GNU Radio 3.11 from /usr/local/lib/cmake/gnuradio.
If it doesn't, you can specify the path:

```bash
mkdir build
cd build
cmake ../ -DCMAKE_PREFIX_PATH=/usr/local
```

### Step 4: Build and Install

```bash
make -j$(nproc)
sudo make install
sudo ldconfig
```

### Step 5: Verify Installation

```bash
python3 -c "import osmosdr; print('gr-osmosdr loaded successfully')"
ldd $(python3 -c "import osmosdr; import os; print(os.path.dirname(osmosdr.__file__))")/osmosdr_python*.so | grep gnuradio
```

The ldd output should show libgnuradio-runtime.so.3.11 instead of 3.10.

### Step 6: Test with gr-dab

```bash
cd /home/haaken/Nedlastinger/gr-dab/build
export XDG_CACHE_HOME=/home/haaken/Nedlastinger/gr-dab/.cache
python3 apps/grdab.exe info --freq 222.064
```

## Troubleshooting

### If cmake can't find GNU Radio 3.11:

```bash
export CMAKE_PREFIX_PATH=/usr/local:$CMAKE_PREFIX_PATH
cmake ../
```

### If Python can't find the new module:

```bash
export PYTHONPATH=/usr/local/lib/python3.12/dist-packages:$PYTHONPATH
```

### To keep using system gr-osmosdr (GNU Radio 3.10):

If rebuilding doesn't work, you could downgrade GNU Radio to 3.10 to match gr-osmosdr.

## Notes

- The build will automatically detect GNU Radio 3.11 from /usr/local if CMake is configured correctly
- After installation, the new gr-osmosdr will be in /usr/local/lib/python3.12/dist-packages/osmosdr
- Make sure to run `sudo ldconfig` after installation to update library cache
- The build process may take 10-30 minutes depending on your system
- You may need to uninstall the package manager version first: `sudo apt-get remove gr-osmosdr` (but keep libgnuradio-osmosdr0.2.0t64 for now)
