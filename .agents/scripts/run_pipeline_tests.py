#!/usr/bin/env python3
"""
Unit and integration tests for GeoIP pipeline components.
Tests IP conversion, RangeTable sweep-line, voting logic, and timezone calculation.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock

# Gracefully handle optional third-party packages if not yet installed in current python env
for mod in ("yaml", "netaddr", "mmdb_writer", "tzfpy"):
    if mod not in sys.modules:
        try:
            __import__(mod)
        except ImportError:
            sys.modules[mod] = MagicMock()


# Ensure project root is in path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.merge import (
    hex_to_int,
    ip_to_int,
    ipv6_to_int,
    int_to_hex,
    RangeTable,
    load_latlong_tsv,
    resolve_region_city,
    pick_winner,
)
from scripts.convert import hex_to_ip, process_file


class TestIPConversion(unittest.TestCase):
    def test_ip_to_int_and_hex(self):
        # 1.1.1.1
        val = ip_to_int("1.1.1.1")
        self.assertEqual(val, (1 << 24) + (1 << 16) + (1 << 8) + 1)
        self.assertEqual(hex_to_int(int_to_hex(val)), val)

    def test_ipv6_to_int(self):
        val = ipv6_to_int("2001:db8::1")
        self.assertIsInstance(val, int)
        self.assertGreater(val, 0)

    def test_hex_to_ip(self):
        if isinstance(sys.modules.get("netaddr"), MagicMock):
            self.skipTest("netaddr is not installed (running in stub mode)")
        hex_v4 = int_to_hex(ip_to_int("8.8.8.8"))
        ip_obj = hex_to_ip(hex_v4, ipv6=False)
        self.assertEqual(str(ip_obj), "8.8.8.8")


class TestRangeTable(unittest.TestCase):
    def test_range_table_sequential(self):
        rt = RangeTable()
        rt.add(10, 20, ("US", 37.0, -122.0, True, "", ""))
        rt.add(30, 40, ("JP", 35.0, 139.0, True, "", ""))
        rt.finalize("test_source")

        # Test within bounds
        res = rt.sweep(15)
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "US")

        # Test gap
        res_gap = rt.sweep(25)
        self.assertIsNone(res_gap)

        # Test second range
        res2 = rt.sweep(35)
        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], "JP")

    def test_range_table_boundary(self):
        rt = RangeTable()
        rt.add(100, 200, ("ID", -6.2, 106.8, True, "Jakarta Raya", "Jakarta"))
        rt.finalize("boundary_test")

        # In sweep-line, endpoints are tested sequentially
        self.assertIsNone(rt.sweep(99))
        self.assertIsNotNone(rt.sweep(100))
        self.assertIsNotNone(rt.sweep(199))
        self.assertIsNone(rt.sweep(200)) # end is exclusive in RangeTable


class TestTimezoneEngine(unittest.TestCase):
    def test_tzfpy_lookup(self):
        if isinstance(sys.modules.get("tzfpy"), MagicMock):
            self.skipTest("tzfpy is not installed (running in stub mode)")
        from tzfpy import get_tz
        # Jakarta: -6.2, 106.8
        tz = get_tz(106.8, -6.2)
        self.assertEqual(tz, "Asia/Jakarta")

        # Tokyo: 35.6, 139.7
        tz_tokyo = get_tz(139.7, 35.6)
        self.assertEqual(tz_tokyo, "Asia/Tokyo")


class TestIndonesiaResolution(unittest.TestCase):
    def test_resolve_region_city_winner(self):
        all_data = {
            "ip2location": ("ID", "-6.20", "106.84", True, "Jakarta Raya", "Jakarta"),
            "dbip": ("ID", "-6.21", "106.85", True, "Jakarta", "Jakarta"),
        }
        reg, city = resolve_region_city(all_data, "ip2location", ["ip2location", "dbip"])
        self.assertEqual(reg, "Jakarta Raya")
        self.assertEqual(city, "Jakarta")

    def test_resolve_region_city_fallback(self):
        # Winning source only had country-level info, but another source had details
        all_data = {
            "ip2location": ("ID", "-6.20", "106.84", False, "", ""),
            "dbip": ("ID", "-6.21", "106.85", True, "Jawa Barat", "Bandung"),
        }
        reg, city = resolve_region_city(all_data, "ip2location", ["ip2location", "dbip"])
        self.assertEqual(reg, "Jawa Barat")
        self.assertEqual(city, "Bandung")

    def test_pick_winner_id_vs_foreign(self):
        merge_config = {
            "coord_spread_threshold": 2,
            "coord_priority": ["ip2location", "dbip"],
        }
        # Indonesian IP
        all_data_id = {
            "ip2location": ("ID", "-6.208", "106.845", True, "Jakarta Raya", "Jakarta"),
            "dbip": ("ID", "-6.209", "106.846", True, "Jakarta", "Jakarta"),
        }
        winner = pick_winner(all_data_id, {"ip2location", "dbip"}, merge_config)
        self.assertIsNotNone(winner)
        cc, lat, lon, reg, city, label = winner
        self.assertEqual(cc, "ID")
        self.assertEqual(reg, "Jakarta Raya")
        self.assertEqual(city, "Jakarta")

        # Foreign IP (US) - MUST NOT have region or city populated
        all_data_us = {
            "ip2location": ("US", "37.75", "-122.4", True, "", ""),
            "dbip": ("US", "37.76", "-122.41", True, "", ""),
        }
        winner_us = pick_winner(all_data_us, {"ip2location", "dbip"}, merge_config)
        self.assertIsNotNone(winner_us)
        cc_us, lat_us, lon_us, reg_us, city_us, label_us = winner_us
        self.assertEqual(cc_us, "US")
        self.assertEqual(reg_us, "")
        self.assertEqual(city_us, "")


class TestMMDBOutputStructure(unittest.TestCase):
    def test_convert_id_detailed_vs_foreign_minimal(self):
        import tempfile
        import shutil

        temp_dir = tempfile.mkdtemp()
        tsv_path = os.path.join(temp_dir, "test.tsv")
        mmdb_path = os.path.join(temp_dir, "test.mmdb")

        try:
            from mmdb_writer import MMDBWriter
            import maxminddb

            # Create test TSV with 1 ID row (with region & city) and 1 US row (no region & city)
            # 103.10.60.0 -> 103.10.60.255: hex 670a3c00 - 670a3cff (ID)
            # 8.8.8.0 -> 8.8.8.255: hex 8080800 - 80808ff (US)
            with open(tsv_path, "w", encoding="utf-8") as f:
                f.write("670a3c00\t670a3cff\tID\t-6.2088\t106.8456\tJakarta Raya\tJakarta\n")
                f.write("8080800\t80808ff\tUS\t37.7510\t-97.8220\n")

            writer = MMDBWriter(ip_version=4, database_type="GeoIP2-City")
            count = process_file(tsv_path, writer, ipv6=False)
            self.assertEqual(count, 2)
            writer.to_db_file(mmdb_path)

            with maxminddb.open_database(mmdb_path) as reader:
                # 1. Indonesia query
                rec_id = reader.get("103.10.60.1")
                self.assertIsNotNone(rec_id)
                self.assertEqual(rec_id["country"]["iso_code"], "ID")
                self.assertIn("city", rec_id)
                self.assertEqual(rec_id["city"]["names"]["en"], "Jakarta")
                self.assertIn("subdivisions", rec_id)
                self.assertEqual(rec_id["subdivisions"][0]["names"]["en"], "Jakarta Raya")
                self.assertEqual(rec_id["location"]["time_zone"], "Asia/Jakarta")

                # 2. US query (must NOT have city or subdivisions)
                rec_us = reader.get("8.8.8.1")
                self.assertIsNotNone(rec_us)
                self.assertEqual(rec_us["country"]["iso_code"], "US")
                self.assertNotIn("city", rec_us)
                self.assertNotIn("subdivisions", rec_us)
                self.assertEqual(rec_us["location"]["time_zone"], "America/Chicago")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
