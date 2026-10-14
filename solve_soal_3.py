import frappe
from frappe.utils import nowdate
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"
    abbr = "A"
    raw_wh = f"Gudang Bahan Baku - {abbr}"
    payable_acc = f"2111.001 - Hutang Dagang Dalam Negeri - {abbr}"

    print("====================================================")
    print("   EKSEKUSI SOAL 3: PENGADAAN (PROCUREMENT FLOW)    ")
    print("====================================================")

    # Pastikan default payable account adalah Hutang Dagang Dalam Negeri
    frappe.db.set_value("Company", company, "default_payable_account", payable_acc)
    frappe.db.commit()

    # 1. PURCHASE ORDER
    supplier = "PT Baja Mandiri Perkasa"
    po_custom_ref = "PO-SIM-001"

    existing_po = frappe.db.get_value("Purchase Order", {"supplier": supplier, "company": company, "docstatus": 1}, "name")

    if not existing_po:
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "company": company,
            "supplier": supplier,
            "transaction_date": nowdate(),
            "schedule_date": nowdate(),
            "title": f"{po_custom_ref} - Pengadaan Rangka & Kaki Bintang",
            "items": [
                {
                    "item_code": "RM-RANGKA-01",
                    "qty": 20,
                    "rate": 150000,
                    "schedule_date": nowdate(),
                    "warehouse": raw_wh
                },
                {
                    "item_code": "RM-BASE-01",
                    "qty": 20,
                    "rate": 95000,
                    "schedule_date": nowdate(),
                    "warehouse": raw_wh
                }
            ]
        })
        po.insert(ignore_permissions=True)
        po.submit()
        frappe.db.commit()
        po_name = po.name
        print(f"[SUCCESS] 1. Purchase Order dibuat & disubmit : {po.name} (Ref: {po_custom_ref})")
        print(f"          Supplier   : {po.supplier}")
        print(f"          Total Nilai: Rp {po.grand_total:>11,.2f}")
    else:
        po_name = existing_po
        print(f"[EXISTS] 1. Purchase Order sudah ada            : {po_name}")

    # 2. PURCHASE RECEIPT (Penerimaan Barang Fisik ke Gudang)
    existing_pr = frappe.db.get_value("Purchase Receipt", {"supplier": supplier, "company": company, "docstatus": 1}, "name")
    if not existing_pr:
        pr = make_purchase_receipt(po_name)
        for it in pr.items:
            it.warehouse = raw_wh
        pr.insert(ignore_permissions=True)
        pr.submit()
        frappe.db.commit()
        pr_name = pr.name
        print(f"[SUCCESS] 2. Purchase Receipt disubmit (Stok Masuk): {pr.name}")
        print(f"          Gudang Target: {raw_wh}")
    else:
        pr_name = existing_pr
        print(f"[EXISTS] 2. Purchase Receipt sudah ada          : {pr_name}")

    # 3. PURCHASE INVOICE (Pencatatan Tagihan & Hutang Dagang)
    existing_pi = frappe.db.get_value("Purchase Invoice", {"supplier": supplier, "company": company, "docstatus": 1}, "name")
    if not existing_pi:
        pi = make_purchase_invoice(pr_name)
        pi.bill_no = f"INV-BMP-2026/09"
        pi.bill_date = nowdate()
        pi.credit_to = payable_acc
        pi.insert(ignore_permissions=True)
        pi.submit()
        frappe.db.commit()
        pi_name = pi.name
        print(f"[SUCCESS] 3. Purchase Invoice disubmit (Hutang)  : {pi.name}")
        print(f"          No. Tagihan Vendor: {pi.bill_no}")
        print(f"          Akun Hutang       : {pi.credit_to}")
        print(f"          Total Tagihan     : Rp {pi.grand_total:>11,.2f}")
    else:
        pi_name = existing_pi
        print(f"[EXISTS] 3. Purchase Invoice sudah ada          : {pi_name}")

    # 4. VERIFIKASI SALDO STOK SETELAH PENERIMAAN PO
    print("\n====================================================")
    print(f"   SALDO STOK ITEM PENGADAAN DI {raw_wh}")
    print("====================================================")
    items_po = ["RM-RANGKA-01", "RM-BASE-01"]
    for ic in items_po:
        actual_qty = frappe.db.get_value("Bin", {"item_code": ic, "warehouse": raw_wh}, "actual_qty") or 0
        val_rate = frappe.db.get_value("Bin", {"item_code": ic, "warehouse": raw_wh}, "valuation_rate") or 0
        print(f"Item: {ic:<15} | Saldo Akhir: {actual_qty:>3.0f} Nos (50 Saldo Awal + 20 dari PO) | Nilai Satuan: Rp {val_rate:>8,.0f}")
    print("====================================================")

    # 5. JURNAL UMUM (GL ENTRIES)
    print("\nJurnal Akuntansi yang Terbentuk Otomatis:")
    gl_entries = frappe.get_all("GL Entry", filters={"voucher_no": ["in", [pr_name, pi_name]]}, fields=["voucher_type", "account", "debit", "credit"], order_by="voucher_type, creation asc")
    for gle in gl_entries:
        print(f"[{gle.voucher_type:<16}] {gle.account:<45} | Dr: Rp {gle.debit:>10,.2f} | Cr: Rp {gle.credit:>10,.2f}")
    print("====================================================")

    frappe.destroy()

if __name__ == "__main__":
    run()
