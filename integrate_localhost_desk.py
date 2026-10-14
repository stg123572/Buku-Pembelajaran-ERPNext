import frappe
import json

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"
    abbr = "A"

    print("================================================================")
    print("   INTEGRASI STUDI KASUS MANUFAKTUR KE LOCALHOST ERPNEXT DESK   ")
    print("================================================================")

    # 1. KUNCI PENGATURAN DEFAULT PERUSAHAAN (GLOBAL & USER DEFAULTS)
    print("\n[1/4] Mengatur Default Perusahaan ke AnggiST...")
    frappe.defaults.set_global_default("default_company", company)
    frappe.defaults.set_global_default("company", company)

    for u in ["Administrator", "anggisitanggang056@gmail.com"]:
        if frappe.db.exists("User", u):
            frappe.defaults.set_user_default("company", company, u)
            frappe.defaults.set_user_default("Company", company, u)
            frappe.defaults.set_user_default("default_company", company, u)
            print(f"  -> Default company user '{u}' diatur ke '{company}'")

    frappe.db.commit()

    # 2. BUAT CUSTOM NUMBER CARDS UNTUK INDIKATOR KUNCI 5 SOAL
    print("\n[2/4] Membuat Custom Number Cards untuk Studi Kasus...")
    number_cards_def = [
        {
            "name": "AKM - Saldo Awal Material",
            "label": "Saldo Awal Material",
            "document_type": "Stock Entry",
            "function": "Sum",
            "aggregate_function_based_on": "total_incoming_value",
            "module": "Manufacturing",
            "filters_json": json.dumps([
                ["Stock Entry", "company", "=", company],
                ["Stock Entry", "stock_entry_type", "=", "Material Receipt"],
                ["Stock Entry", "docstatus", "=", "1"]
            ])
        },
        {
            "name": "AKM - Total Pengadaan Bahan",
            "label": "Total Pengadaan Bahan (PO)",
            "document_type": "Purchase Order",
            "function": "Sum",
            "aggregate_function_based_on": "grand_total",
            "module": "Manufacturing",
            "filters_json": json.dumps([
                ["Purchase Order", "company", "=", company],
                ["Purchase Order", "docstatus", "=", "1"]
            ])
        },
        {
            "name": "AKM - Kursi Diproduksi",
            "label": "Kursi Diproduksi (Unit)",
            "document_type": "Work Order",
            "function": "Sum",
            "aggregate_function_based_on": "produced_qty",
            "module": "Manufacturing",
            "filters_json": json.dumps([
                ["Work Order", "company", "=", company],
                ["Work Order", "production_item", "=", "FG-KURSI-01"],
                ["Work Order", "docstatus", "=", "1"]
            ])
        },
        {
            "name": "AKM - Omzet Penjualan",
            "label": "Total Omzet Penjualan",
            "document_type": "Sales Invoice",
            "function": "Sum",
            "aggregate_function_based_on": "grand_total",
            "module": "Manufacturing",
            "filters_json": json.dumps([
                ["Sales Invoice", "company", "=", company],
                ["Sales Invoice", "docstatus", "=", "1"]
            ])
        }
    ]

    for nc_data in number_cards_def:
        card_name = nc_data["name"]
        if frappe.db.exists("Number Card", card_name):
            doc = frappe.get_doc("Number Card", card_name)
            doc.update(nc_data)
            doc.save(ignore_permissions=True)
            print(f"  -> Update Number Card: {card_name}")
        else:
            doc = frappe.get_doc({
                "doctype": "Number Card",
                "type": "Document Type",
                "is_public": 1,
                **nc_data
            })
            doc.insert(ignore_permissions=True)
            print(f"  -> Buat Number Card: {card_name}")

    frappe.db.commit()

    # 3. BUAT / UPDATE WORKSPACE "Studi Kasus Manufaktur" DI SIDEBAR DESK
    print("\n[3/4] Membuat Workspace Desk Khusus 'Studi Kasus Manufaktur'...")
    ws_name = "Studi Kasus Manufaktur"
    
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

    ws_shortcuts = [
        {"shortcut_name": "Item Kursi & Komponen", "label": "Item Kursi & Komponen", "type": "DocType", "link_to": "Item", "color": "Blue"},
        {"shortcut_name": "Resep BOM Kursi Ergonomis", "label": "Resep BOM Kursi Ergonomis", "type": "DocType", "link_to": "BOM", "color": "Green"},
        {"shortcut_name": "Perintah Kerja (Work Order)", "label": "Perintah Kerja (Work Order)", "type": "DocType", "link_to": "Work Order", "color": "Orange"},
        {"shortcut_name": "Pengadaan (Purchase Order)", "label": "Pengadaan (Purchase Order)", "type": "DocType", "link_to": "Purchase Order", "color": "Cyan"},
        {"shortcut_name": "Penjualan (Sales Order)", "label": "Penjualan (Sales Order)", "type": "DocType", "link_to": "Sales Order", "color": "Purple"},
        {"shortcut_name": "Laporan Laba Rugi", "label": "Laporan Laba Rugi", "type": "Report", "link_to": "Profit and Loss Statement", "color": "Green"}
    ]

    ws_links = [
        # Kartu Soal 1
        {"type": "Card Break", "label": "Soal 1: Master Persediaan & Saldo Awal"},
        {"type": "Link", "label": "Item Master (FG & Bahan)", "link_type": "DocType", "link_to": "Item"},
        {"type": "Link", "label": "Daftar Gudang (Warehouses)", "link_type": "DocType", "link_to": "Warehouse"},
        {"type": "Link", "label": "Kelompok Barang (Item Groups)", "link_type": "DocType", "link_to": "Item Group"},
        {"type": "Link", "label": "Penerimaan Saldo Awal (Material Receipt)", "link_type": "DocType", "link_to": "Stock Entry"},
        {"type": "Link", "label": "Laporan Saldo Stok (Stock Balance)", "link_type": "Report", "link_to": "Stock Balance", "is_query_report": 1},

        # Kartu Soal 2
        {"type": "Card Break", "label": "Soal 2: Workstation & Resep BOM"},
        {"type": "Link", "label": "Stasiun Kerja (Workstations)", "link_type": "DocType", "link_to": "Workstation"},
        {"type": "Link", "label": "Operasi Manufaktur (Operations)", "link_type": "DocType", "link_to": "Operation"},
        {"type": "Link", "label": "Bill of Materials (BOM-FG-KURSI-01-001)", "link_type": "DocType", "link_to": "BOM"},

        # Kartu Soal 3
        {"type": "Card Break", "label": "Soal 3: Procurement Flow"},
        {"type": "Link", "label": "Pesanan Pembelian (Purchase Orders)", "link_type": "DocType", "link_to": "Purchase Order"},
        {"type": "Link", "label": "Penerimaan Barang (Purchase Receipts)", "link_type": "DocType", "link_to": "Purchase Receipt"},
        {"type": "Link", "label": "Faktur Tagihan Vendor (Purchase Invoices)", "link_type": "DocType", "link_to": "Purchase Invoice"},
        {"type": "Link", "label": "Daftar Vendor (Suppliers)", "link_type": "DocType", "link_to": "Supplier"},

        # Kartu Soal 4
        {"type": "Card Break", "label": "Soal 4: Eksekusi Produksi & Mutasi"},
        {"type": "Link", "label": "Surat Perintah Kerja (Work Orders)", "link_type": "DocType", "link_to": "Work Order"},
        {"type": "Link", "label": "Tiket Kerja Stasiun (Job Cards)", "link_type": "DocType", "link_to": "Job Card"},
        {"type": "Link", "label": "Mutasi Material WIP & Finish", "link_type": "DocType", "link_to": "Stock Entry"},
        {"type": "Link", "label": "Buku Besar Persediaan (Stock Ledger)", "link_type": "Report", "link_to": "Stock Ledger", "is_query_report": 1},

        # Kartu Soal 5
        {"type": "Card Break", "label": "Soal 5: Penjualan & Laba Kotor"},
        {"type": "Link", "label": "Pesanan Penjualan (Sales Orders)", "link_type": "DocType", "link_to": "Sales Order"},
        {"type": "Link", "label": "Surat Jalan Kirim (Delivery Notes)", "link_type": "DocType", "link_to": "Delivery Note"},
        {"type": "Link", "label": "Faktur Penjualan (Sales Invoices)", "link_type": "DocType", "link_to": "Sales Invoice"},
        {"type": "Link", "label": "Daftar Pelanggan (Customers)", "link_type": "DocType", "link_to": "Customer"},

        # Kartu Laporan
        {"type": "Card Break", "label": "Laporan Keuangan & Audit"},
        {"type": "Link", "label": "Laba Rugi (Profit & Loss Statement)", "link_type": "Report", "link_to": "Profit and Loss Statement", "is_query_report": 1},
        {"type": "Link", "label": "Analisis Laba Kotor (Gross Profit)", "link_type": "Report", "link_to": "Gross Profit", "is_query_report": 1},
        {"type": "Link", "label": "Buku Besar Umum (General Ledger)", "link_type": "Report", "link_to": "General Ledger", "is_query_report": 1},
        {"type": "Link", "label": "Neraca Keuangan (Balance Sheet)", "link_type": "Report", "link_to": "Balance Sheet", "is_query_report": 1}
    ]

    ws_num_cards = [
        {"number_card_name": "AKM - Saldo Awal Material", "label": "Saldo Awal Material"},
        {"number_card_name": "AKM - Total Pengadaan Bahan", "label": "Total Pengadaan Bahan"},
        {"number_card_name": "AKM - Kursi Diproduksi", "label": "Kursi Diproduksi"},
        {"number_card_name": "AKM - Omzet Penjualan", "label": "Total Omzet Penjualan"}
    ]

    is_new_ws = not frappe.db.exists("Workspace", ws_name)
    if is_new_ws:
        ws = frappe.get_doc({
            "doctype": "Workspace",
            "label": ws_name,
            "title": "Studi Kasus Manufaktur - PT AKM",
            "icon": "package",
            "module": "Manufacturing",
            "is_hidden": 0,
            "public": 1,
            "sequence_id": 1.0,
            "content": json.dumps(ws_content)
        })
    else:
        ws = frappe.get_doc("Workspace", ws_name)
        ws.label = ws_name
        ws.title = "Studi Kasus Manufaktur - PT AKM"
        ws.icon = "package"
        ws.module = "Manufacturing"
        ws.is_hidden = 0
        ws.public = 1
        ws.content = json.dumps(ws_content)
    
    # Update child tables
    ws.set("number_cards", [])
    for nc in ws_num_cards:
        ws.append("number_cards", nc)
        
    ws.set("shortcuts", [])
    for sc in ws_shortcuts:
        ws.append("shortcuts", sc)
        
    ws.set("links", [])
    for lnk in ws_links:
        ws.append("links", lnk)

    if is_new_ws:
        ws.insert(ignore_permissions=True)
    else:
        ws.save(ignore_permissions=True)
    print(f"  -> Workspace '{ws_name}' berhasil disimpan dan dipublikasikan!")

    # 4. TAMBAHKAN SHORTCUTS KE WORKSPACE "Home"
    print("\n[4/4] Memperbarui Workspace 'Home' agar langsung menampilkan Studi Kasus...")
    if frappe.db.exists("Workspace", "Home"):
        home = frappe.get_doc("Workspace", "Home")
        
        home_new_shortcuts = [
            {"shortcut_name": "Studi Kasus Manufaktur", "label": "Studi Kasus PT AKM (Semua Soal)", "type": "Page", "link_to": "studi-kasus-manufaktur", "color": "Green"},
            {"shortcut_name": "Kursi Nexus (FG-KURSI-01)", "label": "Kursi Nexus (FG-KURSI-01)", "type": "DocType", "link_to": "Item", "color": "Blue"},
            {"shortcut_name": "BOM Kursi Ergonomis", "label": "BOM Kursi Ergonomis", "type": "DocType", "link_to": "BOM", "color": "Orange"},
            {"shortcut_name": "Work Order (10 Unit)", "label": "Work Order (10 Unit)", "type": "DocType", "link_to": "Work Order", "color": "Purple"}
        ]
        
        existing_sc_names = [s.label for s in home.shortcuts]
        for sc in home_new_shortcuts:
            if sc["label"] not in existing_sc_names:
                home.append("shortcuts", sc)
                print(f"  -> Menambahkan shortcut ke Home: {sc['label']}")
        
        home.save(ignore_permissions=True)
        print("  -> Workspace 'Home' berhasil diperbarui.")

    frappe.db.commit()
    frappe.clear_cache()
    print("\n[SELESAI] Seluruh integrasi ke localhost:8080 telah tuntas!")

if __name__ == "__main__":
    run()
