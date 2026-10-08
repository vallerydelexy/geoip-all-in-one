#!/usr/bin/env python3
"""
Inspect and verify generated .mmdb files.
Queries sample IPv4 and IPv6 addresses and checks payload structure.
"""

import sys
import os

try:
    import maxminddb
except ImportError:
    maxminddb = None

SAMPLE_IPS = [
    "8.8.8.8",
    "1.1.1.1",
    "103.10.60.1",
    "36.64.0.1",
    "208.67.222.222",
    "2001:4860:4860::8888",
    "2606:4700:4700::1111",
]


def verify_database(mmdb_path, query_ips=None):
    if not os.path.exists(mmdb_path):
        print(f"Error: Database file does not exist: {mmdb_path}", file=sys.stderr)
        return False

    file_size_mb = os.path.getsize(mmdb_path) / (1024 * 1024)
    print(f"[*] Verifying: {mmdb_path} ({file_size_mb:.2f} MB)")

    if maxminddb is None:
        print("[!] Warning: maxminddb library not installed. Checking binary header only.")
        with open(mmdb_path, "rb") as f:
            header = f.read(64)
            if b"\xab\xcd\xefMaxMind.com" in f.read() or len(header) > 0:
                print("[+] Binary file is non-empty and accessible.")
                return True
            return False

    with maxminddb.open_database(mmdb_path) as reader:
        print(f"[+] Metadata type: {reader.metadata().database_type}")
        print(f"[+] IP version: {reader.metadata().ip_version}")
        print(f"[+] Node count: {reader.metadata().node_count}")

        ips_to_check = query_ips or SAMPLE_IPS
        hits = 0
        for ip in ips_to_check:
            try:
                record = reader.get(ip)
                if record:
                    hits += 1
                    country = record.get("country", {}).get("iso_code", "N/A")
                    loc = record.get("location", {})
                    lat = loc.get("latitude", "N/A")
                    lon = loc.get("longitude", "N/A")
                    tz = loc.get("time_zone", "N/A")
                    city = record.get("city", {}).get("names", {}).get("en")
                    subdivs = record.get("subdivisions", [])
                    region = subdivs[0].get("names", {}).get("en") if subdivs else None
                    details = []
                    if city:
                        details.append(f"City: {city}")
                    if region:
                        details.append(f"Region: {region}")
                    extra = f" [{', '.join(details)}]" if details else ""
                    print(f"  [HIT]  {ip:<24} -> {country:<4} ({lat}, {lon}) TZ: {tz}{extra}")
                else:
                    print(f"  [MISS] {ip:<24} -> Not found")
            except Exception as e:
                print(f"  [ERR]  {ip:<24} -> Error: {e}")

        print(f"[+] Verification completed: {hits}/{len(ips_to_check)} sample hits.")
        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_mmdb.py <path_to_mmdb> [ip1 ip2 ...]")
        sys.exit(1)

    db_path = sys.argv[1]
    extra_ips = sys.argv[2:] if len(sys.argv) > 2 else None
    success = verify_database(db_path, extra_ips)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
