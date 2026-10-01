"""C797 activities: drop the WSQ header, K/A mapping and v5.0 references from the .md and the ReportLab PDFs."""
import re, pathlib, pypdf

MD = [(re.compile(r"^\*\*Mapping:\*\* .*\n", re.M), ""), (re.compile(r"\bv5\.0\b"), "v1.0")]
PDF = [(b"(WSQ COURSEWARE | Activity Resource)", b"(COURSEWARE | Activity Resource)"),
       (re.compile(rb"\(Mapping: [KA0-9, ]+ (Suggested time:)"), rb"(\1"),
       (b"slides v5.0)", b"slides v1.0)"), (b"Guide v5.0)", b"Guide v1.0)")]

for f in pathlib.Path("activities").rglob("*.md"):
    t = f.read_text()
    for a, b in MD:
        t = a.sub(b, t)
    f.write_text(t)

for f in pathlib.Path("activities").rglob("*.pdf"):
    w = pypdf.PdfWriter(clone_from=str(f))
    for pg in w.pages:
        co = pg.get_contents()
        d = co.get_data()
        for a, b in PDF:
            d = a.sub(b, d) if hasattr(a, "sub") else d.replace(a, b)
        co.set_data(d)
        pg.replace_contents(co)
    with open(f, "wb") as fh:
        w.write(fh)
print("done")
