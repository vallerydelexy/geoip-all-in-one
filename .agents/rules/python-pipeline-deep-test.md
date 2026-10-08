---
trigger: always_on
description: Python GeoIP Pipeline Deep Testing Policy. All modifications to merge algorithms, download streaming, RangeTable, coordinate tiebreaks, or MMDB writer conversion must be verified using rigorous test suites and binary inspection in .agents/scripts/.
---

# Python GeoIP Pipeline Deep Testing Policy (`python-pipeline-deep-test.md`)

Aturan ini mengatur standar mutlak pengujian **Deep Test & Verifikasi Deterministik** di seluruh basis kode data pipeline GeoIP.

---

## 🚀 Core Policy: 100% Verification & Deep Test Mandate

Setiap modifikasi logika pada `scripts/merge.py`, `scripts/download.py`, `scripts/convert.py`, maupun konfigurasi `rules.yml` **WAJIB diverifikasi secara fungsional** sebelum dinyatakan selesai.

### 1. Sweep-Line RangeTable & Overlap Testing
- Uji struktur `RangeTable` untuk rentang IP non-overlapping, overlapping sebagian, dan sub-rentang (nested CIDR block).
- Pastikan kursor sequential sweep-line berjalan deterministik tanpa kehilangan rentang IP batas (*boundary conditions*: `0.0.0.0`, `255.255.255.255`, `::`, `ffff:...`).

### 2. Country Voting & Tiebreak Priority
- Uji skenario voting negara:
  - Konsensus mutlak (semua sumber setuju).
  - Suara mayoritas vs minoritas.
  - Skenario seri (*tie*): pastikan urutan prioritas di `rules.yml` (`vote_priority`) dihormati secara presisi.

### 3. Coordinate Selection & Centroid Spread
- Uji seleksi latitude/longitude:
  - Bila 3 sumber kota sepakat negara yang sama, evaluasi jarak spread terhadap `coord_spread_threshold`.
  - Bila hanya 2 sumber tersedia atau spread melebihi threshold, pastikan urutan `coord_tiebreak` terpilih dengan tepat.

### 4. Binary MMDB Lookup & Timezone Verification
- Setelah file intermediate TSV dikonversi ke `.mmdb`:
  - Lakukan pembacaan (*lookup*) sample IP IPv4 dan IPv6 menggunakan library reader (`maxminddb` atau verifikasi reader).
  - Validasi bahwa payload yang dihasilkan memuat:
    - `country.iso_code` (string 2 huruf)
    - `location.latitude` (float)
    - `location.longitude` (float)
    - `location.time_zone` (string IANA timezone dari `tzfpy`)
- Pastikan tidak ada field payload asing yang membengkakkan ukuran database biner.

### 5. Eksekusi Pengujian Terenkapsulasi
- Jalankan suite pengujian melalui skrip statis:
  ```bash
  python .agents/scripts/run_pipeline_tests.py
  ```
  dan untuk verifikasi database biner:
  ```bash
  python .agents/scripts/verify_mmdb.py <path_to_mmdb>
  ```
