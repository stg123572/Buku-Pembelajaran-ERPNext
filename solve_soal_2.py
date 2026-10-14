import frappe

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"

    print("====================================================")
    print("   EKSEKUSI SOAL 2: WORKSTATION, OPERATION & BOM    ")
    print("====================================================")

    # 1. WORKSTATIONS
    workstations = [
        {"workstation_name": "WS Potong & Jahit", "hour_rate": 45000},
        {"workstation_name": "WS Perakitan Utama", "hour_rate": 50000},
        {"workstation_name": "WS QC & Packaging", "hour_rate": 35000}
    ]

    for ws in workstations:
        if not frappe.db.exists("Workstation", ws["workstation_name"]):
            doc = frappe.get_doc({
                "doctype": "Workstation",
                "workstation_name": ws["workstation_name"],
                "hour_rate": ws["hour_rate"],
                "production_capacity": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Workstation dibuat: {ws['workstation_name']} (Tarif: Rp {ws['hour_rate']:,}/jam)")
        else:
            print(f"[EXISTS] Workstation: {ws['workstation_name']}")

    # 2. OPERATIONS
    operations = [
        {
            "name": "OP-JAHIT-BUSA",
            "workstation": "WS Potong & Jahit",
            "description": "Memotong busa dan menjahit cover kain mesh pada dudukan/sandaran"
        },
        {
            "name": "OP-ASSEMBLY-FRAME",
            "workstation": "WS Perakitan Utama",
            "description": "Merakit rangka besi, mekanisme hidrolik gaslift, armrest, dan roda"
        },
        {
            "name": "OP-QC-PACKING",
            "workstation": "WS QC & Packaging",
            "description": "Pengujian stabilitas beban dan pengemasan ke kardus box karton"
        }
    ]

    for op in operations:
        if not frappe.db.exists("Operation", op["name"]):
            doc = frappe.get_doc({
                "doctype": "Operation",
                "name": op["name"],
                "workstation": op["workstation"],
                "description": op["description"]
            })
            doc.insert(ignore_permissions=True)
            print(f"[OK] Operation dibuat: {op['name']} (WS: {op['workstation']})")
        else:
            print(f"[EXISTS] Operation: {op['name']}")

    frappe.db.commit()

    # 3. BILL OF MATERIALS (BOM) UNTUK FG-KURSI-01
    bom_item = "FG-KURSI-01"
    existing_bom = frappe.db.get_value("BOM", {"item": bom_item, "is_default": 1, "docstatus": 1}, "name")

    if not existing_bom:
        bom = frappe.get_doc({
            "doctype": "BOM",
            "item": bom_item,
            "quantity": 1,
            "company": company,
            "currency": "IDR",
            "is_active": 1,
            "is_default": 1,
            "with_operations": 1,
            "rm_cost_as_per": "Valuation Rate",
            "items": [
                {"item_code": "RM-RANGKA-01", "qty": 1, "uom": "Nos", "rate": 150000},
                {"item_code": "RM-BUSA-01", "qty": 1, "uom": "Nos", "rate": 75000},
                {"item_code": "RM-KAIN-01", "qty": 2, "uom": "Meter", "rate": 45000},
                {"item_code": "RM-GASLIFT-01", "qty": 1, "uom": "Nos", "rate": 85000},
                {"item_code": "RM-BASE-01", "qty": 1, "uom": "Nos", "rate": 95000},
                {"item_code": "RM-RODA-01", "qty": 1, "uom": "Set", "rate": 40000},
                {"item_code": "RM-ARMREST-01", "qty": 1, "uom": "Set", "rate": 110000},
                {"item_code": "RM-BAUT-01", "qty": 1, "uom": "Set", "rate": 20000},
                {"item_code": "PKG-BOX-01", "qty": 1, "uom": "Nos", "rate": 25000},
                {"item_code": "PKG-PLASTIK-01", "qty": 1, "uom": "Roll", "rate": 10000},
            ],
            "operations": [
                {
                    "operation": "OP-JAHIT-BUSA",
                    "workstation": "WS Potong & Jahit",
                    "time_in_mins": 30,
                    "hour_rate": 45000
                },
                {
                    "operation": "OP-ASSEMBLY-FRAME",
                    "workstation": "WS Perakitan Utama",
                    "time_in_mins": 20,
                    "hour_rate": 50000
                },
                {
                    "operation": "OP-QC-PACKING",
                    "workstation": "WS QC & Packaging",
                    "time_in_mins": 10,
                    "hour_rate": 35000
                }
            ]
        })

        bom.insert(ignore_permissions=True)
        bom.submit()
        frappe.db.commit()
        print(f"\n[SUCCESS] BOM berhasil dibuat & disubmit: {bom.name}")
        bom_name = bom.name
    else:
        print(f"\n[EXISTS] BOM untuk {bom_item} sudah ada: {existing_bom}")
        bom_name = existing_bom

    # Tampilkan Ringkasan Detail BOM
    doc_bom = frappe.get_doc("BOM", bom_name)
    print("\n====================================================")
    print(f"   RINCIAN FORMULA BOM: {doc_bom.name} ({doc_bom.item})")
    print("====================================================")
    print(f"Produk Jadi     : {doc_bom.item} ({doc_bom.quantity} Unit)")
    print(f"Perusahaan      : {doc_bom.company}")
    print(f"Total Biaya RM  : Rp {doc_bom.raw_material_cost:>11,.2f}")
    print(f"Biaya Operasi   : Rp {doc_bom.operating_cost:>11,.2f}")
    print(f"TOTAL HPP BOM   : Rp {doc_bom.total_cost:>11,.2f}")
    print("----------------------------------------------------")
    print("Daftar Material (Raw Materials):")
    for it in doc_bom.items:
        print(f" - {it.item_code:<15} | Qty: {it.qty:>3.0f} {it.uom:<6} | Rate: Rp {it.rate:>8,.0f} | Total: Rp {it.amount:>9,.0f}")
    print("----------------------------------------------------")
    print("Daftar Operasi (Routing & Workstation):")
    for op in doc_bom.operations:
        print(f" - {op.operation:<18} | WS: {op.workstation:<20} | Durasi: {op.time_in_mins:>2.0f} mnt | Biaya: Rp {op.operating_cost:>8,.2f}")
    print("====================================================")

    frappe.destroy()

if __name__ == "__main__":
    run()
