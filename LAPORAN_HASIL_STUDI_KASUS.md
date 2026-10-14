# LAPORAN PENYELESAIAN STUDI KASUS MANUFAKTUR ERPNEXT
**Perusahaan**: AnggiST / PT Anggi Karya Manufaktur  
**Produk Utama**: Kursi Kantor Ergonomis Tipe Nexus (`FG-KURSI-01`)  
**Mata Uang**: IDR (Rupiah)  
**Status**: SELESAI 100% (Semua 5 Soal Terverifikasi)

---

## Ringkasan Eksekusi Siklus Bisnis

```
[1. Master Data & Saldo Awal] 
   └── 10 Komponen Material (Rp 35.000.000) masuk ke Gudang Bahan Baku
[2. Workstation, Operation & BOM]
   └── 3 WS, 3 Operasi, HPP Standar Kursi: Rp 745.000 / unit
[3. Procurement Flow]
   └── PO-SIM-001 (Rp 4.900.000) -> Material Masuk -> Hutang Dagang Diakui
[4. Manufacturing Execution]
   └── SPK 10 Unit Kursi -> Transfer Bahan ke WIP -> Job Cards Selesai -> Kursi Masuk Gudang Barang Jadi (HPP: Rp 765.000 / unit)
[5. Penjualan & Laba Kotor]
   └── SO-SIM-001 -> Pengiriman 10 Unit Kursi -> Faktur Penjualan Rp 12.500.000 -> Laba Kotor: Rp 4.850.000 (Margin 38,80%)
```

---

## 1. Hasil Pengerjaan Soal 1 (Modul Stock)
* **Item Groups**: `Bahan Baku`, `Barang Jadi`, `Bahan Kemasan`, `Barang Setengah Jadi`, `Sub-Assembly`.
* **Gudang (Warehouses)**:
  * `Gudang Bahan Baku - A`
  * `Gudang Work In Progress - A`
  * `Gudang Barang Jadi - A`
  * `Gudang Reject dan Scrap - A`
* **Pemasok**: PT Baja Mandiri Perkasa, CV Foam & Textile Nusantara, PT Mitra Hardware Indonesia, CV Karton Box Lestari.
* **Pelanggan**: PT Sejahtera Finansial Utama, Toko Mebel Modern Jaya, CV Digital Solusi Mandiri.
* **Master Items**: 2 Produk Jadi (`FG-KURSI-01`, `FG-KURSI-02`), 8 Bahan Baku, 2 Bahan Kemasan.
* **Saldo Awal Persediaan**:
  * Dokumen: `MAT-STE-2026-00001` (Material Receipt).
  * Gudang Target: `Gudang Bahan Baku - A`.
  * Total Nilai Saldo Awal: **Rp 35.000.000,00** (50 set komponen material lengkap).

---

## 2. Hasil Pengerjaan Soal 2 (Modul Manufacturing)
* **Workstations**:
  * `WS Potong & Jahit` (Tarif: Rp 45.000 / jam)
  * `WS Perakitan Utama` (Tarif: Rp 50.000 / jam)
  * `WS QC & Packaging` (Tarif: Rp 35.000 / jam)
* **Operations**:
  * `OP-JAHIT-BUSA`
  * `OP-ASSEMBLY-FRAME`
  * `OP-QC-PACKING`
* **Bill of Materials (BOM)**:
  * Dokumen: `BOM-FG-KURSI-01-001` (Status: *Default & Active*).
  * Biaya Bahan Baku per Unit: Rp 700.000,00
  * Biaya Operasi per Unit: Rp 45.000,00 (total 60 menit)
  * **HPP Standar per Unit**: **Rp 745.000,00 / unit**.

---

## 3. Hasil Pengerjaan Soal 3 (Modul Buying & Stock)
* **Purchase Order (PO)**:
  * No. Dokumen: `PUR-ORD-2026-00011` (Ref: `PO-SIM-001`).
  * Vendor: `PT Baja Mandiri Perkasa`.
  * Barang: 20 unit `RM-RANGKA-01` & 20 unit `RM-BASE-01`.
  * Total Nilai: **Rp 4.900.000,00**.
* **Purchase Receipt (PR)**:
  * No. Dokumen: `MAT-PRE-2026-00001`.
  * Menambah stok di `Gudang Bahan Baku - A` (Rangka & Kaki Bintang masing-masing menjadi 70 unit).
* **Purchase Invoice (PI)**:
  * No. Dokumen: `ACC-PINV-2026-00007` (Ref Vendor: `INV-BMP-2026/09`).
  * Mengakui hutang ke `2111.001 - Hutang Dagang Dalam Negeri - A` sebesar **Rp 4.900.000,00**.

---

## 4. Hasil Pengerjaan Soal 4 (Modul Manufacturing Execution)
* **Work Order (WO)**:
  * No. Dokumen: `MFG-WO-2026-00001`.
  * Target: **10 Unit** `FG-KURSI-01`.
  * Status: **COMPLETED** (Produced: 10 / 10 Unit).
* **Material Transfer for Manufacture**:
  * No. Dokumen: `MAT-STE-2026-00002` (Transfer 10 set bahan baku ke Gudang WIP).
* **Job Cards**:
  * `PO-JOB00001` (Seq 1: OP-JAHIT-BUSA) -> Selesai.
  * `PO-JOB00002` (Seq 2: OP-ASSEMBLY-FRAME) -> Selesai.
  * `PO-JOB00003` (Seq 3: OP-QC-PACKING) -> Selesai.
* **Manufacture / Finish**:
  * No. Dokumen: `MAT-STE-2026-00003`.
  * Menghasilkan **10 Unit Kursi Jadi** di `Gudang Barang Jadi - A`.
  * HPP Realisasi: **Rp 765.000,00 / unit** (Total Nilai Barang Jadi: Rp 7.650.000,00).

---

## 5. Hasil Pengerjaan Soal 5 (Modul Selling & Accounting)
* **Sales Order (SO)**:
  * No. Dokumen: `SAL-ORD-2026-00006` (Ref: `SO-SIM-001`).
  * Pelanggan: `PT Sejahtera Finansial Utama`.
  * Pesanan: 10 Unit Kursi @ Rp 1.250.000,00.
  * Total Nilai: **Rp 12.500.000,00**.
* **Delivery Note (Surat Jalan)**:
  * No. Dokumen: `MAT-DN-2026-00001`.
  * Mengirimkan 10 unit kursi dari Gudang Barang Jadi ke pelanggan.
* **Sales Invoice (Faktur Penjualan)**:
  * No. Dokumen: `ACC-SINV-2026-00006`.
  * Piutang diakui di `1131.0010 - Piutang Dagang - A` sebesar **Rp 12.500.000,00**.

---

## 6. Analisis Perhitungan Laba Kotor (Gross Profit)

| Komponen Analisis | Nilai (IDR) | Persentase (%) |
|---|---|---|
| Pendapatan Penjualan (10 Unit @ Rp 1.250.000) | Rp 12.500.000,00 | 100,00 % |
| Harga Pokok Penjualan (10 Unit @ Rp 765.000) | Rp 7.650.000,00 | 61,20 % |
| **Laba Kotor (Gross Profit)** | **Rp 4.850.000,00** | **38,80 %** |

**Kesimpulan:**  
Perusahaan berhasil membukukan laba kotor sebesar **Rp 4.850.000,00** dari penjualan 10 unit kursi kantor ergonomis dengan margin laba kotor yang sangat sehat yaitu **38,80%**.
