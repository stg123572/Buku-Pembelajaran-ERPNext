# PANDUAN PELAKSANAAN PRAKTIK ERPNEXT
## PENYELESAIAN 5 SOAL STUDI KASUS MANUFAKTUR

**Panduan Klik-demi-Klik (GUI Desk) Modul Stock, Manufacturing, Buying, Selling, & Accounting**  
**Perusahaan:** PT Anggi Karya Manufaktur (`AnggiST`)  
**File Dokumen Word:** [PANDUAN_PELAKSANAAN_PRAKTIK_ERPNEXT.docx](file:///c:/Users/User/OneDrive/Documents/ERP/ERP_Anggi/PANDUAN_PELAKSANAAN_PRAKTIK_ERPNEXT.docx)

---

### Petunjuk Awal: Persiapan Lingkungan ERPNext
- **URL Akses Sistem:** Buka browser Google Chrome / Microsoft Edge di alamat `http://localhost:8080`
- **Akun Login:** Username: `Administrator` | Password: `admin` (atau akun pengguna: `anggisitanggang056@gmail.com`)
- **Perusahaan Aktif:** Pastikan perusahaan yang aktif dipilih adalah **AnggiST** (Singkatan Gudang: `- A`).

---

## MODUL 1 (SOAL 1): Konfigurasi Master Data & Saldo Awal
> **Tujuan:** Membangun fondasi master data berupa klasifikasi kelompok barang (*Item Group*), hierarki gudang (*Warehouse*), mitra bisnis (*Supplier & Customer*), master item lengkap beserta harga standar, dan pengisian saldo awal 50 unit bahan baku melalui dokumen persediaan.

### Langkah 1.1: Membuat Kelompok Barang (Item Group)
1. **Navigasi:** Ketik di Awesomebar (search bar atas) `Item Group List` atau klik menu **Stock > Item Group**.
2. **Aksi:** Klik tombol **`+ Add Item Group`** di pojok kanan atas.
3. **Pengisian Form:**
   - **Item Group Name:** `Bahan Baku`
   - **Parent Item Group:** `All Item Groups`
   - **Group Node:** Biarkan tidak tercentang.
   - Klik **Save**.
4. **Ulangi:** Tambahkan kelompok lainnya dengan cara yang sama:
   - `Barang Jadi`
   - `Bahan Kemasan`
   - `Barang Setengah Jadi`
   - `Sub-Assembly`

### Langkah 1.2: Membuat Master Gudang (Warehouse)
1. **Navigasi:** Buka menu **Stock > Warehouse** (atau ketik `Warehouse List`).
2. **Aksi:** Klik tombol **`+ Add Warehouse`**.
3. **Pengisian Form:** Buat 4 gudang berikut secara bertahap:
   - **Gudang 1:** Warehouse Name: `Gudang Bahan Baku` | Company: `AnggiST` | Parent: `All Warehouses - A` *(Tersimpan: `Gudang Bahan Baku - A`)*
   - **Gudang 2:** Warehouse Name: `Gudang Work In Progress` | Company: `AnggiST` | Parent: `All Warehouses - A` *(Tersimpan: `Gudang Work In Progress - A`)*
   - **Gudang 3:** Warehouse Name: `Gudang Barang Jadi` | Company: `AnggiST` | Parent: `All Warehouses - A` *(Tersimpan: `Gudang Barang Jadi - A`)*
   - **Gudang 4:** Warehouse Name: `Gudang Reject dan Scrap` | Company: `AnggiST` | Parent: `All Warehouses - A` *(Tersimpan: `Gudang Reject dan Scrap - A`)*

### Langkah 1.3: Membuat Pemasok (Supplier) & Pelanggan (Customer)
- **Supplier:** Menu **Buying > Supplier > `+ Add Supplier`**.
  - Masukkan nama: `PT Baja Mandiri Perkasa`, Group: `Hardware`.
  - Tambahkan supplier lain: `CV Foam & Textile Nusantara`, `PT Mitra Hardware Indonesia`, `CV Karton Box Lestari`.
- **Customer:** Menu **Selling > Customer > `+ Add Customer`**.
  - Masukkan nama: `PT Sejahtera Finansial Utama`, Customer Group: `Commercial`, Territory: `Indonesia`.
  - Tambahkan customer lain: `Toko Mebel Modern Jaya`, `CV Digital Solusi Mandiri`.

### Langkah 1.4: Membuat Master Items (Produk Jadi & Bahan Baku)
1. **Navigasi:** Masuk ke **Stock > Item > `+ Add Item`**.
2. **Input Produk Jadi (FG):**
   - **Item Code:** `FG-KURSI-01`
   - **Item Name:** `Kursi Kantor Ergonomis Nexus`
   - **Item Group:** `Barang Jadi`
   - **Default UOM:** `Nos`
   - **Standard Selling Rate:** `1.250.000`
   - **Valuation Rate:** `650.000`
   - **Default Warehouse:** `Gudang Barang Jadi - A`
   - Klik **Save**.
3. **Input 10 Komponen Bahan Baku & Kemasan:**

| Kode Item | Nama Item | Kelompok | Satuan | Harga Standar (Rp) | Gudang Default |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RM-RANGKA-01` | Rangka Punggung Besi | Bahan Baku | Nos | 150.000 | Gudang Bahan Baku - A |
| `RM-BUSA-01` | Busa Dudukan High Density | Bahan Baku | Nos | 75.000 | Gudang Bahan Baku - A |
| `RM-KAIN-01` | Kain Pelapis Mesh Hitam | Bahan Baku | Meter | 45.000 | Gudang Bahan Baku - A |
| `RM-GASLIFT-01` | Silinder Hidrolik Gas Lift Class 3 | Bahan Baku | Nos | 85.000 | Gudang Bahan Baku - A |
| `RM-BASE-01` | Kaki Bintang Lima Nilon 320mm | Bahan Baku | Nos | 95.000 | Gudang Bahan Baku - A |
| `RM-RODA-01` | Set Roda Caster 50mm (5 Pcs) | Bahan Baku | Set | 40.000 | Gudang Bahan Baku - A |
| `RM-ARMREST-01` | Set Sandaran Tangan 3D | Bahan Baku | Set | 110.000 | Gudang Bahan Baku - A |
| `RM-BAUT-01` | Paket Baut & Kunci L | Bahan Baku | Set | 20.000 | Gudang Bahan Baku - A |
| `PKG-BOX-01` | Kardus Kemasan Corrugated Brown | Bahan Kemasan | Nos | 25.000 | Gudang Bahan Baku - A |
| `PKG-PLASTIK-01` | Plastik Pembungkus & Bubble Wrap | Bahan Kemasan | Roll | 10.000 | Gudang Bahan Baku - A |

### Langkah 1.5: Input Saldo Awal Persediaan (Material Receipt)
1. **Navigasi:** Buka **Stock > Stock Entry > `+ Add Stock Entry`**.
2. **Header Dokumen:** Pilih **Stock Entry Type:** `Material Receipt` *(Purpose otomatis terisi Material Receipt)*.
3. **Target Warehouse:** Pilih **Default Target Warehouse:** `Gudang Bahan Baku - A`.
4. **Tabel Items:** Tambahkan 10 baris material di atas dengan kuantitas masing-masing **50 unit** *(khusus `RM-KAIN-01` isi **100 Meter**)* dan Basic Rate sesuai harga standar masing-masing.
5. **Akun Penyeimbang:** Pastikan Difference Account / Expense Account terisi `5110.020 - Penyesuaian Stock - A`.
6. **Simpan & Submit:** Klik tombol **Save**, kemudian klik tombol hijau **Submit** di kanan atas.
> **VERIFIKASI SOAL 1:** Total nilai persediaan awal yang masuk ke Gudang Bahan Baku adalah **Rp 35.000.000,00**. Cek melalui laporan **Stock > Stock Balance**.

---

## MODUL 2 (SOAL 2): Setup Workstation, Operation & BOM
> **Tujuan:** Menyiapkan stasiun kerja di pabrik, mendefinisikan waktu siklus dan tarif operasi perakitan, serta menyusun formula resep Bill of Materials (BOM) 1 unit kursi ergonomis.

### Langkah 2.1: Menyiapkan Workstations (Stasiun Kerja)
1. **Navigasi:** Buka **Manufacturing > Workstation > `+ Add Workstation`**.
2. **Stasiun 1:** Masukkan **Workstation Name:** `WS Potong & Jahit` | **Hour Rate:** `45.000` -> Klik **Save**.
3. **Stasiun 2:** Masukkan **Workstation Name:** `WS Perakitan Utama` | **Hour Rate:** `50.000` -> Klik **Save**.
4. **Stasiun 3:** Masukkan **Workstation Name:** `WS QC & Packaging` | **Hour Rate:** `35.000` -> Klik **Save**.

### Langkah 2.2: Menyiapkan Operations (Operasi Produksi)
1. **Navigasi:** Buka **Manufacturing > Operation > `+ Add Operation`**.
2. **Operasi 1:** Operation Name: `OP-JAHIT-BUSA` | Default Workstation: `WS Potong & Jahit` -> Klik **Save**.
3. **Operasi 2:** Operation Name: `OP-ASSEMBLY-FRAME` | Default Workstation: `WS Perakitan Utama` -> Klik **Save**.
4. **Operasi 3:** Operation Name: `OP-QC-PACKING` | Default Workstation: `WS QC & Packaging` -> Klik **Save**.

### Langkah 2.3: Membuat Formula Bill of Materials (BOM)
1. **Navigasi:** Buka **Manufacturing > Bill of Materials > `+ Add BOM`**.
2. **Header Dokumen:**
   - **Item:** `FG-KURSI-01`
   - **Quantity:** `1`
   - **Currency:** `IDR`
   - Diberi centang: **`With Operations`**
3. **Tabel Operations (Routing Produksi):** Tambahkan 3 baris tahapan:
   - Baris 1: Operasi: `OP-JAHIT-BUSA` | Workstation: `WS Potong & Jahit` | Time: `30 mins`
   - Baris 2: Operasi: `OP-ASSEMBLY-FRAME` | Workstation: `WS Perakitan Utama` | Time: `20 mins`
   - Baris 3: Operasi: `OP-QC-PACKING` | Workstation: `WS QC & Packaging` | Time: `10 mins`
4. **Tabel Materials (Daftar Komponen):** Masukkan 10 item komponen per unit (1 Rangka, 1 Busa, 2 Kain, 1 Gaslift, 1 Kaki Bintang, 1 Set Roda, 1 Set Armrest, 1 Set Baut, 1 Box Kardus, 1 Rol Plastik).
5. **Simpan & Submit:** Klik **Save**, lalu klik **Submit**.
> **VERIFIKASI SOAL 2:** Dokumen BOM tersimpan sebagai `BOM-FG-KURSI-01-001`. Total Biaya Bahan = **Rp 700.000**, Biaya Operasi = **Rp 45.000**. Total Biaya Pokok Produksi Standar = **Rp 745.000,00 / unit**.

---

## MODUL 3 (SOAL 3): Siklus Pengadaan / Procurement Flow
> **Tujuan:** Mempraktikkan pengadaan bahan baku ke vendor eksternal dengan alur: *Purchase Order* -> *Purchase Receipt* -> *Purchase Invoice*.

### Langkah 3.1: Menerbitkan Purchase Order (PO-SIM-001)
1. **Navigasi:** Buka **Buying > Purchase Order > `+ Add Purchase Order`**.
2. **Header Dokumen:** Pilih **Supplier:** `PT Baja Mandiri Perkasa`, Required By Date: hari ini.
3. **Tabel Items:** Masukkan 2 baris item yang dibeli:
   - `RM-RANGKA-01` | Qty: `20` | Rate: `150.000` | Target Warehouse: `Gudang Bahan Baku - A`
   - `RM-BASE-01` | Qty: `20` | Rate: `95.000` | Target Warehouse: `Gudang Bahan Baku - A`
4. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Dokumen tersimpan sebagai `PUR-ORD-2026-00011` dengan total transaksi **Rp 4.900.000,00**.

### Langkah 3.2: Penerimaan Barang Fisik (Purchase Receipt)
1. **Aksi Cepat:** Di dokumen Purchase Order yang baru disubmit, klik tombol **`Create ▾`** di kanan atas > pilih **`Receipt`**.
2. **Verifikasi Form:** Sistem menyalin item dan jumlah barang otomatis dari PO. Pastikan Accepted Warehouse mengarah ke `Gudang Bahan Baku - A`.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Stok fisik bertambah secara riil di Gudang Bahan Baku (+20 unit rangka & +20 unit kaki nilon).

### Langkah 3.3: Pencatatan Tagihan Pemasok (Purchase Invoice)
1. **Aksi Cepat:** Di dalam dokumen Purchase Receipt yang sudah disubmit, klik tombol **`Create ▾`** > pilih **`Invoice`**.
2. **Pengisian Tagihan:** Isi Bill No: `INV-BMP-2026/09`. Pastikan akun hutang terarah ke `2111.001 - Hutang Dagang Dalam Negeri - A`.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**.
> **VERIFIKASI SOAL 3:** Pada buku besar (**Accounting > General Ledger**), terlihat jurnal otomatis: Debit Persediaan Barang Rp 4.900.000 dan Kredit Hutang Dagang Rp 4.900.000.

---

## MODUL 4 (SOAL 4): Eksekusi Manufaktur & Mutasi Gudang
> **Tujuan:** Menjalankan perintah kerja perakitan 10 unit kursi ergonomis, transfer bahan dari Gudang Bahan Baku ke Gudang WIP, penyelesaian tiket kerja (Job Cards), dan penyelesaian produk jadi ke Gudang Barang Jadi.

### Langkah 4.1: Menerbitkan Work Order (Surat Perintah Kerja)
1. **Navigasi:** Buka **Manufacturing > Work Order > `+ Add Work Order`**.
2. **Form Header:**
   - **Item to Manufacture:** `FG-KURSI-01`
   - **Qty to Manufacture:** `10`
   - **BOM No:** Otomatis mendeteksi `BOM-FG-KURSI-01-001`
3. **Pengaturan Gudang:**
   - **Source Warehouse:** `Gudang Bahan Baku - A`
   - **WIP Warehouse:** `Gudang Work In Progress - A`
   - **FG Warehouse:** `Gudang Barang Jadi - A`
4. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Dokumen tersimpan dengan nomor `MFG-WO-2026-00001` (Status: *Not Started*).

### Langkah 4.2: Transfer Bahan Baku ke Lantai Produksi (WIP Transfer)
1. **Aksi Cepat:** Pada halaman Work Order yang sudah disubmit, klik tombol **`Start`** (atau klik **`Create ▾` > `Transfer`**).
2. **Verifikasi Form:** Sistem membuka jendela Stock Entry tipe **Material Transfer for Manufacture**. Periksa 10 komponen bahan baku dialokasikan untuk 10 unit produk dari Gudang Bahan Baku ke Gudang WIP.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Status Work Order otomatis berubah menjadi **In Process**.

### Langkah 4.3: Menyelesaikan Pengerjaan Job Cards Stasiun Kerja
1. **Navigasi:** Buka **Manufacturing > Job Card**. Anda akan melihat 3 tiket Job Card yang terhubung dengan Work Order.
2. **Selesaikan Berurutan:**
   - **Urutan 1 (`OP-JAHIT-BUSA`):** Buka dokumen > Masukkan Time Log (30 menit, Qty Completed: 10) > Klik **Save** lalu klik **Submit**.
   - **Urutan 2 (`OP-ASSEMBLY-FRAME`):** Buka dokumen > Masukkan Time Log (20 menit, Qty Completed: 10) > Klik **Save** lalu klik **Submit**.
   - **Urutan 3 (`OP-QC-PACKING`):** Buka dokumen > Masukkan Time Log (10 menit, Qty Completed: 10) > Klik **Save** lalu klik **Submit**.

### Langkah 4.4: Menyelesaikan Produksi (Manufacture Finish)
1. **Aksi Cepat:** Kembali ke dokumen Work Order, klik tombol **`Finish`** (atau **`Create ▾` > `Manufacture`**).
2. **Verifikasi Form:** Sistem memuat Stock Entry tipe **Manufacture**. Semua bahan baku di Gudang WIP dikonsumsi dan 10 unit `FG-KURSI-01` dimasukkan ke `Gudang Barang Jadi - A`.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Status Work Order kini resmi menjadi **COMPLETED**.
> **VERIFIKASI SOAL 4:** Di Gudang Barang Jadi kini tersedia 10 unit Kursi Ergonomis dengan HPP Realisasi **Rp 765.000 / unit** (Total: **Rp 7.650.000,00**). Saldo komponen di Gudang WIP telah nol.

---

## MODUL 5 (SOAL 5): Penjualan & Analisis Laba Kotor
> **Tujuan:** Memproses order penjualan 10 unit kursi ke pelanggan, mengirimkan barang fisik (Surat Jalan / Delivery Note), menerbitkan faktur tagihan (Sales Invoice), dan menganalisis perolehan laba kotor.

### Langkah 5.1: Menerbitkan Sales Order (SO-SIM-001)
1. **Navigasi:** Buka menu **Selling > Sales Order > `+ Add Sales Order`**.
2. **Pengisian Form:**
   - **Customer:** `PT Sejahtera Finansial Utama`
   - **Delivery Date:** Hari ini
3. **Tabel Items:**
   - **Item Code:** `FG-KURSI-01` | **Qty:** `10` | **Rate:** `1.250.000` | **Delivery Warehouse:** `Gudang Barang Jadi - A`
   - Total Order: **Rp 12.500.000,00**
4. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Dokumen tersimpan sebagai `SAL-ORD-2026-00006`.

### Langkah 5.2: Pengiriman Barang Fisik (Delivery Note)
1. **Aksi Cepat:** Pada dokumen Sales Order tadi, klik tombol **`Create ▾`** di kanan atas > pilih **`Delivery`**.
2. **Verifikasi Form:** Pastikan Gudang asal adalah `Gudang Barang Jadi - A` dan jumlah pengiriman adalah 10 unit.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**. Stok fisik kursi di Gudang Barang Jadi berkurang 10 unit menjadi 0.

### Langkah 5.3: Penerbitan Faktur Penjualan (Sales Invoice)
1. **Aksi Cepat:** Pada dokumen Delivery Note yang sudah disubmit, klik tombol **`Create ▾`** > pilih **`Invoice`**.
2. **Verifikasi Akun:** Pastikan akun Piutang terisi `1131.0010 - Piutang Dagang - A` dan Akun Pendapatan `4110.000 - Penjualan - A` dengan total tagihan Rp 12.500.000,00.
3. **Simpan & Submit:** Klik **Save** lalu klik **Submit**.

### Langkah 5.4: Mengevaluasi Laporan Laba Kotor (Gross Profit)
1. **Navigasi:** Buka menu **Accounting > Profit and Loss Statement** (atau **Selling > Gross Profit**).
2. **Hasil Evaluasi Keuangan:**
   - **Pendapatan Penjualan (*Revenue*):** Rp 12.500.000,00 *(10 unit @ Rp 1.250.000)*
   - **Beban Pokok Penjualan (*COGS / HPP*):** Rp 7.650.000,00 *(10 unit @ Rp 765.000)*
   - **LABA KOTOR (*GROSS PROFIT*):** **Rp 4.850.000,00**
   - **MARGIN LABA KOTOR:** **38,80%**
> **VERIFIKASI SOAL 5:** Margin laba kotor sebesar 38,80% membuktikan efisiensi proses perakitan kursi kantor ergonomis pada PT Anggi Karya Manufaktur berjalan sesuai target profitabilitas.
