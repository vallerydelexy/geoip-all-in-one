#!/usr/bin/env python3
"""
Inspect and summarize merged GeoIP TSV files.
Displays line count, sample rows, country distribution, and data integrity.
"""

import sys
import os
from collections import Counter


def inspect_tsv(tsv_path, sample_count=5):
    if not os.path.exists(tsv_path):
        print(f"Error: TSV file does not exist: {tsv_path}", file=sys.stderr)
        return False

    file_size_mb = os.path.getsize(tsv_path) / (1024 * 1024)
    print(f"[*] Inspecting: {tsv_path} ({file_size_mb:.2f} MB)")

    total_lines = 0
    country_counts = Counter()
    samples = []
    malformed = 0

    with open(tsv_path, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) < 5:
                malformed += 1
                continue

            total_lines += 1
            country = parts[2]
            country_counts[country] += 1

            if len(samples) < sample_count:
                samples.append((line_num, parts))

    print(f"[+] Total Valid Ranges: {total_lines:,}")
    print(f"[+] Distinct Countries: {len(country_counts):,}")
    if "ID" in country_counts:
        print(f"[+] Indonesia (ID) Ranges: {country_counts['ID']:,}")
    if malformed:
        print(f"[!] Malformed lines: {malformed:,}")

    print("\n--- Top 10 Countries ---")
    for cc, count in country_counts.most_common(10):
        pct = (count / total_lines * 100) if total_lines else 0
        print(f"  {cc:<4} : {count:>9,} ({pct:5.2f}%)")

    print(f"\n--- First {len(samples)} Sample Entries ---")
    print(f"{'Line':<6} {'Start Hex':<16} {'End Hex':<16} {'CC':<4} {'Latitude':<10} {'Longitude':<10} {'Region':<16} {'City':<16}")
    print("-" * 96)
    for line_num, parts in samples:
        reg = parts[5] if len(parts) > 5 else ''
        city = parts[6] if len(parts) > 6 else ''
        print(f"{line_num:<6} {parts[0]:<16} {parts[1]:<16} {parts[2]:<4} {parts[3]:<10} {parts[4]:<10} {reg:<16} {city:<16}")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: inspect_tsv.py <path_to_tsv> [sample_count]")
        sys.exit(1)

    tsv_path = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    success = inspect_tsv(tsv_path, count)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
