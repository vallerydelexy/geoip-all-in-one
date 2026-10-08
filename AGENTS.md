# AGENTS.md — GeoIP All-in-One Data Pipeline

## 1. Ringkasan & Visi Proyek
Proyek berbasis **Python Data Pipeline** yang mengunduh data geolocation dari berbagai sumber publik (IP2Location LITE, GeoLite2, DB-IP Lite, ip-location-db Whois/ASN, IPinfo, IPlocate), menggabungkannya (*merge*) menggunakan algoritma voting & penentuan prioritas, menghitung zona waktu (*timezone*) via koordinat, dan menghasilkan database biner tunggal **MaxMind DB (`.mmdb`)** yang ringkas dan akurat.

## ⚡ Core Policy: 100% Autonomous YOLO "YES" & Script Encapsulation
Sama seperti standar workflow proyek lainnya, proyek ini memberlakukan **Universal YOLO "YES"**:
- Eksekusi command shell (PowerShell/Bash), Python scripts, `make` targets, pembuatan dan modifikasi file adalah **100% PRE-APPROVED**.
- **HANYA TANYA JIKA:**
  - Menghapus raw dataset secara permanen tanpa backup/re-fetch (`rm -rf data/*`).
  - Menghapus file skrip inti (`scripts/download.py`, `scripts/merge.py`, `scripts/convert.py`) atau konfigurasi (`rules.yml`, `sources.yaml`).
- Script pembantu atau pengujian baru WAJIB dienkapsulasi dengan rapi dalam folder `scripts/` atau `.agents/scripts/`.

## 2. Arsitektur Pipeline & Komponen Proyek
Pipeline terdiri dari 3 tahap utama yang diorkestrasi via `Makefile`:

1. **Download Stage (`scripts/download.py`):**
   - Mengunduh dataset IPv4 & IPv6 berdasarkan entri di `sources.yaml`.
   - Streaming HTTP request dengan deteksi otomatis berkas ZIP & ekstraksi TSV/CSV ke direktori `data/ipv4/` dan `data/ipv6/`.
2. **Merge Stage (`scripts/merge.py`):**
   - Membaca dan menormalisasi IP ranges ke dalam struktur `RangeTable` (sweep-line cursor).
   - Menjalankan algoritma voting negara (mengikuti preferensi dan tiebreak di `rules.yml`).
   - Memilih koordinat (latitude/longitude) menggunakan centroid cluster atau urutan prioritas (`coord_priority` / `coord_tiebreak`).
   - Menghasilkan intermediate TSV: `merged_ipv4.tsv` dan `merged_ipv6.tsv`.
3. **Convert Stage (`scripts/convert.py`):**
   - Mengonversi range IP dari format heksadesimal ke objek `netaddr.IPSet`.
   - Menghitung zona waktu secara presisi dari lat/lon menggunakan engine `tzfpy`.
   - Menulis output final menggunakan `MMDBWriter` ke format `GeoIP2-City`: `geoip_ipv4.mmdb`, `geoip_ipv6.mmdb`, dan database gabungan `geoip.mmdb`.

## 3. Tech Stack Specification
- **Runtime:** Python 3.10+ (disarankan Python 3.11)
- **Core Libraries:**
  - `mmdb_writer`: Kompiler file format MaxMind DB (`.mmdb`)
  - `tzfpy`: Penghitung zona waktu cepat dari koordinat
  - `netaddr`: Manipulasi alamat IP dan CIDR block
  - `pyyaml`: Parser file konfigurasi `sources.yaml` dan `rules.yml`
  - `requests`: HTTP client untuk unduhan sumber data
- **Build & Automation:** `Makefile` & GitHub Actions (`.github/workflows/build.yml`)
- **Package Manager:** `pip`

## 4. Standar Penulisan & Optimasi Kode
- **Efisiensi Memori & Kecepatan:** Pemrosesan IP mencakup jutaan baris; wajib perhatikan konsumsi RAM. Gunakan `__slots__` pada struktur data berulang, operasi bit-shift untuk konversi IP, dan hindari buffering data raksasa dalam memori jika dapat diproses secara streaming.
- **Integritas Aturan & Deterministik:** Perubahan logika voting wajib selaras dengan skema `rules.yml` dan menghasilkan output yang deterministik (dapat direproduksi).
- **Format Output:** File `.mmdb` diformat sebagai tipe `GeoIP2-City` yang hanya menyimpan atribut esensial (`country.iso_code`, `location.latitude`, `location.longitude`, `location.time_zone`) demi efisiensi ukuran file.
- **Cross-Platform:** Skrip harus kompatibel dijalankan di lingkungan Linux (CI/Ubuntu) maupun Windows lokal.
