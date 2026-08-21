# Phone Number Intelligence Analyzer

**Defensive / OSINT metadata tool** for analyzing publicly available phone number information.

> ⚠️ This tool does **NOT** track GPS, locate phones in real time, access cell towers, or identify the owner of a phone number.

---

## 📖 Learning Path

Recommended order para matuto at magamit ang tool:

| Step | Topic                              | Link / File              | Difficulty |
|------|------------------------------------|--------------------------|------------|
| 1    | Overview & Features                | This README              | Beginner   |
| 2    | Installation (Normal + Termux)     | [GUIDE.md](GUIDE.md)     | Beginner   |
| 3    | Basic Usage                        | [GUIDE.md](GUIDE.md)     | Beginner   |
| 4    | Batch Processing & Export          | [GUIDE.md](GUIDE.md)     | Intermediate |
| 5    | Map Generation                     | [GUIDE.md](GUIDE.md)     | Intermediate |
| 6    | Understanding Prefix vs Carrier    | This README + GUIDE      | Intermediate |
| 7    | Ethical Use & Limitations          | Disclaimer section       | Important  |

---

## 🛠 Features

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

---

## ⚠️ Important Notes

- Philippine prefix data reflects **original number assignment** only.
- Due to **Mobile Number Portability (MNP)**, the current carrier may differ from the original prefix network.
- Approximate coordinates are derived from the high-level geographic description returned by the numbering plan — **not** from the device.

---

## 📦 Quick Installation

```bash
pip install -r requirements.txt
```

> Full installation guide (including **Termux**) → [GUIDE.md](GUIDE.md)

---

## 🚀 Quick Usage

```bash
# Single number
python phone_analyzer.py 09171234567

# With map
python phone_analyzer.py --map 09171234567

# Batch
python phone_analyzer.py -b numbers.txt

# Export
python phone_analyzer.py 09171234567 -e json
```

---

## 📋 Full Guide

Para sa detalyadong step-by-step instructions (kasama ang Termux):

**👉 [GUIDE.md](GUIDE.md)**

---

## 📝 Example Output

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

---

## 🚫 Disclaimer

This tool is intended for legitimate defensive security research, fraud investigation, and educational purposes only.  
Misuse of phone number data may violate local laws. Always respect privacy regulations.

## License

MIT
