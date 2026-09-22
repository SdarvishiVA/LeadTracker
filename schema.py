"""Canonical lead-log reader. Resolves fields by header NAME, not column position.
Shared by the converter and by the dashboard aggregator."""
import datetime

CANONICAL = ["Date Received","Week Of","Lead Name","Company","Prospect Type","Phone","Email",
             "Source of Lead","Referred By","Invested Before?","Date Contacted","Responded?",
             "Deal Type","Call Notes","Timeline","Qualified?","Reason Not Qualified",
             "Next Follow-up","Status"]

# every spelling seen in the wild -> canonical field
ALIASES = {
    "date received":"Date Received", "date":"Date Received", "date reçue":"Date Received",
    "week of":"Week Of", "semaine":"Week Of",
    "lead name":"Lead Name", "name":"Lead Name", "nom":"Lead Name",
    "company":"Company", "compagnie":"Company", "entreprise":"Company",
    "prospect type":"Prospect Type", "type de prospect":"Prospect Type",
    "phone":"Phone", "telephone":"Phone", "téléphone":"Phone", "tel":"Phone",
    "email":"Email", "e-mail":"Email", "courriel":"Email",
    "source of lead":"Source of Lead", "lead source":"Source of Lead", "source":"Source of Lead",
    "referred by":"Referred By", "source of referral":"Referred By", "referral":"Referred By",
    "invested before?":"Invested Before?", "invested before":"Invested Before?",
    "date contacted":"Date Contacted", "contacted":"Date Contacted",
    "responded?":"Responded?", "responded":"Responded?",
    "deal type":"Deal Type", "type":"Deal Type",
    "call notes":"Call Notes", "notes":"Call Notes", "note":"Call Notes",
    "timeline":"Timeline", "echeancier":"Timeline",
    "qualified?":"Qualified?", "qualified":"Qualified?",
    "reason not qualified":"Reason Not Qualified",
    "next follow-up":"Next Follow-up", "next follow up":"Next Follow-up", "follow-up":"Next Follow-up",
    "status":"Status", "statut":"Status",
    # carried, not part of the template
    "lead id":"Lead ID", "property owned":"Property owned", "units owned":"units owned",
}

def norm(h):
    if h is None: return None
    return " ".join(str(h).strip().lower().split())

def find_header_row(ws, scan=8):
    """Row whose cells resolve to the most known canonical fields."""
    best_row, best_hits = None, 0
    for r in range(1, min(scan, ws.max_row) + 1):
        hits = sum(1 for c in ws[r] if norm(c.value) in ALIASES)
        if hits > best_hits:
            best_row, best_hits = r, hits
    if best_hits < 3:
        raise ValueError("no header row found in first %d rows" % scan)
    return best_row

def column_map(ws, header_row):
    """canonical field -> column index. Unknown headers kept under their raw name."""
    m, extras = {}, {}
    for c in range(1, ws.max_column + 1):
        raw = ws.cell(header_row, c).value
        n = norm(raw)
        if n is None: continue
        if n in ALIASES:
            field = ALIASES[n]
            m.setdefault(field, c)
        else:
            extras[str(raw).strip()] = c
    return m, extras

def read_rows(ws):
    """Yield dicts keyed by canonical field. Formula cells return None."""
    hr = find_header_row(ws)
    m, extras = column_map(ws, hr)
    out = []
    for r in range(hr + 1, ws.max_row + 1):
        rec, has = {}, False
        for field, c in list(m.items()) + list(extras.items()):
            v = ws.cell(r, c).value
            if isinstance(v, str) and v.startswith("="):
                v = None
            if v == "": v = None
            rec[field] = v
            if v is not None and field != "Week Of": has = True
        rec["_row"] = r
        if has: out.append(rec)
    return out, hr, m, extras
