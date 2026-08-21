#!/usr/bin/env python3

"""
Phone Number Intelligence Analyzer
-----------------------------------
Defensive / OSINT metadata tool.

This tool can analyze publicly available numbering metadata such as:
- Number validity
- Country
- General geographic description
- Timezone
- Carrier metadata
- Philippine number prefix
- Optional approximate map visualization

IMPORTANT:
This tool DOES NOT:
- Track GPS
- Locate a phone in real time
- Access cell towers
- Access private subscriber information
- Identify the owner of a phone number
"""

import argparse
import csv
import json
import os
import re
import time
from datetime import datetime, timezone as dt_timezone

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from geopy.geocoders import Nominatim


APP_NAME = "Phone Number Intelligence Analyzer"
VERSION = "1.2.1"


# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------

def print_banner():
    banner = r"""
┌──────────────────────────────────────────────────────────┐
│                                                         │
│   ░██████████░  ░█████████░  ░█████████░  ░█████████░   │
│   ░██░░░░░░░░  ░██░░░░░░░  ░██░░░░░░░  ░██░░░░░░░   │
│   ░█████████░  ░████████░  ░████████░  ░████████░   │
│   ░██░░░░░░░░  ░██░░░░░░░  ░██░░░░░░░  ░██░░░░░░░   │
│   ░█████████░  ░█████████░  ░█████████░  ░█████████░   │
│                                                         │
│              Z E R I O N S E C                          │
│     Phone Number Intelligence Analyzer  v1.2.1          │
│                                                         │
└──────────────────────────────────────────────────────────┘
"""
    print(banner)


# ---------------------------------------------------------
# PHILIPPINE PREFIX DATABASE
# ---------------------------------------------------------

PH_PREFIXES = {
    "0905": "Globe/TM", "0906": "Globe/TM", "0915": "Globe/TM", "0916": "Globe/TM",
    "0917": "Globe/TM", "0926": "Globe/TM", "0927": "Globe/TM", "0935": "Globe/TM",
    "0936": "Globe/TM", "0937": "Globe/TM", "0945": "Globe/TM", "0956": "Globe/TM",
    "0965": "Globe/TM", "0966": "Globe/TM", "0975": "Globe/TM", "0976": "Globe/TM",
    "0977": "Globe/TM", "0978": "Globe/TM", "0979": "Globe/TM", "0995": "Globe/TM",
    "0996": "Globe/TM", "0997": "Globe/TM", "0998": "Globe/TM", "0999": "Globe/TM",

    "0907": "Smart/TNT", "0908": "Smart/TNT", "0909": "Smart/TNT", "0910": "Smart/TNT",
    "0911": "Smart/TNT", "0912": "Smart/TNT", "0913": "Smart/TNT", "0914": "Smart/TNT",
    "0918": "Smart/TNT", "0919": "Smart/TNT", "0920": "Smart/TNT", "0921": "Smart/TNT",
    "0922": "Smart/TNT", "0923": "Smart/TNT", "0924": "Smart/TNT", "0925": "Smart/TNT",
    "0928": "Smart/TNT", "0929": "Smart/TNT", "0930": "Smart/TNT", "0938": "Smart/TNT",
    "0939": "Smart/TNT", "0940": "Smart/TNT", "0946": "Smart/TNT", "0947": "Smart/TNT",
    "0948": "Smart/TNT", "0949": "Smart/TNT", "0950": "Smart/TNT", "0951": "Smart/TNT",
    "0955": "Smart/TNT", "0960": "Smart/TNT", "0961": "Smart/TNT", "0963": "Smart/TNT",
    "0964": "Smart/TNT", "0967": "Smart/TNT", "0968": "Smart/TNT", "0969": "Smart/TNT",
    "0970": "Smart/TNT", "0971": "Smart/TNT", "0972": "Smart/TNT", "0973": "Smart/TNT",
    "0974": "Smart/TNT", "0980": "Smart/TNT", "0981": "Smart/TNT", "0988": "Smart/TNT",
    "0989": "Smart/TNT", "0990": "Smart/TNT", "0991": "Smart/TNT", "0992": "Smart/TNT",
    "0993": "Smart/TNT", "0994": "Smart/TNT",

    "0895": "DITO", "0896": "DITO", "0897": "DITO", "0898": "DITO",
}


def clean_number(number):
    number = number.strip()
    if number.startswith("+"):
        return "+" + re.sub(r"\D", "", number[1:])
    return re.sub(r"\D", "", number)


def normalize_ph_number(number):
    number = clean_number(number)
    if number.startswith("+63"):
        return number
    if number.startswith("63"):
        return "+" + number
    if number.startswith("0") and len(number) == 11:
        return "+63" + number[1:]
    return number


def get_ph_prefix(number):
    normalized = normalize_ph_number(number)
    if not normalized.startswith("+63"):
        return None
    local = normalized[3:]
    if len(local) < 3:
        return None
    if local.startswith("9") and len(local) >= 3:
        return "0" + local[:3]
    if local.startswith("8") and len(local) >= 3:
        return "0" + local[:3]
    return None


def get_original_ph_network(number):
    prefix = get_ph_prefix(number)
    if not prefix:
        return "Unknown"
    return PH_PREFIXES.get(prefix, "Unknown")


def safe_geocode(geolocator, location, country):
    if not location or location == "Unknown":
        return None, None
    if not country or country == "Unknown":
        return None, None
    if location.strip().lower() == country.strip().lower():
        return None, None
    try:
        query = f"{location}, {country}"
        result = geolocator.geocode(query, exactly_one=True, timeout=10)
        if result:
            return result.latitude, result.longitude
    except Exception:
        pass
    return None, None


class PhoneAnalyzer:

    def __init__(self):
        self.results = []
        self.geolocator = Nominatim(user_agent="phone-intelligence-analyzer/1.2")

    def analyze(self, phone_input):
        original_input = phone_input
        normalized = normalize_ph_number(phone_input)

        result = {
            "input": original_input,
            "number": normalized,
            "timestamp": datetime.now(dt_timezone.utc).isoformat()
        }

        try:
            try:
                parsed = phonenumbers.parse(normalized, "PH")
            except phonenumbers.NumberParseException as exc:
                return {"input": original_input, "error": f"Invalid phone format: {exc}"}

            result["possible"] = phonenumbers.is_possible_number(parsed)
            result["valid"] = phonenumbers.is_valid_number(parsed)

            if not result["valid"]:
                result["error"] = "Number is not valid according to numbering metadata."
                return result

            country = geocoder.country_name_for_number(parsed, "en")
            result["country"] = country or "Unknown"

            general_location = geocoder.description_for_number(parsed, "en")
            raw_location = general_location or "Unknown"
            result["general_location_raw"] = raw_location

            if raw_location.strip().lower() == "philippines":
                result["general_location"] = "Philippines (City/Province level not available for mobile numbers)"
            else:
                result["general_location"] = raw_location

            library_carrier = carrier.name_for_number(parsed, "en")
            result["carrier_metadata"] = library_carrier or "Unknown"

            timezones = timezone.time_zones_for_number(parsed)
            result["timezones"] = list(timezones)

            prefix = get_ph_prefix(phone_input)
            result["ph_prefix"] = prefix or "Unknown"
            result["prefix_network"] = get_original_ph_network(phone_input)

            result["international_format"] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            result["national_format"] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.NATIONAL
            )

            latitude, longitude = safe_geocode(self.geolocator, raw_location, result["country"])
            result["approximate_latitude"] = latitude
            result["approximate_longitude"] = longitude

            result["location_type"] = "Approximate metadata location only"
            result["live_tracking"] = False

            return result

        except Exception as exc:
            return {"input": original_input, "error": str(exc)}

    def display(self, result):
        print("\n" + "=" * 60)
        print(" PHONE NUMBER INTELLIGENCE")
        print("=" * 60)

        if "error" in result:
            print(f"❌ Input    : {result.get('input', 'Unknown')}")
            print(f"❌ Error    : {result['error']}")
            return

        print(f"📞 Number  : {result['number']}")
        print(f"🌍 Country : {result['country']}")
        print(f"🏙️ Location: {result['general_location']}")
        print(f"📡 Carrier : {result['carrier_metadata']}")
        print(f"📱 Prefix  : {result['ph_prefix']}")
        print(f"🏢 Prefix network: {result['prefix_network']}")
        print(f"🕒 Timezone: {', '.join(result['timezones']) or 'Unknown'}")
        print(f"🌐 Intl     : {result['international_format']}")
        print(f"📍 Location type: {result['location_type']}")

        if (
            result.get("approximate_latitude") is not None
            and result.get("approximate_longitude") is not None
        ):
            print(
                f"🗺️ Approx. coordinates: "
                f"{result['approximate_latitude']}, "
                f"{result['approximate_longitude']}"
            )

        print("=" * 60)

    def generate_map(self, result):
        latitude = result.get("approximate_latitude")
        longitude = result.get("approximate_longitude")

        if latitude is None or longitude is None:
            print("⚠️ No useful approximate coordinates available.")
            print("   (Common for Philippine mobile numbers — only country-level data exists)")
            return None

        try:
            import folium
        except ImportError:
            print("❌ Folium is not installed.")
            print("Install with: pip install folium")
            return None

        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", result["number"])
        filename = f"phone_map_{safe_name}.html"

        map_object = folium.Map(location=[latitude, longitude], zoom_start=8)

        popup = f"""
        <b>Phone Intelligence</b><br>
        Number: {result['number']}<br>
        Country: {result['country']}<br>
        General Location: {result['general_location']}<br>
        Carrier Metadata: {result['carrier_metadata']}<br>
        Prefix Network: {result['prefix_network']}<br>
        <hr>
        <b>NOT LIVE GPS LOCATION</b>
        """

        folium.Marker(
            [latitude, longitude],
            popup=popup,
            tooltip="Approximate metadata location"
        ).add_to(map_object)

        map_object.save(filename)
        print(f"🗺️ Map saved: {filename}")
        return filename

    def save_history(self, result, filename="phone_history.json"):
        try:
            history = []
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    try:
                        history = json.load(file)
                    except json.JSONDecodeError:
                        history = []
            history.append(result)
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4, ensure_ascii=False)
            print(f"💾 History saved: {filename}")
        except Exception as exc:
            print(f"⚠️ Could not save history: {exc}")

    def export_csv(self, filename="phone_results.csv"):
        if not self.results:
            print("⚠️ Nothing to export.")
            return
        fields = set()
        for result in self.results:
            fields.update(result.keys())
        fields = sorted(fields)
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        print(f"📄 CSV exported: {filename}")

    def export_json(self, filename="phone_results.json"):
        if not self.results:
            print("⚠️ Nothing to export.")
            return
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.results, file, indent=4, ensure_ascii=False)
        print(f"📄 JSON exported: {filename}")

    def process_batch(self, filename):
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return
        try:
            with open(filename, "r", encoding="utf-8") as file:
                numbers = [line.strip() for line in file if line.strip()]
        except Exception as exc:
            print(f"❌ Could not read file: {exc}")
            return
        print(f"📂 Loaded {len(numbers)} number(s).")
        for index, number in enumerate(numbers, start=1):
            print(f"\n[{index}/{len(numbers)}]")
            result = self.analyze(number)
            self.results.append(result)
            self.display(result)
            self.save_history(result)
            if index < len(numbers):
                time.sleep(1)

    @staticmethod
    def show_version():
        print(f"{APP_NAME} v{VERSION}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze phone-number metadata. This tool does not perform live GPS tracking."
    )
    parser.add_argument("number", nargs="?", help="Phone number to analyze")
    parser.add_argument("-b", "--batch", help="Text file containing one number per line")
    parser.add_argument("-e", "--export", choices=["json", "csv"], help="Export results")
    parser.add_argument("--map", action="store_true", help="Generate an approximate metadata map")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if not args.version:
        print_banner()

    analyzer = PhoneAnalyzer()

    if args.version:
        analyzer.show_version()
        return

    if args.batch:
        analyzer.process_batch(args.batch)
    else:
        number = args.number
        if not number:
            number = input("📞 Enter phone number: ").strip()
        if not number:
            print("❌ No phone number provided.")
            return

        result = analyzer.analyze(number)
        analyzer.results.append(result)
        analyzer.display(result)
        analyzer.save_history(result)

        if args.map:
            analyzer.generate_map(result)

    if args.export == "json":
        analyzer.export_json()
    elif args.export == "csv":
        analyzer.export_csv()


if __name__ == "__main__":
    main()
