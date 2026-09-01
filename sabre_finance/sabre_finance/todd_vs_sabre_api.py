import frappe


@frappe.whitelist()
def build_todd_vs_sabre(month, year):
    """
    Build 'Todd VS Sabre' records for a specific month/year, one row per
    distinct sc_code found in 'Todd Report Data' for that period.
    pseudo_city_pnr is not used/stored at all.

    - agency_name: looked up by sc_code, first from MIDT Data.iata_name,
      then falls back to Sabre Central Segments Data.segment_name.
    - todd_air: sum of quantity across all Todd Report Data rows for
      this sc_code where source == "EDIFACT" (0 if none found).
    - todd_ndc: sum of quantity across all Todd Report Data rows for
      this sc_code where source == "NDC" (0 if none found).
    - air: looked up by sc_code from Sabre Central Segments Data.
    - sabre_bookings: looked up by sc_code from MIDT Data.
    - sc_ndc, midt_ndc: both looked up by sc_code from Sabre Central
      Segments Data.ndc (same value in both fields).
    - account_manager: left empty for manual entry later.

    Existing Todd VS Sabre rows for the same (sc_code, month, year)
    are skipped to avoid duplicates if this is run more than once for
    the same period.
    """

    missing = []
    if not frappe.db.exists("Todd Report Data", {"month": month, "year": year}):
        missing.append("Todd Report")
    if not frappe.db.exists("MIDT Data", {"month": month, "year": year}):
        missing.append("MIDT")
    if not frappe.db.exists("Sabre Central Segments Data", {"month": month, "year": year}):
        missing.append("Sabre Central Segments")

    if missing:
        frappe.throw(
            f"Cannot generate Todd VS Sabre for {month} {year}. "
            f"The following file(s) have not been uploaded and processed yet: "
            f"{', '.join(missing)}."
        )

    midt_rows = frappe.get_all(
        "MIDT Data",
        filters={"month": month, "year": year},
        fields=["sc_code", "iata_name", "sabre_bookings"],
    )
    midt_name_lookup = {}
    midt_bookings_lookup = {}
    for r in midt_rows:
        if not r.sc_code:
            continue
        if r.sc_code not in midt_name_lookup and r.iata_name:
            midt_name_lookup[r.sc_code] = r.iata_name
        if r.sc_code not in midt_bookings_lookup and r.sabre_bookings is not None:
            midt_bookings_lookup[r.sc_code] = r.sabre_bookings

    scs_rows = frappe.get_all(
        "Sabre Central Segments Data",
        filters={"month": month, "year": year},
        fields=["sc_code", "segment_name", "air", "ndc"],
    )
    scs_name_lookup = {}
    scs_air_lookup = {}
    scs_ndc_lookup = {}
    for r in scs_rows:
        if not r.sc_code:
            continue
        if r.sc_code not in scs_name_lookup and r.segment_name:
            scs_name_lookup[r.sc_code] = r.segment_name
        if r.sc_code not in scs_air_lookup and r.air is not None:
            scs_air_lookup[r.sc_code] = r.air
        if r.sc_code not in scs_ndc_lookup and r.ndc is not None:
            scs_ndc_lookup[r.sc_code] = r.ndc

    todd_rows = frappe.get_all(
        "Todd Report Data",
        filters={"month": month, "year": year},
        fields=["sc_code", "source", "quantity"],
    )

    if not todd_rows:
        frappe.throw(f"No Todd Report Data found for {month} {year}.")

    grouped = {}
    for row in todd_rows:
        if not row.sc_code:
            continue
        g = grouped.setdefault(row.sc_code, {"todd_air": 0, "todd_ndc": 0})
        source = (row.source or "").strip().upper()
        qty = row.quantity or 0
        if source == "EDIFACT":
            g["todd_air"] += qty
        elif source == "NDC":
            g["todd_ndc"] += qty

    created = 0
    skipped_existing = 0
    matched_midt = 0
    matched_scs = 0
    no_match = 0

    for sc_code, g in grouped.items():
        exists = frappe.db.exists("Todd VS Sabre", {
            "sc_code": sc_code,
            "month": month,
            "year": year,
        })
        if exists:
            skipped_existing += 1
            continue

        agency_name = midt_name_lookup.get(sc_code)
        if agency_name:
            matched_midt += 1
        else:
            agency_name = scs_name_lookup.get(sc_code)
            if agency_name:
                matched_scs += 1
            else:
                no_match += 1

        air = scs_air_lookup.get(sc_code)
        sabre_bookings = midt_bookings_lookup.get(sc_code)

        # sc_ndc and midt_ndc both come from the same source: the ndc
        # value on Sabre Central Segments Data for this sc_code.
        scs_ndc = scs_ndc_lookup.get(sc_code)

        doc = frappe.get_doc({
            "doctype": "Todd VS Sabre",
            "sc_code": sc_code,
            "agency_name": agency_name,
            "month": month,
            "year": year,
            "todd_air": g["todd_air"],
            "todd_ndc": g["todd_ndc"],
            "air": air,
            "sabre_bookings": sabre_bookings,
            "sc_ndc": scs_ndc,
            "midt_ndc": scs_ndc,
            "account_manager": None,
        })
        doc.insert(ignore_permissions=True)
        created += 1

        if created % 200 == 0:
            frappe.db.commit()

    frappe.db.commit()

    return {
        "status": "success",
        "month": month,
        "year": year,
        "created": created,
        "skipped_existing": skipped_existing,
        "matched_from_midt": matched_midt,
        "matched_from_scs": matched_scs,
        "no_agency_match": no_match,
    }
