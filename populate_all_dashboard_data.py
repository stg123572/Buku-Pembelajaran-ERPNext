import frappe
from frappe.utils import nowdate
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"
    abbr = "A"
    raw_wh = f"Gudang Bahan Baku - {abbr}"
    wip_wh = f"Gudang Work In Progress - {abbr}"
    fg_wh = f"Gudang Barang Jadi - {abbr}"

    print("====================================================")
    print("   POPULASI DATA LENGKAP STUDI KASUS KE DASHBOARD   ")
    print("====================================================")

    # 1. PURCHASE ORDERS TAMBAHAN (BUYING DASHBOARD)
    pos = [
        {
            "ref": "PO-SIM-002",
            "supplier": "CV Foam & Textile Nusantara",
            "items": [
                {"item_code": "RM-BUSA-01", "qty": 20, "rate": 75000},
                {"item_code": "RM-KAIN-01", "qty": 40, "rate": 45000}
            ]
        },
        {
            "ref": "PO-SIM-003",
            "supplier": "PT Mitra Hardware Indonesia",
            "items": [
                {"item_code": "RM-GASLIFT-01", "qty": 20, "rate": 85000},
                {"item_code": "RM-RODA-01", "qty": 20, "rate": 40000},
                {"item_code": "RM-ARMREST-01", "qty": 20, "rate": 110000},
                {"item_code": "RM-BAUT-01", "qty": 20, "rate": 20000}
            ]
        },
        {
            "ref": "PO-SIM-004",
            "supplier": "CV Karton Box Lestari",
            "items": [
                {"item_code": "PKG-BOX-01", "qty": 20, "rate": 25000},
                {"item_code": "PKG-PLASTIK-01", "qty": 20, "rate": 10000}
            ]
        }
    ]

    for p in pos:
        if not frappe.db.exists("Purchase Order", {"title": ["like", f"%{p['ref']}%"], "company": company}):
            po = frappe.get_doc({
                "doctype": "Purchase Order",
                "company": company,
                "supplier": p["supplier"],
                "transaction_date": nowdate(),
                "schedule_date": nowdate(),
                "title": f"{p['ref']} - Pengadaan Bahan Baku",
                "items": [
                    {
                        "item_code": it["item_code"],
                        "qty": it["qty"],
                        "rate": it["rate"],
                        "schedule_date": nowdate(),
                        "warehouse": raw_wh
                    }
                    for it in p["items"]
                ]
            })
            po.insert(ignore_permissions=True)
            po.submit()
            print(f"[OK] PO dibuat: {po.name} ({p['ref']} - {p['supplier']}) Rp {po.grand_total:,.0f}")
        else:
            print(f"[EXISTS] PO: {p['ref']}")

    # 2. SALES ORDERS TAMBAHAN (SELLING DASHBOARD)
    # SO-SIM-002: Toko Mebel Modern Jaya (To Deliver & Bill)
    if not frappe.db.exists("Sales Order", {"title": ["like", "%SO-SIM-002%"], "company": company}):
        so2 = frappe.get_doc({
            "doctype": "Sales Order",
            "company": company,
            "customer": "Toko Mebel Modern Jaya",
            "transaction_date": nowdate(),
            "delivery_date": nowdate(),
            "title": "SO-SIM-002 - Pesanan Kursi Retail Toko Modern Jaya",
            "items": [
                {
                    "item_code": "FG-KURSI-01",
                    "qty": 5,
                    "rate": 1200000,
                    "delivery_date": nowdate(),
                    "warehouse": fg_wh
                }
            ]
        })
        so2.insert(ignore_permissions=True)
        so2.submit()
        print(f"[OK] SO dibuat: {so2.name} (SO-SIM-002 - Toko Mebel Modern Jaya) Rp {so2.grand_total:,.0f} [Status: To Deliver & Bill]")
    else:
        print("[EXISTS] SO: SO-SIM-002")

    # SO-SIM-003: CV Digital Solusi Mandiri (Delivered, To Bill)
    if not frappe.db.exists("Sales Order", {"title": ["like", "%SO-SIM-003%"], "company": company}):
        so3 = frappe.get_doc({
            "doctype": "Sales Order",
            "company": company,
            "customer": "CV Digital Solusi Mandiri",
            "transaction_date": nowdate(),
            "delivery_date": nowdate(),
            "title": "SO-SIM-003 - Pesanan Coworking Kursi Ergonomis",
            "items": [
                {
                    "item_code": "FG-KURSI-01",
                    "qty": 3,
                    "rate": 1250000,
                    "delivery_date": nowdate(),
                    "warehouse": fg_wh
                }
            ]
        })
        so3.insert(ignore_permissions=True)
        so3.submit()
        print(f"[OK] SO dibuat: {so3.name} (SO-SIM-003 - CV Digital Solusi Mandiri) Rp {so3.grand_total:,.0f}")
        
        # Buat Delivery Note untuk SO3 agar masuk ke Top Customers
        dn3 = make_delivery_note(so3.name)
        for it in dn3.items:
            it.warehouse = fg_wh
        dn3.insert(ignore_permissions=True)
        dn3.submit()
        print(f"[OK] Delivery Note dibuat untuk SO3: {dn3.name} (Delivered 3 Unit)")
    else:
        print("[EXISTS] SO: SO-SIM-003")

    # 3. WORK ORDER AKTIF (MANUFACTURING DASHBOARD)
    # Work order 5 unit FG-KURSI-01 yang sedang berjalan (In Process)
    bom_no = frappe.db.get_value("BOM", {"item": "FG-KURSI-01", "is_default": 1, "docstatus": 1}, "name")
    if not frappe.db.exists("Work Order", {"production_item": "FG-KURSI-01", "qty": 5, "company": company}):
        wo2 = frappe.get_doc({
            "doctype": "Work Order",
            "company": company,
            "production_item": "FG-KURSI-01",
            "bom_no": bom_no,
            "qty": 5,
            "planned_start_date": nowdate(),
            "source_warehouse": raw_wh,
            "wip_warehouse": wip_wh,
            "fg_warehouse": fg_wh,
            "use_multi_level_bom": 0
        })
        wo2.set_work_order_operations()
        wo2.insert(ignore_permissions=True)
        wo2.submit()
        print(f"[OK] Work Order Aktif dibuat: {wo2.name} (5 Unit Kursi) [Status: Not Started / In Process]")
        
        # Transfer bahan ke WIP
        raw_dict = make_stock_entry(wo2.name, "Material Transfer for Manufacture", 5)
        se2 = frappe.get_doc(raw_dict)
        se2.insert(ignore_permissions=True)
        se2.submit()
        print(f"[OK] Material Transfer ke WIP untuk WO2: {se2.name} [Status WO: In Process]")
    else:
        print("[EXISTS] Work Order 2")

    frappe.db.commit()

    # 4. PASTIKAN USER DEFAULT COMPANY UNTUK ANGGISITANGGANG & ADMINISTRATOR
    users = ["anggisitanggang056@gmail.com", "Administrator"]
    for u in users:
        frappe.defaults.set_user_default("company", company, u)
        frappe.defaults.set_user_default("Company", company, u)
        frappe.clear_cache(user=u)

    frappe.defaults.set_global_default("default_company", company)
    frappe.defaults.set_global_default("company", company)
    frappe.clear_cache()
    frappe.db.commit()

    print("\n====================================================")
    print("   STATUS ELEMEN DASHBOARD SELLING SEKARANG        ")
    print("====================================================")
    from frappe.desk.doctype.number_card.number_card import get_result
    cards = ['Annual Sales', 'Sales Orders to Deliver', 'Sales Orders to Bill', 'Active Customers']
    for c in cards:
        card_doc = frappe.get_doc("Number Card", c)
        val = get_result(card_doc.as_json(), "[]")
        print(f"Card: {c:<25} -> {val}")

    print("====================================================")
    frappe.destroy()

if __name__ == "__main__":
    run()
