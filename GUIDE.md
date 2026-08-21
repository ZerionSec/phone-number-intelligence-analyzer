# 📚 Complete Guide - Phone Number Intelligence Analyzer

This guide is designed to make it easy to learn and use the tool, especially for beginners and Termux users.

---

## 📖 Learning Path Overview

1. **Understand what the tool can and cannot do**
2. **Install correctly** (PC or Termux)
3. **Run basic commands**
4. **Use batch & export features**
5. **Generate maps (optional)**
6. **Understand Prefix vs Current Carrier**
7. **Practice ethical usage**

---

## 1. What This Tool Does

| Feature                        | Status     | Notes                                      |
|--------------------------------|------------|--------------------------------------------|
| Check if number is valid       | ✅ Yes     | Using public numbering plans               |
| Country detection              | ✅ Yes     |                                            |
| General location description   | ✅ Yes     | High-level only                            |
| Timezone                       | ✅ Yes     |                                            |
| Original Philippine prefix     | ✅ Yes     | e.g. 0917 = originally Globe/TM            |
| Current carrier                | ⚠️ Limited | Library data (may be outdated due to MNP)  |
| Live GPS tracking              | ❌ No      | Impossible with public data                |
| Owner identification           | ❌ No      |                                            |
| Cell tower location            | ❌ No      |                                            |

---

## 2. Installation

### A. Normal Computer (Windows / Linux / Mac)

```bash
git clone https://github.com/ZerionSec/phone-number-intelligence-analyzer.git
cd phone-number-intelligence-analyzer
pip install -r requirements.txt
```

### B. Termux (Android) — Recommended Steps

```bash
# Update packages
pkg update && pkg upgrade -y

# Install git and python
pkg install git python -y

# Clone the repository
git clone https://github.com/ZerionSec/phone-number-intelligence-analyzer.git
cd phone-number-intelligence-analyzer

# Install dependencies
pip install phonenumbers geopy

# Optional (for map feature)
pip install folium
```

> **Tip:** Kung slow ang internet, pwede munang huwag i-install ang `folium` kung hindi mo kailangan ng map.

---

## 3. Basic Usage

### Single Number Analysis

```bash
python phone_analyzer.py 09171234567
```

or international format:

```bash
python phone_analyzer.py +639171234567
```

### Interactive Mode (kung walang argument)

```bash
python phone_analyzer.py
# Then type the number when asked
```

---

## 4. Advanced Usage

### Generate Approximate Map

```bash
python phone_analyzer.py --map 09171234567
```

- Magse-save ng HTML file (hal. `phone_map_+639171234567.html`)
- Buksan sa browser

### Batch Processing

1. Gumawa ng text file:

```bash
nano numbers.txt
```

Ilagay ang numbers (one per line):

```
09171234567
09991234567
+639171234567
```

Save: `Ctrl + O` → Enter → `Ctrl + X`

2. Run:

```bash
python phone_analyzer.py -b numbers.txt
```

### Export Results

```bash
# JSON
python phone_analyzer.py 09171234567 -e json

# CSV
python phone_analyzer.py 09171234567 -e csv

# Combined with batch
python phone_analyzer.py -b numbers.txt -e json
```

---

## 5. Understanding the Output

| Field                | Meaning                                                                 |
|----------------------|-------------------------------------------------------------------------|
| Number               | Normalized international format                                         |
| Country              | Detected country                                                        |
| Location             | General description from numbering plan                                 |
| Carrier              | Library carrier data (may not reflect current carrier due to MNP)       |
| Prefix               | First 4 digits (e.g. 0917)                                              |
| Prefix network       | Original network assigned to that prefix                                |
| Timezone             | Timezone(s) associated with the number                                  |
| Approx. coordinates  | Geocoded from general location (NOT device location)                    |

---

## 6. Prefix vs Current Carrier (Important!)

Dahil sa **Mobile Number Portability (MNP)** sa Pilipinas:

- Ang **Prefix** (hal. 0917) ay nagsasabi lang kung **anong network originally** ang number.
- Ang **current carrier** ay maaaring magbago kung in-port ang number.

Halimbawa:
- 0917 → Originally Globe/TM
- Pero possible na Smart o DITO na ngayon ang actual network.

Kaya laging tingnan ang dalawang field:
- `Prefix network` → Original
- `Carrier` → Library estimate

---

## 7. Useful Commands Cheat Sheet

| Action                        | Command                                      |
|-------------------------------|----------------------------------------------|
| Analyze one number            | `python phone_analyzer.py 0917xxxxxxx`       |
| With map                      | `python phone_analyzer.py --map 0917xxxxxxx` |
| Batch                         | `python phone_analyzer.py -b numbers.txt`    |
| Export JSON                   | `... -e json`                                |
| Export CSV                    | `... -e csv`                                 |
| Show version                  | `python phone_analyzer.py -v`                |
| Save output to file           | `python phone_analyzer.py 0917... > result.txt` |

---

## 8. Common Issues (Termux)

| Problem                          | Solution                                      |
|----------------------------------|-----------------------------------------------|
| `python: command not found`      | Use `python` or `python3`                     |
| `pip: command not found`         | `pkg install python` then try again           |
| Slow install                     | Install one by one: `pip install phonenumbers` |
| Permission denied                | Huwag gumamit ng `sudo` sa Termux             |
| Folium error                     | Skip map feature or install `pkg install libjpeg-turbo` |

---

## 9. Ethical Reminder

- Gamitin lang para sa **legitimate** purposes (research, fraud investigation, learning).
- Huwag gamitin para manmanan o harass ang tao.
- Laging igalang ang privacy laws.

---

## Need Help?

Kapag may error, kopyahin ang exact error message at i-message para matulungan kita.

Maligayang pag-aaral! 🚀
