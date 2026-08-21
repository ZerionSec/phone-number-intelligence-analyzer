# Phone Number Intelligence Analyzer

**Defensive / OSINT metadata tool** for analyzing publicly available phone number information.

> ⚠️ This tool does **NOT** track GPS, locate phones in real time, access cell towers, or identify the owner of a phone number.

## Features

- Number validity check
- Country detection
- General geographic description
- Timezone information
- Carrier metadata (via `phonenumbers` library)
- Philippine mobile prefix lookup (original network association)
- Optional approximate map visualization (metadata only)
- Batch processing
- JSON / CSV export
- Local history logging

## Important Notes

- Philippine prefix data reflects **original number assignment** only.
- Due to **Mobile Number Portability (MNP)**, the current carrier may differ from the original prefix network.
- Approximate coordinates are derived from the high-level geographic description returned by the numbering plan — **not** from the device.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single number

```bash
python phone_analyzer.py 09171234567
python phone_analyzer.py +639171234567
python phone_analyzer.py --map 09171234567
```

### Batch mode

```bash
python phone_analyzer.py -b numbers.txt
```

### Export results

```bash
python phone_analyzer.py 09171234567 -e json
python phone_analyzer.py -b numbers.txt -e csv
```

### Version

```bash
python phone_analyzer.py -v
```

## Example Output

```
============================================================
 PHONE NUMBER INTELLIGENCE
============================================================
📞 Number  : +639171234567
🌍 Country : Philippines
🏙️ Location: Philippines
📡 Carrier : Globe Telecom
📱 Prefix  : 0917
🏢 Prefix network: Globe/TM
🕒 Timezone: Asia/Manila
🌐 Intl     : +63 917 123 4567
📍 Location type: Approximate metadata location only

⚠️ This is NOT live GPS tracking.
⚠️ Coordinates represent general metadata only.
============================================================
```

## Disclaimer

This tool is intended for legitimate defensive security research, fraud investigation, and educational purposes only.  
Misuse of phone number data may violate local laws. Always respect privacy regulations.

## License

MIT
