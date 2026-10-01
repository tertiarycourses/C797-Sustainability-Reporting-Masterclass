"""C797 Learner Guide: explicit rewrite of the WSQ LG (TGS-2025052343) as the non-WSQ twin."""
import shutil, docx
from docxutil import *

SRC = "source-wsq/courseware/LG-Sustainability-Reporting-and-Engineering-Strategies-for-Senior-Leaders-v5.0.docx"
OUT = "courseware/LG-Sustainability Reporting Masterclass (C797).docx"
shutil.copy(SRC, OUT)
d = docx.Document(OUT)

replace_runs(d, [(OLD_TITLE, NEW_TITLE),
                 ("TGS Ref No: TGS-2025052343", "Course Code: C797"),
                 ("Version 5.0", "Version 1.0"),
                 ("TGS-2025052343", "C797")])

t0, t1 = d.tables
single_version_row(t0, "First version of the Sustainability Reporting Masterclass learner guide: course overview, "
                       "learning outcomes and four activity procedures.")

# TOC (the source lists the version record / TOC one page late)
set_text(para_by_text(d, "Document Version Control Record\t"), "Document Version Control Record\t2")
set_text(para_by_text(d, "Table of Contents\t"), "Table of Contents\t3")
delete(para_by_text(d, "Assessment preparation\t"))
set_text(para_by_text(d, "Learning Outcomes and Competency Mapping\t"), "Learning Outcomes\t5")

set_text(para_by_text(d, "This two-day WSQ programme"),
         "This two-day course helps senior leaders connect engineering decisions to defensible sustainability "
         "disclosures, regulatory compliance and market positioning. Duration is 15 instructional hours over "
         "2 days (9:30am – 5:30pm).")

# Learning outcomes: heading and the K/A mapping column
for p in d.paragraphs:
    if p.style.name == "Heading 1" and p.text == "Learning Outcomes and Competency Mapping":
        set_text(p, "Learning Outcomes")
assert t1.rows[0].cells[1].text == "K/A mapping"
drop_column(t1, 1)

# Assessment preparation section
delete_range(d, "Assessment preparation", "References")

d.core_properties.title = "LG-Sustainability Reporting Masterclass (C797)"
d.save(OUT)
print("saved", OUT)
