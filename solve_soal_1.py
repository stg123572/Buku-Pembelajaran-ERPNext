import frappe
from frappe.utils import nowdate

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")
    
    company = "AnggiST"
    abbr = "A"

    print("====================================================")
    print("   EKSEKUSI SOAL 1: MASTER DATA & SALDO AWAL        ")
    print("====================================================")

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
            print(f"[EXISTS] Item Group: {ig}")

    # 2. UOM
    uoms = ["Nos", "Meter", "Set", "Roll"]
    for u in uoms:
        if not frappe.db.exists("UOM", u):
            doc = frappe.get_doc({"doctype": "UOM", "uom_name": u})
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
            print(f"[EXISTS] Warehouse: {wh['name']}")

    # 4. CUSTOMER GROUPS & SUPPLIER GROUPS
    if not frappe.db.exists("Customer Group", "Retail"):
        cg = frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": "Retail",
            "parent_customer_group": "All Customer Groups",
            "is_group": 0
        })
        cg.insert(ignore_permissions=True)
        print("[OK] Customer Group dibuat: Retail")

    if not frappe.db.exists("Supplier Group", "Packaging"):
        sg = frappe.get_doc({
            "doctype": "Supplier Group",
            "supplier_group_name": "Packaging",
            "parent_supplier_group": "All Supplier Groups",
            "is_group": 0
        })
        sg.insert(ignore_permissions=True)
        print("[OK] Supplier Group dibuat: Packaging")

    # 5. SUPPLIERS
    suppliers = [
        {"name": "PT Baja Mandiri Perkasa", "group": "Hardware"},
        {"name": "CV Foam & Textile Nusantara", "group": "Raw Material"},
        {"name": "PT Mitra Hardware Indonesia", "group": "Hardware"},
        {"name": "CV Karton Box Lestari", "group": "Packaging"}
    ]
    for sup in suppliers:
        if not frappe.db.exists("Supplier", sup["name"]):
            doc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": sup["name"],
                "supplier_group": sup["group"],
                "supplier_type": "Company",
                "country": "Indonesia"
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Supplier dibuat: {sup['name']}")
        else:
            print(f"[EXISTS] Supplier: {sup['name']}")

    # 6. CUSTOMERS
    customers = [
        {"name": "PT Sejahtera Finansial Utama", "group": "Commercial"},
        {"name": "Toko Mebel Modern Jaya", "group": "Retail"},
        {"name": "CV Digital Solusi Mandiri", "group": "Commercial"}
    ]
    territory = "Indonesia" if frappe.db.exists("Territory", "Indonesia") else "All Territories"
    for cust in customers:
        if not frappe.db.exists("Customer", cust["name"]):
            doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": cust["name"],
                "customer_group": cust["group"],
                "customer_type": "Company",
                "territory": territory
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Customer dibuat: {cust['name']}")
        else:
            print(f"[EXISTS] Customer: {cust['name']}")

    # 7. ITEMS
    items = [
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
            doc.append("item_defaults", {
                "company": company,
                "default_warehouse": item["default_warehouse"]
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Item dibuat: {item['item_code']} - {item['item_name']}")
        else:
            print(f"[EXISTS] Item: {item['item_code']}")

    frappe.db.commit()

    # 8. SALDO AWAL (MATERIAL RECEIPT)
    raw_wh = f"Gudang Bahan Baku - {abbr}"
    opening_items = [
        {"item_code": "RM-RANGKA-01", "qty": 50, "rate": 150000},
        {"item_code": "RM-BUSA-01", "qty": 50, "rate": 75000},
        {"item_code": "RM-KAIN-01", "qty": 100, "rate": 45000},
        {"item_code": "RM-GASLIFT-01", "qty": 50, "rate": 85000},
        {"item_code": "RM-BASE-01", "qty": 50, "rate": 95000},
        {"item_code": "RM-RODA-01", "qty": 50, "rate": 40000},
        {"item_code": "RM-ARMREST-01", "qty": 50, "rate": 110000},
        {"item_code": "RM-BAUT-01", "qty": 50, "rate": 20000},
        {"item_code": "PKG-BOX-01", "qty": 50, "rate": 25000},
        {"item_code": "PKG-PLASTIK-01", "qty": 50, "rate": 10000},
    ]

    existing_se = frappe.db.get_value("Stock Entry", {
        "purpose": "Material Receipt",
        "company": company,
        "docstatus": 1
    }, "name")

    if not existing_se:
        expense_acc = frappe.db.get_value("Account", {
            "company": company,
            "account_type": "Stock Adjustment"
        }, "name") or "5110.020 - Penyesuaian Stock - A"

        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "purpose": "Material Receipt",
            "company": company,
            "posting_date": nowdate(),
            "to_warehouse": raw_wh,
            "items": []
        })

        for oi in opening_items:
            se.append("items", {
                "item_code": oi["item_code"],
                "qty": oi["qty"],
                "t_warehouse": raw_wh,
                "basic_rate": oi["rate"],
                "expense_account": expense_acc
            })

        se.insert(ignore_permissions=True)
        se.submit()
        frappe.db.commit()
        print(f"\n[SUCCESS] Stock Entry Material Receipt Saldo Awal berhasil dibuat & disubmit: {se.name}")
    else:
        print(f"\n[EXISTS] Stock Entry Saldo Awal sudah pernah disubmit: {existing_se}")

    # VERIFIKASI SALDO STOK
    print("\n====================================================")
    print("   STATUS SALDO STOK GUDANG BAHAN BAKU              ")
    print("====================================================")
    bins = frappe.get_all("Bin", filters={"warehouse": raw_wh}, fields=["item_code", "actual_qty", "valuation_rate", "stock_value"], order_by="item_code asc")
    total_val = 0
    for b in bins:
        total_val += b.stock_value
        print(f"Item: {b.item_code:<15} | Qty: {b.actual_qty:<5.0f} | Valuation: Rp {b.valuation_rate:>9,.0f} | Nilai: Rp {b.stock_value:>11,.0f}")
    print("----------------------------------------------------")
    print(f"TOTAL NILAI SALDO AWAL PERSEDIAAN: Rp {total_val:>11,.0f}")
    print("====================================================")

    frappe.destroy()

if __name__ == "__main__":
    run()
