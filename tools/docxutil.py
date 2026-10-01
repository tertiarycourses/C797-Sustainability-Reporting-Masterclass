import copy, re

OLD_TITLE, NEW_TITLE = "Sustainability Reporting and Engineering Strategies for Senior Leaders", "Sustainability Reporting Masterclass"

def set_text(par, text):
    """Rewrite a paragraph through runs[0] so its formatting survives."""
    if not par.runs:
        par.add_run(text)
        return
    # cells open with an EMPTY run; write into the first run that carries text so its formatting survives
    runs = par.runs                      # fresh proxies on every access: compare by index, never `is`
    k = next((i for i, r in enumerate(runs) if r.text), len(runs) - 1)
    for i, r in enumerate(runs):
        r.text = text if i == k else ""

def delete(par):
    par._p.getparent().remove(par._p)

def set_cell(cell, text):
    set_text(cell.paragraphs[0], text)
    for extra in cell.paragraphs[1:]:
        delete(extra)

def retitle_all(doc):
    def fix(par):
        if OLD_TITLE in par.text:
            set_text(par, par.text.replace(OLD_TITLE, NEW_TITLE))
    for par in doc.paragraphs:
        fix(par)
    for t in doc.tables:
        for c in t._cells:
            for par in c.paragraphs:
                fix(par)

def para_by_text(doc, start):
    hits = [p for p in doc.paragraphs if p.text.startswith(start)]
    assert len(hits) == 1, (start, len(hits))
    return hits[0]

def delete_range(doc, first_start, stop_start):
    """Delete paragraphs from the one starting with first_start up to (not incl.) stop_start."""
    pars = doc.paragraphs
    i = next(k for k, p in enumerate(pars) if p.text.startswith(first_start))
    j = next(k for k, p in enumerate(pars) if k > i and p.text.startswith(stop_start))
    for p in pars[i:j]:
        delete(p)
    return j - i

def rebuild_rows(table, spec):
    """spec = [(template_row_index, [cell texts])]; replaces every body row (row 0 = header kept)."""
    tpl = [copy.deepcopy(r._tr) for r in table.rows]
    tbl = table._tbl
    for r in list(table.rows)[1:]:
        tbl.remove(r._tr)
    for ti, texts in spec:
        tbl.append(copy.deepcopy(tpl[ti]))
        row = table.rows[-1]
        cells = []
        for c in row.cells:
            if not cells or cells[-1]._tc is not c._tc:
                cells.append(c)
        assert len(cells) == len(texts), (len(cells), texts)
        for c, t in zip(cells, texts):
            set_cell(c, t)

KA = re.compile(r"\s*\((?:[KA][^()]*·\s*)+(LO\d)\)")   # "(K1–K4 · A1, A2 · LO1)" -> "(LO1)"

CODES = re.compile(r"\s*\((?:[KA]\d+(?:,\s*)?)+\)")   # "(K1, K2, A3, A4)"

def strip_codes_all(doc):
    for par in doc.paragraphs:
        if CODES.search(par.text):
            set_text(par, CODES.sub("", par.text))


def all_paragraphs(doc):
    yield from doc.paragraphs
    for t in doc.tables:
        for c in t._cells:
            yield from c.paragraphs
    for s in doc.sections:
        for part in (s.footer, s.header, s.first_page_footer, s.even_page_footer):
            yield from part.paragraphs

def replace_runs(doc, subs):
    """Run-level literal replacement (body, tables, headers/footers); only changed runs are assigned,
    so footer PAGE/NUMPAGES field runs survive."""
    n = 0
    for par in all_paragraphs(doc):
        for r in par.runs:
            t = r.text
            for a, b in subs:
                t = t.replace(a, b)
            if t != r.text:
                r.text = t
                n += 1
    return n

def single_version_row(table, changes):
    for r in list(table.rows)[2:]:
        table._tbl.remove(r._tr)
    for cell, text in zip(table.rows[1].cells, ["1.0", "01 Oct 2026", changes, "Tertiary Infotech Academy"]):
        set_cell(cell, text)

def drop_column(table, idx):
    grid = table._tbl.tblGrid
    grid.remove(grid.gridCol_lst[idx])
    for r in table.rows:
        tc = r._tr.tc_lst[idx]
        r._tr.remove(tc)
