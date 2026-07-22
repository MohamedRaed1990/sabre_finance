import os
import openpyxl
import frappe


def safe(val):
    if val is not None and str(val).strip() not in ("", "None", "nan"):
        return str(val).strip()
    return None


def safe_int(val):
    if val is None:
        return None
    try:
        return int(float(str(val).replace(',', '').strip()))
    except (ValueError, TypeError):
        return None


def get_col(row, idx):
    if row and idx < len(row):
        return row[idx]
    return None


@frappe.whitelist()
def process_todd_import(docname):
    doc = frappe.get_doc("Todd Report Import", docname)
    doc.status = "Processing"
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    try:
        file_url = getattr(doc, "todd_file", None) or getattr(doc, "import_file", None)
        if not file_url:
            frappe.throw("يرجى إرفاق ملف Todd Report أولاً.")

        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()

        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        ws = wb.active

        imported = 0
        skipped = 0
        duplicates = 0

        for row in ws.iter_rows(values_only=True):
            if not row or not any(row):
                continue

            first_col = safe(get_col(row, 0))

            if first_col and "grand total" in first_col.lower():
                break

            sc_code = safe(get_col(row, 1))
            pcc_pnr = safe(get_col(row, 2))

            if not sc_code and not pcc_pnr:
                skipped += 1
                continue

            if sc_code == "SC Code":
                skipped += 1
                continue

            qty_val = safe_int(get_col(row, 5))
            if qty_val is None:
                qty_val = 0

            source = safe(get_col(row, 4))
            service_type = first_col

            exists = frappe.db.exists("Todd Report Data", {
                "month": doc.month,
                "year": doc.year,
                "sc_code": sc_code,
                "pseudo_city_pnr": pcc_pnr,
                "source": source,
                "service_type": service_type,
            })
            if exists:
                duplicates += 1
                continue

            data_doc = frappe.get_doc({
                "doctype": "Todd Report Data",
                "todd_import": docname,
                "month": doc.month,
                "year": doc.year,
                "service_type": service_type,
                "sc_code": sc_code,
                "pseudo_city_pnr": pcc_pnr,
                "agency_country_code": safe(get_col(row, 3)),
                "source": source,
                "quantity": qty_val
            })
            data_doc.insert(ignore_permissions=True)
            imported += 1

        wb.close()

        doc.status = "Completed"
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "imported": imported,
            "skipped": skipped,
            "duplicates": duplicates,
        }

    except Exception:
        doc.status = "Failed"
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        raise
