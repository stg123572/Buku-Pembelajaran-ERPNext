import frappe

def run():
    frappe.init(site='frontend')
    frappe.connect()
    company = "AnggiST"
    abbr = "A"

    print("=== MULAI EKSEKUSI TAHAP 1: SETUP MASTER DATA ===")

    # 1. ITEM GROUPS
    item_groups = [
        "Bahan Baku",
        "Barang Jadi",
        "Bahan Kemasan",
        "Barang Setengah Jadi",
        "Sub-Assembly"
    ]
    for ig in item_groups:
        if not frappe.db.exists("Item Group", ig):
            doc = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": ig,
                "parent_item_group": "All Item Groups",
                "is_group": 0
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Item Group dibuat: {ig}")
        else:
            print(f"[SKIP] Item Group sudah ada: {ig}")

    # 2. UOM CHECK & CREATE
    uoms = ["Nos", "Meter", "Set", "Roll"]
    for u in uoms:
        if not frappe.db.exists("UOM", u):
            doc = frappe.get_doc({
                "doctype": "UOM",
                "uom_name": u
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] UOM dibuat: {u}")
        else:
            print(f"[EXISTS] UOM: {u}")

    # 3. WAREHOUSES
    parent_wh = f"All Warehouses - {abbr}"
    warehouses = [
        {"name": f"Gudang Bahan Baku - {abbr}", "warehouse_name": "Gudang Bahan Baku"},
        {"name": f"Gudang Work In Progress - {abbr}", "warehouse_name": "Gudang Work In Progress"},
        {"name": f"Gudang Barang Jadi - {abbr}", "warehouse_name": "Gudang Barang Jadi"},
        {"name": f"Gudang Reject dan Scrap - {abbr}", "warehouse_name": "Gudang Reject dan Scrap"},
    ]
    for wh in warehouses:
        if not frappe.db.exists("Warehouse", wh["name"]):
            doc = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh["warehouse_name"],
                "parent_warehouse": parent_wh,
                "company": company,
                "is_group": 0
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Warehouse dibuat: {wh['name']}")
        else:
            print(f"[SKIP] Warehouse sudah ada: {wh['name']}")

    # 4. SUPPLIERS
    suppliers = [
        {"name": "PT Baja Mandiri Perkasa", "group": "Hardware"},
        {"name": "CV Foam & Textile Nusantara", "group": "Raw Material"},
        {"name": "PT Mitra Hardware Indonesia", "group": "Hardware"},
        {"name": "CV Karton Box Lestari", "group": "All Supplier Groups"}
    ]
    for sup in suppliers:
        # Check supplier group
        s_group = sup["group"]
        if not frappe.db.exists("Supplier Group", s_group):
            s_group = "All Supplier Groups"
        if not frappe.db.exists("Supplier", sup["name"]):
            doc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": sup["name"],
                "supplier_group": s_group,
                "supplier_type": "Company",
                "country": "Indonesia"
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Supplier dibuat: {sup['name']}")
        else:
            print(f"[SKIP] Supplier sudah ada: {sup['name']}")

    # 5. CUSTOMERS
    customers = [
        {"name": "PT Sejahtera Finansial Utama", "group": "Commercial"},
        {"name": "Toko Mebel Modern Jaya", "group": "All Customer Groups"},
        {"name": "CV Digital Solusi Mandiri", "group": "Commercial"}
    ]
    territory = "Indonesia" if frappe.db.exists("Territory", "Indonesia") else "All Territories"
    for cust in customers:
        c_group = cust["group"] if frappe.db.exists("Customer Group", cust["group"]) else "All Customer Groups"
        if not frappe.db.exists("Customer", cust["name"]):
            doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": cust["name"],
                "customer_group": c_group,
                "customer_type": "Company",
                "territory": territory
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Customer dibuat: {cust['name']}")
        else:
            print(f"[SKIP] Customer sudah ada: {cust['name']}")

    # 6. ITEMS
    items = [
        # Finished Goods
        {
            "item_code": "FG-KURSI-01",
            "item_name": "Kursi Kantor Ergonomis Nexus",
            "item_group": "Barang Jadi",
            "stock_uom": "Nos",
            "standard_rate": 1250000,
            "valuation_rate": 650000,
            "description": "Kursi kantor ergonomis dengan penopang lumbal dan armrest 3D",
            "default_warehouse": f"Gudang Barang Jadi - {abbr}"
        },
        {
            "item_code": "FG-KURSI-02",
            "item_name": "Kursi Kantor Direktur Executive",
            "item_group": "Barang Jadi",
            "stock_uom": "Nos",
            "standard_rate": 2100000,
            "valuation_rate": 1150000,
            "description": "Kursi kantor direktur dengan bantalan tebal dan finishing kulit sintetis",
            "default_warehouse": f"Gudang Barang Jadi - {abbr}"
        },
        # Raw Materials
        {
            "item_code": "RM-RANGKA-01",
            "item_name": "Rangka Punggung Besi",
            "item_group": "Bahan Baku",
            "stock_uom": "Nos",
            "standard_rate": 0,
            "valuation_rate": 150000,
            "description": "Rangka utama penopang punggung kursi",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-BUSA-01",
            "item_name": "Busa Dudukan High Density",
            "item_group": "Bahan Baku",
            "stock_uom": "Nos",
            "standard_rate": 0,
            "valuation_rate": 75000,
            "description": "Busa cetak high density anti kempes",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-KAIN-01",
            "item_name": "Kain Pelapis Mesh Hitam",
            "item_group": "Bahan Baku",
            "stock_uom": "Meter",
            "standard_rate": 0,
            "valuation_rate": 45000,
            "description": "Kain mesh berpori breathable warna hitam",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-GASLIFT-01",
            "item_name": "Silinder Hidrolik Gas Lift Class 3",
            "item_group": "Bahan Baku",
            "stock_uom": "Nos",
            "standard_rate": 0,
            "valuation_rate": 85000,
            "description": "Silinder hidrolik pengatur ketinggian standar BIFMA",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-BASE-01",
            "item_name": "Kaki Bintang Lima Nilon 320mm",
            "item_group": "Bahan Baku",
            "stock_uom": "Nos",
            "standard_rate": 0,
            "valuation_rate": 95000,
            "description": "Kaki kursi bintang 5 bahan nilon kokoh",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-RODA-01",
            "item_name": "Set Roda Caster 50mm (5 Pcs)",
            "item_group": "Bahan Baku",
            "stock_uom": "Set",
            "standard_rate": 0,
            "valuation_rate": 40000,
            "description": "Satu set berisi 5 roda swivel putar bebas",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-ARMREST-01",
            "item_name": "Set Sandaran Tangan 3D Kiri Kanan",
            "item_group": "Bahan Baku",
            "stock_uom": "Set",
            "standard_rate": 0,
            "valuation_rate": 110000,
            "description": "Sandaran tangan adjustable 3 arah",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "RM-BAUT-01",
            "item_name": "Paket Baut dan Kunci L Perakitan",
            "item_group": "Bahan Baku",
            "stock_uom": "Set",
            "standard_rate": 0,
            "valuation_rate": 20000,
            "description": "Paket lengkap baut mur dan kunci L",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        # Packaging
        {
            "item_code": "PKG-BOX-01",
            "item_name": "Kardus Kemasan Corrugated Brown",
            "item_group": "Bahan Kemasan",
            "stock_uom": "Nos",
            "standard_rate": 0,
            "valuation_rate": 25000,
            "description": "Kardus tebal kemasan packing aman",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        },
        {
            "item_code": "PKG-PLASTIK-01",
            "item_name": "Plastik Pembungkus dan Bubble Wrap",
            "item_group": "Bahan Kemasan",
            "stock_uom": "Roll",
            "standard_rate": 0,
            "valuation_rate": 10000,
            "description": "Plastik pelindung gesekan komponen",
            "default_warehouse": f"Gudang Bahan Baku - {abbr}"
        }
    ]

    for item in items:
        if not frappe.db.exists("Item", item["item_code"]):
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "item_group": item["item_group"],
                "stock_uom": item["stock_uom"],
                "is_stock_item": 1,
                "include_item_in_manufacturing": 1,
                "standard_rate": item["standard_rate"],
                "valuation_rate": item["valuation_rate"],
                "description": item["description"]
            })
            # Add item default warehouse
            doc.append("item_defaults", {
                "company": company,
                "default_warehouse": item["default_warehouse"]
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Item dibuat: {item['item_code']} - {item['item_name']}")
        else:
            print(f"[SKIP] Item sudah ada: {item['item_code']}")

    frappe.db.commit()
    print("=== SELESAI EKSEKUSI TAHAP 1: SEMUA DATA BERHASIL DIBUAT & DI-COMMIT ===")
    frappe.destroy()

if __name__ == "__main__":
    run()
