#!/usr/bin/env python3
"""
Convert DABstar UFF file to GNU Radio complex float format.

UFF file format:
- XML header (ends with </SDR>)
- Padding (null bytes)
- Binary IQ data: uint8, I/Q interleaved, LSB ordering

GNU Radio complex float format:
- Interleaved float32 pairs: [real, imag, real, imag, ...]
- Little-endian
- Each complex sample is 8 bytes (4 bytes real + 4 bytes imag)
"""

import struct
import sys
import xml.etree.ElementTree as ET
import os

def find_iq_data_start(filename):
    """Find where IQ data starts after XML header."""
    with open(filename, 'rb') as f:
        data = f.read(2000)  # Read enough to find XML end
    
    xml_end = data.find(b'</SDR>')
    if xml_end == -1:
        raise ValueError("Could not find </SDR> tag in file")
    
    xml_end_pos = xml_end + 6  # After </SDR>
    
    # Find first non-null byte after XML (start of IQ data)
    iq_start = xml_end_pos
    while iq_start < len(data) and data[iq_start] == 0:
        iq_start += 1
    
    # If we hit the end, check if there's padding before actual data
    # Look for pattern that suggests IQ data (non-zero bytes)
    if iq_start >= len(data):
        # Read more to find actual data start
        f.seek(0)
        data = f.read(10000)
        xml_end = data.find(b'</SDR>')
        xml_end_pos = xml_end + 6
        iq_start = xml_end_pos
        # Skip null padding
        while iq_start < len(data) and data[iq_start] == 0:
            iq_start += 1
    
    return iq_start

def parse_uff_metadata(filename):
    """Parse XML metadata from UFF file."""
    with open(filename, 'rb') as f:
        data = f.read(2000)
    
    xml_end = data.find(b'</SDR>')
    if xml_end == -1:
        return None
    
    xml_data = data[:xml_end + 6].decode('utf-8', errors='ignore')
    
    try:
        root = ET.fromstring(xml_data)
        metadata = {}
        
        # Extract recorder info
        recorder = root.find('Recorder')
        if recorder is not None:
            metadata['recorder_version'] = recorder.get('Version', '')
            metadata['recorder_name'] = recorder.get('Name', '')
        
        # Extract device info
        device = root.find('Device')
        if device is not None:
            metadata['device_name'] = device.get('Name', '')
            metadata['device_model'] = device.get('Model', '')
        
        # Extract time
        time_elem = root.find('Time')
        if time_elem is not None:
            metadata['time'] = time_elem.get('Value', '')
        
        # Extract sample info
        sample = root.find('Sample')
        if sample is not None:
            samplerate = sample.find('Samplerate')
            if samplerate is not None:
                metadata['samplerate'] = int(samplerate.get('Value', '0'))
            
            channels = sample.find('Channels')
            if channels is not None:
                metadata['ordering'] = channels.get('Ordering', '')
                metadata['container'] = channels.get('Container', '')
                metadata['bits'] = int(channels.get('Bits', '8'))
        
        # Extract datablock info
        datablocks = root.find('Datablocks')
        if datablocks is not None:
            datablock = datablocks.find('Datablock')
            if datablock is not None:
                freq_elem = datablock.find('Frequency')
                if freq_elem is not None:
                    metadata['frequency'] = int(freq_elem.get('Value', '0'))
                metadata['modulation'] = datablock.get('Modulation', '')
                metadata['sample_count'] = int(datablock.get('Count', '0'))
        
        return metadata
    except ET.ParseError as e:
        print(f"Warning: Could not parse XML metadata: {e}", file=sys.stderr)
        return None

def convert_uff_to_gr_complex(input_file, output_file=None):
    """Convert UFF file to GNU Radio complex float format."""
    
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '_gr_complex.dat'
    
    # Parse metadata
    print(f"Reading UFF file: {input_file}")
    metadata = parse_uff_metadata(input_file)
    if metadata:
        print(f"  Recorder: {metadata.get('recorder_name', 'Unknown')} v{metadata.get('recorder_version', '?')}")
        print(f"  Device: {metadata.get('device_model', 'Unknown')}")
        print(f"  Sample Rate: {metadata.get('samplerate', 0):,} Hz")
        print(f"  Frequency: {metadata.get('frequency', 0):,} kHz")
        print(f"  Sample Count: {metadata.get('sample_count', 0):,}")
    
    # Find where IQ data starts
    iq_start = find_iq_data_start(input_file)
    print(f"  IQ data starts at byte offset: {iq_start}")
    
    # Get file size
    file_size = os.path.getsize(input_file)
    iq_data_size = file_size - iq_start
    expected_samples = iq_data_size // 2  # uint8 I/Q pairs
    print(f"  IQ data size: {iq_data_size:,} bytes ({expected_samples:,} complex samples)")
    
    # Convert
    print(f"\nConverting to GNU Radio complex float format...")
    samples_written = 0
    
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        # Skip to IQ data
        infile.seek(iq_start)
        
        # Read and convert in chunks
        chunk_size = 1024 * 1024  # 1 MB chunks
        buffer = bytearray(chunk_size)
        
        while True:
            # Read uint8 I/Q pairs
            data = infile.read(chunk_size)
            if not data:
                break
            
            # Ensure we read even number of bytes (I/Q pairs)
            if len(data) % 2 != 0:
                data = data[:-1]
            
            # Convert uint8 I/Q pairs to complex float
            # RTL-SDR uses offset binary: 128 = DC, so normalize to -1.0 to 1.0
            for i in range(0, len(data), 2):
                i_val = data[i]
                q_val = data[i + 1]
                
                # Convert from uint8 (0-255) to float (-1.0 to 1.0)
                # Offset binary: 128 = 0.0, 0 = -1.0, 255 = +1.0
                i_float = (i_val - 128.0) / 128.0
                q_float = (q_val - 128.0) / 128.0
                
                # Write as little-endian float32 pair
                outfile.write(struct.pack('<ff', i_float, q_float))
                samples_written += 1
            
            if len(data) < chunk_size:
                break
    
    print(f"\nConversion complete!")
    print(f"  Output file: {output_file}")
    print(f"  Samples written: {samples_written:,}")
    print(f"  Output file size: {os.path.getsize(output_file):,} bytes")
    print(f"\nUsage with gr-dab:")
    freq_hz = metadata.get('frequency', 222064) * 1000 if metadata and metadata.get('frequency') else 222064000
    print(f"  python -m gnuradio.dab.receive_dabplus --from-file {output_file} --frequency {freq_hz}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: uff_to_gr_complex.py <input.uff> [output.dat]")
        print("\nConverts DABstar UFF file to GNU Radio complex float format.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        convert_uff_to_gr_complex(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
