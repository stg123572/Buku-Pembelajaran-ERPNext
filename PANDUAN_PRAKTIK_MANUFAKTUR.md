# PANDUAN PRAKTIK ERPNEXT: INDUSTRI MANUFAKTUR
**Studi Kasus:** PT Anggi Karya Manufaktur (Perakitan Kursi Kantor Ergonomis)  
**Lokasi Dataset:** Folder `ERP_Anggi`

---

## 1. Profil Skenario Bisnis
* **Nama Perusahaan**: PT Anggi Karya Manufaktur
* **Bidang Usaha**: Manufaktur & Perakitan Furnitur Kantor (*Assembly Manufacturing*)
* **Produk Utama**: Kursi Kantor Ergonomis Tipe Nexus (`FG-KURSI-01`)
* **Mata Uang**: IDR (Rupiah)

---

## 2. Struktur Data dalam Folder `ERP_Anggi`

| No | File | Deskripsi & Tujuan |
|---|---|---|
| 1 | `01_Item_Groups.csv` | Kelompok barang (Bahan Baku, Barang Jadi, Kemasan, dll.) |
| 2 | `02_Warehouses.csv` | Master Gudang (Bahan Baku, Work In Progress / WIP, Barang Jadi) |
| 3 | `03_Workstations_and_Operations.csv` | Stasiun kerja & jenis pekerjaan produksi |
| 4 | `04_Suppliers.csv` | Daftar vendor/pemasok komponen bahan baku |
| 5 | `05_Customers.csv` | Daftar pelanggan B2B dan retail pembeli produk jadi |
| 6 | `06_Items.csv` | Master data seluruh material dan produk jadi lengkap dengan harga |
| 7 | `07_Bill_of_Materials_BOM.csv` | Resep / komposisi material untuk memproduksi 1 unit kursi |
| 8 | `08_Opening_Stock.csv` | Data saldo awal bahan baku untuk langsung mulai produksi |
| 9 | `09_Purchase_Order_Simulasi.csv` | Contoh transaksi pemesanan pembelian ke supplier |
| 10 | `10_Sales_Order_Simulasi.csv` | Contoh transaksi pesanan penjualan dari customer |

---

## 3. Alur Praktik Langkah Demi Langkah (Step-by-Step)

### LANGKAH 1: Setup Master Data
Masuk ke ERPNext ([http://localhost:8080](http://localhost:8080)):

1. **Item Group**:
   * Buka modul **Stock** > **Item Group** > Buat kelompok: `Bahan Baku`, `Barang Jadi`, `Bahan Kemasan`.
2. **Warehouses (Gudang)**:
   * Buka modul **Stock** > **Warehouse** > Tambahkan:
     * `Gudang Bahan Baku - AKM` (Tipe: Stores)
     * `Gudang Work In Progress - AKM` (Tipe: Work In Progress)
     * `Gudang Barang Jadi - AKM` (Tipe: Finished Goods)
3. **Items (Daftar Barang)**:
   * Masukkan barang jadi: `FG-KURSI-01` (Beri centang *Is Stock Item*, Maintain Stock).
   * Masukkan bahan baku: `RM-RANGKA-01`, `RM-BUSA-01`, `RM-KAIN-01`, `RM-GASLIFT-01`, `RM-BASE-01`, `RM-RODA-01`, `RM-ARMREST-01`, `RM-BAUT-01`, `PKG-BOX-01`, `PKG-PLASTIK-01`.

---

### LANGKAH 2: Setup Komponen Manufaktur
1. **Workstation & Operation**:
   * Buka modul **Manufacturing** > **Workstation**:
     * `WS Potong dan Jahit` (Tarif Rp 45.000 / jam)
     * `WS Perakitan Utama` (Tarif Rp 50.000 / jam)
     * `WS QC dan Packaging` (Tarif Rp 35.000 / jam)
   * Buka **Manufacturing** > **Operation** untuk menambahkan operasi terkait.
2. **Bill of Materials (BOM)**:
   * Buka **Manufacturing** > **BOM** > Klik **Add BOM**.
   * Item: `FG-KURSI-01` (Kuantitas: 1).
   * Masukkan tabel material sesuai file `07_Bill_of_Materials_BOM.csv`.
   * Simpan dan klik **Submit**. Status BOM akan menjadi *Default* & *Active*.

---

### LANGKAH 3: Pengadaan Bahan Baku (Stocking)
Pilih salah satu cara untuk mengisi stok bahan baku:
* **Cara Cepat (Opening Stock)**:
  * Buka **Stock** > **Stock Entry** > Tipe: `Material Receipt`.
  * Target Warehouse: `Gudang Bahan Baku - AKM`.
  * Masukkan item bahan baku sesuai file `08_Opening_Stock.csv`.
  * Simpan & Submit. Sekarang gudang bahan baku sudah terisi 50 set komponen.
* **Cara Realistis (Procurement Flow)**:
  * Buka modul **Buying** > **Purchase Order** > Isi vendor dari `04_Suppliers.csv`.
  * Buat **Purchase Receipt** saat barang datang.
  * Buat **Purchase Invoice** untuk penagihan vendor.

---

### LANGKAH 4: Menjalankan Perintah Kerja (Work Order)
1. Buka **Manufacturing** > **Work Order** > Klik **Add Work Order**.
2. Pilih Item: `FG-KURSI-01`.
3. Tentukan kuantitas produksi, misalnya: **10 Unit**.
4. Sistem otomatis memuat BOM:
   * **Source Warehouse**: `Gudang Bahan Baku - AKM`
   * **WIP Warehouse**: `Gudang Work In Progress - AKM`
   * **Target Warehouse**: `Gudang Barang Jadi - AKM`
5. Klik **Save** lalu **Submit**.

---

### LANGKAH 5: Eksekusi Produksi & Transfer Bahan
1. Pada dokumen Work Order yang sudah disubmit:
   * Klik tombol **Start** / **Transfer Material for Manufacture**.
   * Sistem akan membuat dokumen **Stock Entry (Material Transfer for Manufacture)** dari Gudang Bahan Baku ke Gudang WIP.
   * Simpan dan **Submit**.
2. Selesaikan operasi (bila menggunakan fitur Job Card).
3. Setelah perakitan selesai:
   * Di halaman Work Order, klik **Finish** / **Manufacture**.
   * Sistem membuat dokumen **Stock Entry (Manufacture)**:
     * Mengurangi komponen dari Gudang WIP.
     * Menambahkan 10 unit `FG-KURSI-01` ke `Gudang Barang Jadi - AKM`.
   * Simpan dan **Submit**. Status Work Order akan berubah menjadi **Completed**.

---

### LANGKAH 6: Penjualan Produk Jadi (Sales)
1. Buka modul **Selling** > **Sales Order** > Pilih Customer `PT Sejahtera Finansial Utama`.
2. Masukkan item: `FG-KURSI-01` sebanyak 10 unit @ Rp 1.250.000.
3. Submit Sales Order.
4. Buat **Delivery Note** (Surat Jalan) untuk mengirim barang dari `Gudang Barang Jadi - AKM` ke pelanggan.
5. Buat **Sales Invoice** (Faktur Penjualan) untuk mencatat piutang dan penerimaan pembayaran.

---

### LANGKAH 7: Evaluasi Laporan & Akuntansi
Periksa laporan otomatis yang dihasilkan oleh ERPNext:
1. **Stock** > **Stock Balance** / **Stock Ledger**: Melihat mutasi keluar-masuk bahan baku dan bertambahnya barang jadi.
2. **Manufacturing** > **Production Analytics**: Melihat performa dan ketepatan waktu produksi.
3. **Accounting** > **Profit and Loss Statement (Laba Rugi)**: Melihat pendapatan penjualan, HPP (*Cost of Goods Sold*), dan laba kotor yang diperoleh.
