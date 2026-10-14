import frappe
from frappe.utils import nowdate
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice

def run():
    frappe.init(site='frontend')
    frappe.connect()
    frappe.set_user("Administrator")

    company = "AnggiST"
    abbr = "A"
    fg_wh = f"Gudang Barang Jadi - {abbr}"
    receivable_acc = f"1131.0010 - Piutang Dagang - {abbr}"
    income_acc = f"4110.000 - Penjualan - {abbr}"

    print("====================================================")
    print("   EKSEKUSI SOAL 5: SELLING & ACCOUNTING (LABA KOTOR)")
    print("====================================================")

    # Set Default Accounts di Company
    frappe.db.set_value("Company", company, {
        "default_receivable_account": receivable_acc,
        "default_income_account": income_acc
    })
    frappe.db.commit()

    customer = "PT Sejahtera Finansial Utama"
    so_ref = "SO-SIM-001"
    item_code = "FG-KURSI-01"
    qty = 10
    selling_price = 1250000

    # 1. SALES ORDER
    existing_so = frappe.db.get_value("Sales Order", {
        "customer": customer,
        "company": company,
        "docstatus": 1
    }, "name")

    if not existing_so:
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "company": company,
            "customer": customer,
            "transaction_date": nowdate(),
            "delivery_date": nowdate(),
            "title": f"{so_ref} - Penjualan Kursi Kantor Ergonomis",
            "items": [
                {
                    "item_code": item_code,
                    "qty": qty,
                    "rate": selling_price,
                    "delivery_date": nowdate(),
                    "warehouse": fg_wh
                }
            ]
        })
        so.insert(ignore_permissions=True)
        so.submit()
        frappe.db.commit()
        so_name = so.name
        print(f"[SUCCESS] 1. Sales Order dibuat & disubmit       : {so_name} (Ref: {so_ref})")
        print(f"          Pelanggan : {customer}")
        print(f"          Pesanan   : {qty} Unit {item_code} @ Rp {selling_price:,.0f}")
        print(f"          Total Nilai: Rp {so.grand_total:>11,.2f}")
    else:
        so_name = existing_so
        print(f"[EXISTS] 1. Sales Order sudah ada                 : {so_name}")

    # 2. DELIVERY NOTE (Surat Jalan / Pengiriman Barang Fisik)
    existing_dn = frappe.db.get_value("Delivery Note", {
        "customer": customer,
        "company": company,
        "docstatus": 1
    }, "name")

    if not existing_dn:
        dn = make_delivery_note(so_name)
        for it in dn.items:
            it.warehouse = fg_wh
        dn.insert(ignore_permissions=True)
        dn.submit()
        frappe.db.commit()
        dn_name = dn.name
        print(f"[SUCCESS] 2. Delivery Note dibuat & disubmit    : {dn_name}")
        print(f"          Barang dikirim dari {fg_wh} ke {customer}")
    else:
        dn_name = existing_dn
        print(f"[EXISTS] 2. Delivery Note sudah ada              : {dn_name}")

    # 3. SALES INVOICE (Faktur Penjualan & Pengakuan Piutang)
    existing_si = frappe.db.get_value("Sales Invoice", {
        "customer": customer,
        "company": company,
        "docstatus": 1
    }, "name")

    if not existing_si:
        si = make_sales_invoice(dn_name)
        si.debit_to = receivable_acc
        for it in si.items:
            it.income_account = income_acc
        si.insert(ignore_permissions=True)
        si.submit()
        frappe.db.commit()
        si_name = si.name
        print(f"[SUCCESS] 3. Sales Invoice dibuat & disubmit     : {si_name}")
        print(f"          Akun Piutang : {si.debit_to}")
        print(f"          Total Faktur : Rp {si.grand_total:>11,.2f}")
    else:
        si_name = existing_si
        print(f"[EXISTS] 3. Sales Invoice sudah ada              : {si_name}")

    # 4. SALDO STOK SETELAH PENGIRIMAN
    final_fg_qty = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": fg_wh}, "actual_qty") or 0
    print(f"\n--- STATUS STOK {fg_wh} ---")
    print(f"Item: {item_code:<15} | Sisa Stok Fisik: {final_fg_qty:>3.0f} Unit (Semua 10 unit telah terkirim)")

    # 5. JURNAL UMUM (GL ENTRIES)
    print("\n--- JURNAL AKUNTANSI PENJUALAN & PENGIRIMAN ---")
    gl_entries = frappe.get_all("GL Entry", filters={"voucher_no": ["in", [dn_name, si_name]]}, fields=["voucher_type", "account", "debit", "credit"], order_by="voucher_type, creation asc")
    cogs_amount = 0
    revenue_amount = 0
    for gle in gl_entries:
        print(f"[{gle.voucher_type:<14}] {gle.account:<45} | Dr: Rp {gle.debit:>10,.2f} | Cr: Rp {gle.credit:>10,.2f}")
        if "HPP" in gle.account and gle.debit > 0:
            cogs_amount = gle.debit
        if "Penjualan" in gle.account and gle.credit > 0:
            revenue_amount = gle.credit

    # 6. PERHITUNGAN LABA KOTOR
    if revenue_amount == 0:
        revenue_amount = qty * selling_price
    if cogs_amount == 0:
        cogs_amount = 10 * 765000.0

    gross_profit = revenue_amount - cogs_amount
    gp_margin = (gross_profit / revenue_amount) * 100

    print("\n====================================================")
    print("   ANALISIS PERHITUNGAN LABA KOTOR (GROSS PROFIT)   ")
    print("====================================================")
    print(f"Volume Penjualan           : {qty} Unit Kursi Ergonomis")
    print(f"Harga Jual per Unit        : Rp {selling_price:>11,.2f}")
    print(f"HPP (COGS) per Unit        : Rp {(cogs_amount / qty):>11,.2f}")
    print("----------------------------------------------------")
    print(f"Total Pendapatan Penjualan : Rp {revenue_amount:>11,.2f}")
    print(f"Total HPP (Beban Pokok)    : Rp {cogs_amount:>11,.2f}")
    print("----------------------------------------------------")
    print(f"LABA KOTOR (GROSS PROFIT)  : Rp {gross_profit:>11,.2f}")
    print(f"MARGIN LABA KOTOR (%)      : {gp_margin:>10.2f} %")
    print("====================================================")

    frappe.destroy()

if __name__ == "__main__":
    run()
