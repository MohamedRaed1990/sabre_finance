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


def find_col_indices(header_row, wanted):
    """
    header_row: tuple of cell values from the header row
    wanted: dict like {"sc_code": "Sc Code", "segment_name": "Name", "air": "Air", "ndc": "NDC"}
    returns: dict {"sc_code": 0, "segment_name": 1, ...} (0-based column index) or raises
    """
    normalized = {}
    for idx, cell in enumerate(header_row):
        if cell is not None:
            normalized[str(cell).strip().lower()] = idx

    result = {}
    missing = []
    for key, header_name in wanted.items():
        idx = normalized.get(header_name.strip().lower())
        if idx is None:
            missing.append(header_name)
        else:
            result[key] = idx

    if missing:
        frappe.throw(f"Could not find the following columns in the file: {', '.join(missing)}")

    return result


def is_total_row(sc_code, segment_name):
    """Detect a 'Total' summary row (e.g. the last row of the file) so it
    is never imported as data."""
    for value in (sc_code, segment_name):
        if value and value.strip().lower() in ("total", "grand total"):
            return True
    return False


@frappe.whitelist()
def process_scs_import(docname):
    doc = frappe.get_doc("Sabre Central Segments Import", docname)
    doc.status = "Processing"
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    try:
        file_url = doc.scs_file
        if not file_url:
            frappe.throw("Please attach a Sabre Central Segments file first.")

        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()

        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        ws = wb.active

        rows_iter = ws.iter_rows(values_only=True)

        # Skip any leading blank rows to find the real header row
        header_row = None
        for row in rows_iter:
            if row and any(cell is not None and str(cell).strip() != "" for cell in row):
                header_row = row
                break
        if not header_row:
            frappe.throw("File is empty or has no header row.")

        cols = find_col_indices(header_row, {
            "sc_code": "Sc Code",
            "segment_name": "Name",
            "air": "Air",
            "ndc": "NDC",
        })

        imported = 0
        skipped = 0
        duplicates = 0

        # Track sc_codes already recorded in this run so a repeated
        # sc_code only produces one record (the first occurrence).
        seen_sc_codes = set()

        for row in rows_iter:
            if not row or not any(row):
                continue

            sc_code = safe(row[cols["sc_code"]]) if cols["sc_code"] < len(row) else None
            segment_name = safe(row[cols["segment_name"]]) if cols["segment_name"] < len(row) else None
            air = safe_int(row[cols["air"]]) if cols["air"] < len(row) else None
            ndc = safe_int(row[cols["ndc"]]) if cols["ndc"] < len(row) else None

            first_cell = safe(row[0]) if row else None
            if first_cell and "grand total" in first_cell.lower():
                break

            if is_total_row(sc_code, segment_name):
                skipped += 1
                continue

            if not sc_code and not segment_name:
                skipped += 1
                continue

            if sc_code and sc_code in seen_sc_codes:
                duplicates += 1
                continue

            exists = frappe.db.exists("Sabre Central Segments Data", {
                "month": doc.month,
                "year": doc.year,
                "sc_code": sc_code,
            })
            if exists:
                duplicates += 1
                if sc_code:
                    seen_sc_codes.add(sc_code)
                continue

            data_doc = frappe.get_doc({
                "doctype": "Sabre Central Segments Data",
                "scs_import": docname,
                "month": doc.month,
                "year": doc.year,
                "sc_code": sc_code,
                "segment_name": segment_name,
                "air": air or 0,
                "ndc": ndc or 0,
            })
            data_doc.insert(ignore_permissions=True)
            imported += 1

            if sc_code:
                seen_sc_codes.add(sc_code)

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
