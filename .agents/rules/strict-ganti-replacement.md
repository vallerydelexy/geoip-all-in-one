---
trigger: always_on
description: Strict Ganti Replacement Policy. When user says 'ganti', 'rename', 'ubah', or 'refactor', previous files, functions, variables, configurations, or modules MUST be truly deleted permanently. Zero backward compatibility, zero re-export stubs, zero legacy aliases, and zero leftovers.
---

# Strict 'Ganti' Replacement Policy (`strict-ganti-replacement.md`)

Aturan ini mengatur standar mutlak ketika user menginstruksikan **"ganti"**, **"rename"**, **"ubah"**, atau **"refactor"** terhadap suatu file, fungsi, kelas, konfigurasi, skrip, atau variabel di seluruh repositori **GeoIP All-in-One**.

---

## 🚀 Core Policy: Zero Backward Compatibility & Real Removal

> **"Kalau saya bilang 'ganti' berarti file atau variable sebelumnya beneran di-hapus, jangan ada istilah 'backward'. User TIDAK AKAN PERNAH backward kalau sudah bilang 'ganti'. Dilarang keras menyisakan hasil ganti."**

---

## ⛔ DILARANG KERAS: Segala Bentuk "Backward Compatibility"

Ketika user memerintahkan "ganti" atau "rename", agen **DILARANG KERAS** melakukan hal-hal berikut:

1. **Dilarang Membuat File Stub / Bridge Re-export**:
   - ❌ **Dilarang**: Menyisakan file skrip lama lalu menulis import/export pembungkus ke skrip baru.
   - ✅ **Wajib**: File fisik lama **BENERAN DIHAPUS** secara permanen dari sistem berkas (`rm` / `git rm`).
2. **Dilarang Membuat Alias Variabel / Function / Class Legacy**:
   - ❌ **Dilarang**: `old_function_name = new_function_name` atau menjaga wrapper lama.
   - ✅ **Wajib**: Hanya gunakan nama baru. Perbarui seluruh referensi kode pemanggil secara tuntas.
3. **Dilarang Menyisakan Konfigurasi Ganda**:
   - ❌ **Dilarang**: Menyisakan key lama di `sources.yaml` atau `rules.yml` berdampingan dengan key baru untuk fallback.
   - ✅ **Wajib**: Perbarui skema konfigurasi langsung ke entri baru.
4. **Dilarang Menyisakan Komentar / Anotasi Deprecated**:
   - ❌ **Dilarang**: Memberi komentar `# deprecated: use new one` atau fallback bersarang.
   - ✅ **Wajib**: Bersihkan langsung seluruh sisa kode lama.
