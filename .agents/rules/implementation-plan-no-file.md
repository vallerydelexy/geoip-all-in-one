---
trigger: always_on
description: Implementation Plan & Task Artifact Policy. Use Antigravity IDE Artifacts with RequestFeedback=true for implementation plans (Proceed button), followed by task.md for task tracking upon Proceed. NEVER create or modify PLAN.md in the project workspace.
---

# Implementation Plan & Task Artifact Policy: Antigravity IDE Artifacts (Proceed Button & task.md)

Aturan ini mengatur standar mutlak ketika user meminta **"implementation plan"**, **"buat implementation plan"**, atau **"bikin plan"** dan alur eksekusinya.

---

## 🚀 Core Policy: Gunakan Antigravity IDE Artifact (Proceed & task.md)

> **"Kalau user minta 'implementation plan', buat Artifact `<appDataDir>/brain/<conversation-id>/implementation_plan.md` dengan parameter `RequestFeedback: true` (sehingga muncul tombol interaktif 'Proceed' di UI Antigravity). Ketika di-Proceed / disetujui, agen WAJIB membuat Task Artifact `<appDataDir>/brain/<conversation-id>/task.md` untuk melacak eksekusi bertahap. DILARANG KERAS membuat file `PLAN.md` di root workspace proyek."**

---

## ⛔ DILARANG KERAS:

1. **Dilarang Menulis / Membuat File `PLAN.md` di Root Workspace**:
   - ❌ **Dilarang**: Menggunakan `write_to_file` ke `PLAN.md`, `PLANNING.md`, dsb di workspace.
   - ✅ **Wajib**: Tulis file rencana dan task ke direktori artefak IDE:
     - Rencana: `<appDataDir>/brain/<conversation-id>/implementation_plan.md`
     - Task: `<appDataDir>/brain/<conversation-id>/task.md`
2. **Dilarang Mengotori Workspace Repo dengan File Scratch/Planning**:
   - Seluruh file dokumen artefak perencanaan dan tracking IDE wajib berada di dalam artifact directory IDE, bukan di root repository.

---

## 📋 Prosedur Standar Alur Perencanaan & Eksekusi:

1. **Tahap 1: Buat Artifact `implementation_plan.md` (Tombol "Proceed")**:
   - Path: `<appDataDir>/brain/<conversation-id>/implementation_plan.md`
   - Metadata:
     ```json
     "ArtifactMetadata": {
       "RequestFeedback": true,
       "Summary": "Rangkuman rencana implementasi...",
       "UserFacing": true
     }
     ```
   - Antigravity IDE akan menampilkan tombol **"Proceed"** di panel Artifact UI.

2. **Tahap 2: Saat "Proceed" Ditekan / Disetujui -> WAJIB Buat Task Artifact `task.md`**:
   - Path: `<appDataDir>/brain/<conversation-id>/task.md`
   - Metadata:
     ```json
     "ArtifactMetadata": {
       "RequestFeedback": false,
       "Summary": "Task checklist progress eksekusi...",
       "UserFacing": true
     }
     ```
   - Isi file berisi daftar checklist berformat GitHub markdown (`- [ ]`, `- [/]`, `- [x]`) per fase implementasi.
   - Agen wajib mengupdate centang `- [x]` di `task.md` seiring berjalannya progres eksekusi hingga selesai.
