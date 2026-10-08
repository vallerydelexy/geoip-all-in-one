---
name: geoip-pipeline
description: >
  GeoIP All-in-One Data Pipeline Workflow and Automation. Cheatsheet and procedure
  for running download, merge with voting algorithm, timezone resolution, MMDB compilation,
  and local sanity verification.
---

# GeoIP All-in-One Pipeline Workflow

Panduan komprehensif menjalankan, men-debug, dan memverifikasi siklus hidup pipeline data GeoIP.

---

## 🔄 Tahapan Pipeline Utama

### 1. Download Stage (`scripts/download.py`)
Mengunduh sumber data yang terdaftar di `sources.yaml` untuk IPv4 atau IPv6.
```bash
python scripts/download.py sources.yaml ipv4 data/ipv4
python scripts/download.py sources.yaml ipv6 data/ipv6
```
- Deteksi berkas ZIP otomatis (unzip file CSV/TSV secara langsung).
- Output disimpan di `data/ipv4/` dan `data/ipv6/`.

### 2. Merge Stage (`scripts/merge.py`)
Membaca dataset, menyusun `RangeTable`, menjalankan voting negara & penentuan koordinat.
```bash
python scripts/merge.py sources.yaml ipv4 data/ipv4 merged_ipv4.tsv
python scripts/merge.py sources.yaml ipv6 data/ipv6 merged_ipv6.tsv
```
- Aturan voting dan prioritas dikendalikan oleh `rules.yml`.
- Output berupa TSV 5-kolom: `start_hex \t end_hex \t country \t lat \t lon`.

### 3. Convert Stage (`scripts/convert.py`)
Mengonversi rentang IP dari format heksadesimal ke `.mmdb` dan mengkalkulasi zona waktu dari koordinat menggunakan `tzfpy`.
```bash
# Build database per versi:
python scripts/convert.py merged_ipv4.tsv geoip_ipv4.mmdb 4
python scripts/convert.py merged_ipv6.tsv geoip_ipv6.mmdb 6

# Build database gabungan (IPv4 + IPv6):
python scripts/convert.py merged_ipv4.tsv merged_ipv6.tsv geoip.mmdb
```

---

## 🛠️ Makefile Shortcuts
```bash
# Install seluruh dependensi Python
make deps

# Jalankan seluruh pipeline (download, merge, convert ke geoip.mmdb)
make all

# Jalankan parsial
make download-ipv4
make merge
make convert
make clean
```

---

## 🔍 Testing & Verifikasi Cepat (Enkapsulasi)

Untuk pengujian tanpa memicu dialog konfirmasi terminal:
```bash
# 1. Jalankan unit test algoritma merge & range table:
python .agents/scripts/run_pipeline_tests.py

# 2. Verifikasi isi berkas MMDB yang dihasilkan:
python .agents/scripts/verify_mmdb.py geoip.mmdb

# 3. Analisis statistik berkas intermediate TSV:
python .agents/scripts/inspect_tsv.py merged_ipv4.tsv
```
