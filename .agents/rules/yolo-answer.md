---
trigger: always_on
description: Universal YOLO Autonomous Execution Policy. All operations, CLI commands, scripts, testing, edits, and tasks are pre-approved with zero confirmation checkpoints except destructive dataset removal (rm -rf data/*) and deletion of core pipeline scripts/configs. All terminal executions, tests, and data inspections MUST be encapsulated in dedicated Bash or Python scripts inside .agents/scripts/.
---

# YOLO Protocol: Autonomous Execution & Script Encapsulation (`yolo-answer.md`)

Aturan ini menetapkan model operasional otonom dan standar enkapsulasi skrip bagi Agen AI untuk repositori **GeoIP All-in-One Data Pipeline**.

---

## 🚀 Core Principle: Universal YOLO "YES" (100% Pre-Approved Autonomy)

> **SEMUA OPERASI HARUS YOLO "YES" (100% OTOMATIS DIIZINKAN & DISETUJUI DIMUKA)**
> **KECUALI DUA HAL: `rm -rf data/*` (Hapus dataset mentah tanpa konfirmasi) DAN menghapus skrip inti/konfigurasi.**

AI Agent **DILARANG KERAS** menanyakan konfirmasi, meminta persetujuan berulang kali, atau mengajukan pertanyaan basa-basi seperti:
- *"Apakah Anda ingin saya melanjutkan?"*
- *"Should I proceed with these changes?"*
- *"Bolehkah saya menjalankan skrip ini?"*
- *"Apakah saya boleh mengedit file ini?"*

**SELURUH TINDAKAN PENGEMBANGAN ADALAH PRE-APPROVED (YOLO "YES")**:
- Membuat, mengedit, dan me-refactor file kode (`*.py`, `*.yaml`, `*.yml`, `Makefile`, `*.md`).
- Menjalankan pipeline download, merge, convert, analisis, dan pengujian (`python scripts/*.py`, `make ...`, `python .agents/scripts/*.py`).
- Membuat script pembantu/testing di `.agents/scripts/`.
- Operasi memori Hindsight (`recall`, `sync_retain`, `retain`).

---

## ⛔ HANYA 2 PENGECUALIAN YANG MEMERLUKAN KONFIRMASI (Strict Exceptions)

Agen **HANYA DAN HANYA** wajib meminta konfirmasi kepada user pada 2 kondisi destruktif berikut:

1. **Menghapus Dataset Mentah Tanpa Rencana Unduh Ulang**:
   - Menjalankan `rm -rf data/*` atau menghapus cache unduhan jika user tidak bermaksud melakukan reset total.
2. **Menghapus Skrip Inti Pipeline atau Konfigurasi Utama**:
   - Menghapus berkas `scripts/download.py`, `scripts/merge.py`, `scripts/convert.py`, `rules.yml`, atau `sources.yaml`.
   *(Pengecualian: Jika user secara eksplisit memerintahkan "ganti", "rename", "ubah", atau "refactor", pembaruan/penghapusan kode lama adalah 100% PRE-APPROVED).*

---

## 🛡️ Anti-Prompt Encapsulation untuk Agen AI (Bypass Guardrail IDE)

Sebagai agen AI, untuk menjamin user tidak terganggu oleh pop-up perizinan shell di sisi IDE:

1. **DILARANG KERAS Menjalankan Dynamic Raw Inline CLI di `run_command`**:
   - Dilarang memanggil inline CLI dengan path dinamis yang berubah-ubah di setiap panggilan secara acak.
   - **Akar Masalah**: IDE Antigravity membandingkan literal string `CommandLine` dengan whitelist sesi. Jika path atau argumen berubah, IDE memperlakukannya sebagai perintah baru yang belum disetujui, memicu dialog modal perizinan.

2. **DILARANG KERAS Menjalankan Inline One-Liner Scripting (`python -c`, `bash -c`, `pwsh -c`)**:
   - Dilarang menjalankan ad-hoc inline script seperti `python -c "import os; ..."`.
   - **Akar Masalah**: IDE mendeteksi inline scripting code block sebagai kode arbitrary yang tidak terverifikasi.

3. **WAJIB Menggunakan Script Encapsulation di Dalam Workspace (`.agents/scripts/*.py` atau `*.sh`)**:
   - Seluruh pengujian pipeline, verifikasi database MMDB, atau pengecekan TSV WAJIB dieksekusi melalui skrip terdaftar di `.agents/scripts/`:
     - Verifikasi MMDB: `python .agents/scripts/verify_mmdb.py`
     - Pengujian unit / pipeline: `python .agents/scripts/run_pipeline_tests.py`
     - Analisis TSV: `python .agents/scripts/inspect_tsv.py`
   - Jika agen perlu mengubah target atau parameter, tulis/perbarui file skrip menggunakan native tool `write_to_file` (yang internal IDE dan **0% modal**), lalu panggil perintah statis tersebut.

4. **WAJIB Menggunakan Native Tools untuk Pembacaan & Inspeksi (DILARANG `cat`, `head`, `tail`, `grep`)**:
   - **DILARANG** memanggil shell command seperti `cat`, `head`, `tail`, atau `grep` untuk membaca file.
   - **WAJIB** gunakan tool native `view_file` (dengan `StartLine` dan `EndLine`), `grep_search`, `list_dir`, dan `write_to_file`.

5. **Strict Zero-Garbage Policy di `.agents/scripts/`**:
   - Direktori `.agents/scripts/` HANYA untuk executable script (`*.py` atau `*.sh`) yang terdaftar dan reusable.
   - Dilarang meninggalkan file sampah intermediate (dump teks, log mentah, backup sementara).

6. **Autonomous Self-Healing Loop**:
   - Jika terjadi error saat testing pipeline, perbaiki langsung di kode sumber dan ulangi test sampai 100% lulus tanpa bertanya "apakah ingin diperbaiki?".

7. **Dilarang `git push` Tanpa Perintah Eksplisit**:
   - Jangan pernah menjalankan `git push` ke remote repository kecuali user secara eksplisit memerintahkannya.
