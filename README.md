# GeoIP All in One

This downloads geolocation sources, merges them using a deterministic voting and centroid algorithm, resolves timezones from coordinates, and outputs a compact MaxMind DB (`.mmdb`) file.

Releases are built weekly.

---

### Features & Output Schema

* **Format**: MaxMind DB (`GeoIP2-City` database type).
* **Global records**: Compact footprint containing `country.iso_code`, `location.latitude`, `location.longitude`, and `location.time_zone`.
* **Indonesia (`ID`) records**: Granular place details including `city.names.en` and `subdivisions[].names.en` (state/province) alongside coordinates and timezone.

---

### City sources

Longitude and latitude:

- [IP2Location LITE](https://lite.ip2location.com)
- [GeoLite2](https://www.maxmind.com)
- [DB-IP Lite](https://db-ip.com)

### Country sources

These are additionally used to help vote on which city source to use for a given IP range:

- [ip-location-db GeoFeed + Whois + ASN database](https://github.com/tdulcet/ip-geolocation-dbs?tab=readme-ov-file#geofeed--whois--asn-database) (Created by merging the five [Regional Internet Registries](https://en.wikipedia.org/wiki/Regional_Internet_registry) (RIRs) ([AFRINIC](https://afrinic.net/), [APNIC](https://www.apnic.net/), [ARIN](https://www.arin.net/), [LACNIC](https://www.lacnic.net/), [RIPE NCC](https://www.ripe.net/)) IP-ASN, WHOIS and [OpenGeoFeed](https://opengeofeed.org/) databases)
- [IPinfo\.io](https://ipinfo.io)
- [IPlocate](https://iplocate.io)

### Timezone data

Calculated from coordinates using [tzfpy](https://github.com/ringsaturn/tzfpy).

---

## Quick Start & Pipeline Execution

### 1. Environment Setup

Create and activate a virtual environment (Python 3.10+ recommended, e.g. Python 3.11):

**Windows (PowerShell):**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Run Entire Pipeline (Automated via Make)

If you have `make` installed:

```bash
# Build combined geoip.mmdb, geoip_ipv4.mmdb, and geoip_ipv6.mmdb
make

# Or run individual stages:
make download    # Stage 1: Download raw datasets to data/
make merge       # Stage 2: Merge into intermediate TSVs (merged_ipv4.tsv, merged_ipv6.tsv)
make convert     # Stage 3: Convert TSVs into final .mmdb files
```

---

### 3. Run Pipeline Manually (Direct CLI / PowerShell)

You can run each stage directly with Python:

#### Step 1: Download Datasets
```powershell
python scripts/download.py sources.yaml ipv4 data/ipv4
python scripts/download.py sources.yaml ipv6 data/ipv6
```

#### Step 2: Merge & Vote
Processes IP ranges, runs voting, centroid calculation, and Indonesia city/province resolution:
```powershell
python scripts/merge.py sources.yaml ipv4 data/ipv4 merged_ipv4.tsv
python scripts/merge.py sources.yaml ipv6 data/ipv6 merged_ipv6.tsv
```

#### Step 3: Convert to MMDB & Compute Timezones
```powershell
# Combined database (IPv4 + IPv6)
python scripts/convert.py merged_ipv4.tsv merged_ipv6.tsv geoip.mmdb

# Or individual versions
python scripts/convert.py merged_ipv4.tsv geoip_ipv4.mmdb 4
python scripts/convert.py merged_ipv6.tsv geoip_ipv6.mmdb 6
```

#### Step 4: Verify Database & Run Tests
```powershell
# Inspect and verify IP lookups against the generated MMDB
python .agents/scripts/verify_mmdb.py geoip.mmdb

# Run pipeline deep tests
python .agents/scripts/run_pipeline_tests.py
```

---

### 4. How to Restart / Reset from Scratch

To clean up downloaded caches, intermediate TSVs, and compiled MMDB files so the pipeline downloads and builds fresh:

**Using Make:**
```bash
make clean
make
```

**Using PowerShell:**
```powershell
Remove-Item -Recurse -Force data, *.tsv, *.mmdb -ErrorAction SilentlyContinue
```

Then re-run Step 1 through Step 3 above.

---

## Merge Algorithm

1. For each IP range, all 6 sources vote on a country code.
2. The winning country is used to narrow down coordinate sources.
3. Coordinates are selected via `coord_priority` (`ip2location` > `dbip` > `geolite2`). If all 3 city sources agree on country, a centroid/center point within `coord_spread_threshold` is chosen.
4. For **Indonesia (`ID`)**, the winning coordinate source provides the detailed city and state/province names, falling back to other agreeing sources if missing. For all other countries, place names are left empty to keep the database size lightweight.

---

## Licenses

| Source           | Attribution                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------- |
| IP2Location LITE | This project uses the IP2Location LITE database for [IP geolocation](https://lite.ip2location.com). |
| GeoLite2         | This product includes GeoLite2 Data created by MaxMind, available from https://www.maxmind.com/.    |
| DB-IP Lite       | [IP Geolocation by DB-IP](https://db-ip.com)                                                        |

## Sources

- [tdulcet/ip-geolocation-dbs](https://github.com/tdulcet/ip-geolocation-dbs)
- [sapics/ip-location-db](https://github.com/sapics/ip-location-db)
