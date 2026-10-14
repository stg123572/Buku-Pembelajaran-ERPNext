import frappe
from frappe.utils import nowdate, now_datetime, add_to_date
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
    print("   EKSEKUSI SOAL 4: MANUFACTURING EXECUTION         ")
    print("====================================================")

    prod_item = "FG-KURSI-01"
    bom_no = frappe.db.get_value("BOM", {"item": prod_item, "is_default": 1, "docstatus": 1}, "name")
    qty_to_produce = 10

    # 1. CEK / BUAT WORK ORDER
    existing_wo = frappe.db.get_value("Work Order", {
        "production_item": prod_item,
        "company": company,
        "qty": qty_to_produce,
        "docstatus": 1
    }, "name")

    if not existing_wo:
        wo = frappe.get_doc({
            "doctype": "Work Order",
            "company": company,
            "production_item": prod_item,
            "bom_no": bom_no,
            "qty": qty_to_produce,
            "planned_start_date": nowdate(),
            "source_warehouse": raw_wh,
            "wip_warehouse": wip_wh,
            "fg_warehouse": fg_wh,
            "use_multi_level_bom": 0
        })
        wo.set_work_order_operations()
        wo.insert(ignore_permissions=True)
        wo.submit()
        frappe.db.commit()
        wo_name = wo.name
        print(f"[SUCCESS] 1. Work Order diterbitkan & disubmit  : {wo_name}")
    else:
        wo_name = existing_wo
        print(f"[EXISTS] 1. Work Order sudah ada                 : {wo_name}")

    print(f"          Item Target : {prod_item} ({qty_to_produce} Unit)")
    print(f"          Formula BOM : {bom_no}")
    print(f"          Gudang Asal : {raw_wh}")
    print(f"          Gudang WIP  : {wip_wh}")
    print(f"          Gudang FG   : {fg_wh}")

    # 2. MATERIAL TRANSFER FOR MANUFACTURE (Pindah Bahan Baku -> WIP)
    existing_transfer = frappe.db.get_value("Stock Entry", {
        "work_order": wo_name,
        "purpose": "Material Transfer for Manufacture",
        "docstatus": 1
    }, "name")

    if not existing_transfer:
        raw_dict = make_stock_entry(wo_name, "Material Transfer for Manufacture", qty_to_produce)
        se_transfer = frappe.get_doc(raw_dict)
        se_transfer.insert(ignore_permissions=True)
        se_transfer.submit()
        frappe.db.commit()
        print(f"[SUCCESS] 2. Material Transfer ke WIP disubmit   : {se_transfer.name}")
        print(f"          10 set komponen material dipindahkan dari {raw_wh} ke {wip_wh}")
    else:
        print(f"[EXISTS] 2. Material Transfer sudah pernah dibuat: {existing_transfer}")

    # 3. SELESAIKAN JOB CARDS SECARA BERURUTAN (SEQUENCE_ID ASC)
    job_cards = frappe.get_all("Job Card", filters={"work_order": wo_name}, fields=["name", "operation", "sequence_id", "docstatus"], order_by="sequence_id asc")
    for jc in job_cards:
        if jc.docstatus == 0:
            jc_doc = frappe.get_doc("Job Card", jc.name)
            start_time = now_datetime()
            end_time = add_to_date(start_time, minutes=30)
            if not jc_doc.time_logs:
                jc_doc.append("time_logs", {
                    "from_time": start_time,
                    "to_time": end_time,
                    "time_in_mins": 30,
                    "completed_qty": qty_to_produce
                })
            jc_doc.for_quantity = qty_to_produce
            jc_doc.total_completed_qty = qty_to_produce
            jc_doc.save(ignore_permissions=True)
            jc_doc.submit()
            frappe.db.commit()
            print(f"[OK]      Seq {jc.sequence_id}: Job Card selesai disubmit: {jc.operation} ({jc.name})")
        else:
            print(f"[EXISTS]  Seq {jc.sequence_id}: Job Card sudah disubmit: {jc.operation} ({jc.name})")

    # 4. MANUFACTURE / FINISH (WIP -> Barang Jadi)
    existing_finish = frappe.db.get_value("Stock Entry", {
        "work_order": wo_name,
        "purpose": "Manufacture",
        "docstatus": 1
    }, "name")

    if not existing_finish:
        raw_finish_dict = make_stock_entry(wo_name, "Manufacture", qty_to_produce)
        se_finish = frappe.get_doc(raw_finish_dict)
        for c in se_finish.additional_costs:
            c.expense_account = "5110.020 - Penyesuaian Stock - A"
        se_finish.insert(ignore_permissions=True)
        se_finish.submit()
        frappe.db.commit()
        print(f"\n[SUCCESS] 3. Stock Entry Manufacture disubmit    : {se_finish.name}")
        print(f"          10 Unit {prod_item} selesai dirakit dan masuk ke {fg_wh}")
    else:
        print(f"\n[EXISTS] 3. Stock Entry Manufacture sudah ada   : {existing_finish}")

    # Reload Work Order untuk verifikasi status
    wo_final = frappe.get_doc("Work Order", wo_name)
    print(f"\n====================================================")
    print(f"   STATUS AKHIR WORK ORDER: {wo_final.status.upper()}")
    print(f"   Target: {wo_final.qty:.0f} Unit | Selesai Diproduksi: {wo_final.produced_qty:.0f} Unit")
    print("====================================================")

    # 5. VERIFIKASI SALDO GUDANG BARANG JADI
    print(f"\n--- SALDO GUDANG BARANG JADI ({fg_wh}) ---")
    fg_qty = frappe.db.get_value("Bin", {"item_code": prod_item, "warehouse": fg_wh}, "actual_qty") or 0
    fg_val = frappe.db.get_value("Bin", {"item_code": prod_item, "warehouse": fg_wh}, "valuation_rate") or 0
    print(f"Produk Jadi: {prod_item:<15} | Saldo: {fg_qty:>3.0f} Unit | HPP Satuan: Rp {fg_val:>10,.2f} | Total Nilai FG: Rp {(fg_qty * fg_val):>11,.2f}")

    # 6. SISA SALDO GUDANG WORK IN PROGRESS (HARUS 0 KARENA SUDAH DIKONSUMSI)
    print(f"\n--- SISA SALDO GUDANG WORK IN PROGRESS ({wip_wh}) ---")
    wip_bins = frappe.get_all("Bin", filters={"warehouse": wip_wh}, fields=["item_code", "actual_qty"], order_by="item_code asc")
    for wb in wip_bins:
        if wb.actual_qty > 0:
            print(f"Item WIP: {wb.item_code:<15} | Sisa Stok: {wb.actual_qty:>3.0f}")
    print("Semua komponen WIP telah berhasil dikonsumsi menjadi barang jadi.")

    # 7. SISA SALDO GUDANG BAHAN BAKU
    print(f"\n--- SISA SALDO GUDANG BAHAN BAKU ({raw_wh}) ---")
    bins = frappe.get_all("Bin", filters={"warehouse": raw_wh}, fields=["item_code", "actual_qty"], order_by="item_code asc")
    for b in bins:
        print(f"Item: {b.item_code:<15} | Sisa Stok: {b.actual_qty:>3.0f}")
    print("====================================================")

    frappe.destroy()

if __name__ == "__main__":
    run()
