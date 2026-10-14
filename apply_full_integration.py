import frappe
import json

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"
    abbr = "A"

    print("================================================================")
    print("   INTEGRASI LENGKAP 5 SOAL STUDI KASUS KE LOCALHOST ERPNEXT    ")
    print("================================================================")

    # 1. ATUR PERUSAHAAN DEFAULT (GLOBAL & USER DEFAULTS)
    print("\n[1/5] Mengatur Default Company ke 'AnggiST'...")
    frappe.defaults.set_global_default("default_company", company)
    frappe.defaults.set_global_default("company", company)

    for user_id in ["Administrator", "anggisitanggang056@gmail.com"]:
        if frappe.db.exists("User", user_id):
            frappe.defaults.set_user_default("company", company, user_id)
            frappe.defaults.set_user_default("Company", company, user_id)
            frappe.defaults.set_user_default("default_company", company, user_id)
            print(f"  -> Default company untuk user '{user_id}' sukses diatur ke '{company}'")

    frappe.db.commit()

    # 2. BUAT CUSTOM NUMBER CARDS
    print("\n[2/5] Menyiapkan Number Cards untuk 5 Soal...")
    cards_config = [
        {
            "label": "AKM - Saldo Awal Material",
            "document_type": "Stock Entry",
            "function": "Sum",
            "aggregate_function_based_on": "total_incoming_value",
            "filters_json": json.dumps([
                ["Stock Entry", "company", "=", company],
                ["Stock Entry", "stock_entry_type", "=", "Material Receipt"],
                ["Stock Entry", "docstatus", "=", "1"]
            ])
        },
        {
            "label": "AKM - Total Pengadaan Bahan",
            "document_type": "Purchase Order",
            "function": "Sum",
            "aggregate_function_based_on": "grand_total",
            "filters_json": json.dumps([
                ["Purchase Order", "company", "=", company],
                ["Purchase Order", "docstatus", "=", "1"]
            ])
        },
        {
            "label": "AKM - Kursi Diproduksi",
            "document_type": "Work Order",
            "function": "Sum",
            "aggregate_function_based_on": "produced_qty",
            "filters_json": json.dumps([
                ["Work Order", "company", "=", company],
                ["Work Order", "production_item", "=", "FG-KURSI-01"],
                ["Work Order", "docstatus", "=", "1"]
            ])
        },
        {
            "label": "AKM - Omzet Penjualan",
            "document_type": "Sales Invoice",
            "function": "Sum",
            "aggregate_function_based_on": "grand_total",
            "filters_json": json.dumps([
                ["Sales Invoice", "company", "=", company],
                ["Sales Invoice", "docstatus", "=", "1"]
            ])
        }
    ]

    card_names = []
    for c in cards_config:
        card_label = c["label"]
        if frappe.db.exists("Number Card", card_label):
            frappe.delete_doc("Number Card", card_label, ignore_permissions=True)
            print(f"  -> Menghapus versi lama: {card_label}")
        
        nc = frappe.get_doc({
            "doctype": "Number Card",
            "name": card_label,
            "label": card_label,
            "document_type": c["document_type"],
            "function": c["function"],
            "aggregate_function_based_on": c["aggregate_function_based_on"],
            "filters_json": c["filters_json"],
            "module": "Manufacturing",
            "type": "Document Type",
            "is_public": 1
        })
        nc.insert(ignore_permissions=True)
        card_names.append(nc.name)
        print(f"  -> [OK] Number Card dibuat: {nc.name}")

    frappe.db.commit()

    # 3. BUAT WORKSPACE KHUSUS "Studi Kasus Manufaktur"
    print("\n[3/5] Menyiapkan Workspace 'Studi Kasus Manufaktur'...")
    ws_name = "Studi Kasus Manufaktur"
    
    if frappe.db.exists("Workspace", ws_name):
        frappe.delete_doc("Workspace", ws_name, ignore_permissions=True)
        print(f"  -> Menghapus workspace lama '{ws_name}'")

    ws_content = [
        {
            "id": "hdr_kpi",
            "type": "header",
            "data": {"text": "<span class=\"h4\"><b>Ringkasan KPI Eksekusi Manufaktur & Penjualan (PT Anggi Karya Manufaktur)</b></span>", "col": 12}
        },
        {
            "id": "card_saldo",
            "type": "number_card",
            "data": {"number_card_name": "AKM - Saldo Awal Material", "col": 3}
        },
        {
            "id": "card_po",
            "type": "number_card",
            "data": {"number_card_name": "AKM - Total Pengadaan Bahan", "col": 3}
        },
        {
            "id": "card_wo",
            "type": "number_card",
            "data": {"number_card_name": "AKM - Kursi Diproduksi", "col": 3}
        },
        {
            "id": "card_omzet",
            "type": "number_card",
            "data": {"number_card_name": "AKM - Omzet Penjualan", "col": 3}
        },
        {
            "id": "spc_1",
            "type": "spacer",
            "data": {"col": 12}
        },
        {
            "id": "hdr_shortcuts",
            "type": "header",
            "data": {"text": "<span class=\"h4\"><b>Navigasi Cepat Dokumen 5 Soal Studi Kasus</b></span>", "col": 12}
        },
        {
            "id": "sc_item",
            "type": "shortcut",
            "data": {"shortcut_name": "Item Kursi & Komponen", "col": 4}
        },
        {
            "id": "sc_bom",
            "type": "shortcut",
            "data": {"shortcut_name": "Resep BOM Kursi Ergonomis", "col": 4}
        },
        {
            "id": "sc_wo",
            "type": "shortcut",
            "data": {"shortcut_name": "Perintah Kerja (Work Order)", "col": 4}
        },
        {
            "id": "sc_po",
            "type": "shortcut",
            "data": {"shortcut_name": "Pengadaan (Purchase Order)", "col": 4}
        },
        {
            "id": "sc_so",
            "type": "shortcut",
            "data": {"shortcut_name": "Penjualan (Sales Order)", "col": 4}
        },
        {
            "id": "sc_pnl",
            "type": "shortcut",
            "data": {"shortcut_name": "Laporan Laba Rugi", "col": 4}
        },
        {
            "id": "spc_2",
            "type": "spacer",
            "data": {"col": 12}
        },
        {
            "id": "hdr_cards",
            "type": "header",
            "data": {"text": "<span class=\"h4\"><b>Daftar Modul & Laporan Terkait</b></span>", "col": 12}
        },
        {
            "id": "crd_soal1",
            "type": "card",
            "data": {"card_name": "Soal 1: Master Persediaan & Saldo Awal", "col": 4}
        },
        {
            "id": "crd_soal2",
            "type": "card",
            "data": {"card_name": "Soal 2: Workstation & Resep BOM", "col": 4}
        },
        {
            "id": "crd_soal3",
            "type": "card",
            "data": {"card_name": "Soal 3: Procurement Flow", "col": 4}
        },
        {
            "id": "crd_soal4",
            "type": "card",
            "data": {"card_name": "Soal 4: Eksekusi Produksi & Mutasi", "col": 4}
        },
        {
            "id": "crd_soal5",
            "type": "card",
            "data": {"card_name": "Soal 5: Penjualan & Laba Kotor", "col": 4}
        },
        {
            "id": "crd_lap",
            "type": "card",
            "data": {"card_name": "Laporan Keuangan & Audit", "col": 4}
        }
    ]

    ws = frappe.get_doc({
        "doctype": "Workspace",
        "name": ws_name,
        "label": ws_name,
        "title": "Studi Kasus Manufaktur - PT AKM",
        "icon": "package",
        "module": "Manufacturing",
        "is_hidden": 0,
        "public": 1,
        "sequence_id": 1.0,
        "content": json.dumps(ws_content),
        "number_cards": [
            {"number_card_name": "AKM - Saldo Awal Material", "label": "AKM - Saldo Awal Material"},
            {"number_card_name": "AKM - Total Pengadaan Bahan", "label": "AKM - Total Pengadaan Bahan"},
            {"number_card_name": "AKM - Kursi Diproduksi", "label": "AKM - Kursi Diproduksi"},
            {"number_card_name": "AKM - Omzet Penjualan", "label": "AKM - Omzet Penjualan"}
        ],
        "shortcuts": [
            {"label": "Item Kursi & Komponen", "type": "DocType", "link_to": "Item", "color": "Blue"},
            {"label": "Resep BOM Kursi Ergonomis", "type": "DocType", "link_to": "BOM", "color": "Green"},
            {"label": "Perintah Kerja (Work Order)", "type": "DocType", "link_to": "Work Order", "color": "Orange"},
            {"label": "Pengadaan (Purchase Order)", "type": "DocType", "link_to": "Purchase Order", "color": "Cyan"},
            {"label": "Penjualan (Sales Order)", "type": "DocType", "link_to": "Sales Order", "color": "Purple"},
            {"label": "Laporan Laba Rugi", "type": "Report", "link_to": "Profit and Loss Statement", "color": "Green"}
        ],
        "links": [
            # Soal 1
            {"type": "Card Break", "label": "Soal 1: Master Persediaan & Saldo Awal"},
            {"type": "Link", "label": "Item Master (FG & Bahan)", "link_type": "DocType", "link_to": "Item"},
            {"type": "Link", "label": "Daftar Gudang (Warehouses)", "link_type": "DocType", "link_to": "Warehouse"},
            {"type": "Link", "label": "Kelompok Barang (Item Groups)", "link_type": "DocType", "link_to": "Item Group"},
            {"type": "Link", "label": "Penerimaan Saldo Awal (Material Receipt)", "link_type": "DocType", "link_to": "Stock Entry"},
            {"type": "Link", "label": "Laporan Saldo Stok (Stock Balance)", "link_type": "Report", "link_to": "Stock Balance", "is_query_report": 1},

            # Soal 2
            {"type": "Card Break", "label": "Soal 2: Workstation & Resep BOM"},
            {"type": "Link", "label": "Stasiun Kerja (Workstations)", "link_type": "DocType", "link_to": "Workstation"},
            {"type": "Link", "label": "Operasi Manufaktur (Operations)", "link_type": "DocType", "link_to": "Operation"},
            {"type": "Link", "label": "Bill of Materials (BOM-FG-KURSI-01-001)", "link_type": "DocType", "link_to": "BOM"},

            # Soal 3
            {"type": "Card Break", "label": "Soal 3: Procurement Flow"},
            {"type": "Link", "label": "Pesanan Pembelian (Purchase Orders)", "link_type": "DocType", "link_to": "Purchase Order"},
            {"type": "Link", "label": "Penerimaan Barang (Purchase Receipts)", "link_type": "DocType", "link_to": "Purchase Receipt"},
            {"type": "Link", "label": "Faktur Tagihan Vendor (Purchase Invoices)", "link_type": "DocType", "link_to": "Purchase Invoice"},
            {"type": "Link", "label": "Daftar Vendor (Suppliers)", "link_type": "DocType", "link_to": "Supplier"},

            # Soal 4
            {"type": "Card Break", "label": "Soal 4: Eksekusi Produksi & Mutasi"},
            {"type": "Link", "label": "Surat Perintah Kerja (Work Orders)", "link_type": "DocType", "link_to": "Work Order"},
            {"type": "Link", "label": "Tiket Kerja Stasiun (Job Cards)", "link_type": "DocType", "link_to": "Job Card"},
            {"type": "Link", "label": "Mutasi Material WIP & Finish", "link_type": "DocType", "link_to": "Stock Entry"},
            {"type": "Link", "label": "Buku Besar Persediaan (Stock Ledger)", "link_type": "Report", "link_to": "Stock Ledger", "is_query_report": 1},

            # Soal 5
            {"type": "Card Break", "label": "Soal 5: Penjualan & Laba Kotor"},
            {"type": "Link", "label": "Pesanan Penjualan (Sales Orders)", "link_type": "DocType", "link_to": "Sales Order"},
            {"type": "Link", "label": "Surat Jalan Kirim (Delivery Notes)", "link_type": "DocType", "link_to": "Delivery Note"},
            {"type": "Link", "label": "Faktur Penjualan (Sales Invoices)", "link_type": "DocType", "link_to": "Sales Invoice"},
            {"type": "Link", "label": "Daftar Pelanggan (Customers)", "link_type": "DocType", "link_to": "Customer"},

            # Laporan
            {"type": "Card Break", "label": "Laporan Keuangan & Audit"},
            {"type": "Link", "label": "Laba Rugi (Profit & Loss Statement)", "link_type": "Report", "link_to": "Profit and Loss Statement", "is_query_report": 1},
            {"type": "Link", "label": "Analisis Laba Kotor (Gross Profit)", "link_type": "Report", "link_to": "Gross Profit", "is_query_report": 1},
            {"type": "Link", "label": "Buku Besar Umum (General Ledger)", "link_type": "Report", "link_to": "General Ledger", "is_query_report": 1},
            {"type": "Link", "label": "Neraca Keuangan (Balance Sheet)", "link_type": "Report", "link_to": "Balance Sheet", "is_query_report": 1}
        ]
    })

    ws.insert(ignore_permissions=True)
    print(f"  -> [OK] Workspace '{ws_name}' berhasil dibuat!")
    frappe.db.commit()

    # 4. TAMBAHKAN SHORTCUT KE WORKSPACE "Home"
    print("\n[4/5] Memperbarui Workspace 'Home'...")
    if frappe.db.exists("Workspace", "Home"):
        home = frappe.get_doc("Workspace", "Home")
        
        home_shortcuts_to_add = [
            {"label": "Studi Kasus PT AKM", "type": "URL", "url": "/app/studi-kasus-manufaktur", "color": "Green"},
            {"label": "Kursi Nexus (FG-KURSI-01)", "type": "DocType", "link_to": "Item", "color": "Blue"},
            {"label": "BOM Kursi Ergonomis", "type": "DocType", "link_to": "BOM", "color": "Orange"},
            {"label": "Work Order (10 Unit)", "type": "DocType", "link_to": "Work Order", "color": "Purple"}
        ]
        
        existing_labels = [s.label for s in home.shortcuts]
        for sc in home_shortcuts_to_add:
            if sc["label"] not in existing_labels:
                home.append("shortcuts", sc)
                print(f"  -> Shortcut ditambahkan ke Home: {sc['label']}")
        
        home.save(ignore_permissions=True)
        print("  -> [OK] Workspace 'Home' berhasil diperbarui!")

    frappe.db.commit()

    # 5. BERSIHKAN CACHE SISTEM
    print("\n[5/5] Membersihkan cache sistem ERPNext...")
    frappe.clear_cache()
    for u in ["Administrator", "anggisitanggang056@gmail.com"]:
        frappe.clear_cache(user=u)

    print("\n================================================================")
    print("   INTEGRASI SELESAI DENGAN SUKSES!                            ")
    print("   Buka http://localhost:8080 untuk melihat hasilnya langsung!  ")
    print("================================================================")

if __name__ == "__main__":
    run()
