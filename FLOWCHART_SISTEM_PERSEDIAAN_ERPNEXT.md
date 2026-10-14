# STANDAR OPERASIONAL PROSEDUR & FLOWCHART SISTEM PERSEDIAAN TERPADU ERPNEXT
**Studi Kasus Manufaktur**: PT Anggi Karya Manufaktur (AnggiST)  
**Produk Utama**: Kursi Kantor Ergonomis Tipe Nexus (`FG-KURSI-01`)  
**Format Dokumen Word**: [FLOWCHART_SISTEM_PERSEDIAAN_ERPNEXT.docx](file:///c:/Users/User/OneDrive/Documents/ERP/ERP_Anggi/FLOWCHART_SISTEM_PERSEDIAAN_ERPNEXT.docx)  
**File Diagram Visual (300 DPI)**: [flowchart_persediaan_lanjutan.png](file:///c:/Users/User/OneDrive/Documents/ERP/ERP_Anggi/flowchart_persediaan_lanjutan.png)

---

## 1. Outline Rinci Alur Sistem Persediaan ERPNext

### Tahap 1: Inbound / Penerimaan Bahan Baku
* **Penerimaan dari Supplier**: Saat vendor mengirimkan material (seperti rangka besi, busa jok, silinder gaslift, set roda, baut, kardus), departemen gudang menerbitkan dokumen **Purchase Receipt (PR)**. Transaksi ini secara otomatis menambah kuantitas dan nilai fisik di **Gudang Bahan Baku - A**.
* **Penerimaan Saldo Awal / Penyesuaian**: Untuk pengisian stok awal operasional atau koreksi fisik manual, digunakan dokumen **Stock Entry (tipe Material Receipt)**.

### Tahap 2: Internal Movement / Transfer Material ke WIP
* **Perencanaan Produksi**: Penerbitan dokumen **Work Order (WO)** sebagai perintah kerja mengacu pada formula resep **BOM (BOM-FG-KURSI-01-001)**.
* **Transfer Material**: Bahan baku dipindahkan dari Gudang Bahan Baku - A ke **Gudang WIP - A** menggunakan dokumen **Stock Entry (tipe Material Transfer for Manufacture)**.

### Tahap 3: Transformasi Produksi & Stasiun Kerja (Workstations)
Proses perakitan dieksekusi secara berurutan menggunakan dokumen **Job Cards** pada 3 stasiun kerja:
1. **WS Potong & Jahit** (`OP-JAHIT-BUSA`): Memotong busa dan menjahit kain mesh.
2. **WS Perakitan Utama** (`OP-ASSEMBLY-FRAME`): Merakit rangka, gaslift, armrest, dan kaki bintang.
3. **WS QC & Packaging** (`OP-QC-PACKING`): Pengujian mekanik dan pembungkusan kardus.

### Tahap 4: Kondisi Percabangan Quality Control (QC)
Di stasiun kerja QC & Packaging, dilakukan inspeksi kelayakan produk akhir:
* **Jika Lolos QC (Pass)**:
  * Sistem menerbitkan dokumen **Stock Entry (tipe Manufacture)**.
  * Memotong/mengonsumsi saldo seluruh bahan baku di **Gudang WIP - A** (saldo WIP kembali menjadi 0).
  * Menambah kuantitas produk jadi (**FG-KURSI-01**) di **Gudang Barang Jadi - A** dengan akumulasi HPP material dan jam kerja stasiun kerja.
* **Jika Reject / Material Cacat (Fail)**:
  * Komponen atau unit yang rusak dipindahkan ke **Gudang Reject dan Scrap - A** agar terisolasi dari jalur perakitan dan stok siap jual.

### Tahap 5: Outbound / Pengiriman Produk ke Pelanggan
* **Pengiriman Barang**: Berdasarkan **Sales Order**, diterbitkan dokumen **Delivery Note (DN)** yang mengurangkan kuantitas barang jadi dari **Gudang Barang Jadi - A** dan mendebit Beban Pokok Penjualan (HPP / Cost of Goods Sold).
* **Penagihan**: Bagian akuntansi menerbitkan **Sales Invoice** untuk mencatat piutang dan pendapatan penjualan resmi.

### Tahap 6: Pengendalian & Audit Persediaan
* Jika ditemukan selisih kuantitas saat opname berkala, dilakukan penyesuaian melalui dokumen **Stock Reconciliation**.

---

## 2. Diagram Flowchart Sintaks Mermaid

```mermaid
flowchart TD
    subgraph Inbound ["1. Inbound / Penerimaan Bahan Baku"]
        A[Supplier / Vendor] -->|Kirim Material| B[Purchase Receipt / PR]
        B --> C[(Gudang Bahan Baku - A)]
        D[Stock Entry: Material Receipt] -->|Saldo Awal / Opname| C
    end

    subgraph Internal ["2. Internal Movement / WIP Transfer"]
        E[Work Order / WO] -->|Acuan BOM| F[Stock Entry: Material Transfer for Manufacture]
        C -->|Ambil Bahan Baku| F
        F -->|Transfer Material| G[(Gudang WIP - A)]
    end

    subgraph Production ["3. Produksi & Stasiun Kerja (Job Cards)"]
        G --> H[WS Potong & Jahit<br/>OP-JAHIT-BUSA]
        H --> I[WS Perakitan Utama<br/>OP-ASSEMBLY-FRAME]
        I --> J[WS QC & Packaging<br/>OP-QC-PACKING]
        J --> K{Hasil Inspeksi QC?}
    end

    subgraph QC_Branch ["Kondisi Percabangan QC"]
        K -->|Lolos QC (Pass)| L[Stock Entry: Manufacture]
        L --> M[(Gudang Barang Jadi - A)]
        K -->|Reject / Cacat (Fail)| N[(Gudang Reject dan Scrap - A)]
    end

    subgraph Outbound ["4. Outbound / Fulfillment"]
        O[Sales Order] --> P[Delivery Note / DN]
        M -->|Ambil Finished Goods| P
        P -->|Kirim Produk| Q[Pelanggan / Customer]
        P --> R[Sales Invoice]
    end
```

---

## 3. Ringkasan Pemetaan Dokumen & Stasiun Kerja

| Tahapan Operasional | Stasiun Kerja (Workstation) | Dokumen ERPNext yang Terlibat | Gudang Terkait (Alur Mutasi) |
|---|---|---|---|
| **Penerimaan Material** | Area Penerimaan / Gudang | `Purchase Receipt (PR)`, `Stock Entry (Material Receipt)` | Supplier $\rightarrow$ Gudang Bahan Baku - A |
| **Transfer ke Produksi** | Lantai Produksi (Shop Floor) | `Work Order (WO)`, `Stock Entry (Material Transfer)` | Gudang Bahan Baku - A $\rightarrow$ Gudang WIP - A |
| **Pengerjaan & Perakitan** | 1. `OP-JAHIT-BUSA`<br>2. `OP-ASSEMBLY-FRAME`<br>3. `OP-QC-PACKING` | `Job Cards` (PO-JOB...), `BOM-FG-KURSI-01-001` | Gudang WIP - A (Internal Workstations) |
| **Keputusan QC: Lolos** | WS QC & Packaging | `Stock Entry (tipe Manufacture)` | Gudang WIP - A $\rightarrow$ Gudang Barang Jadi - A |
| **Keputusan QC: Reject** | WS QC & Packaging / Area Scrap | `Stock Entry` (Penanganan Cacat / Scrap) | Gudang WIP - A $\rightarrow$ Gudang Reject dan Scrap - A |
| **Pengiriman Pelanggan** | Area Logistik / Dispatch | `Sales Order`, `Delivery Note (DN)`, `Sales Invoice` | Gudang Barang Jadi - A $\rightarrow$ Pelanggan |

---

## 4. Mekanisme Jurnal Otomatis Akuntansi Persediaan Perpetual
1. **Saat Penerimaan Material**: `Persediaan Barang (Debit)` vs `Stock Diterima Tapi Belum Ditagih (Kredit)`.
2. **Saat Tagihan Vendor Masuk**: `Stock Diterima Tapi Belum Ditagih (Debit)` vs `Hutang Dagang Dalam Negeri (Kredit)`.
3. **Saat Penyelesaian Produksi (Manufacture)**: `Persediaan Barang Jadi (Debit)` vs `Persediaan Bahan Baku WIP (Kredit)` & `Penyerapan Biaya Operasi (Kredit)`.
4. **Saat Pengiriman Barang Jadi**: `Beban Pokok Penjualan / HPP (Debit)` vs `Persediaan Barang Jadi (Kredit)`.
