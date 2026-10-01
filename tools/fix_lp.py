"""C797 Lesson Plan: explicit rewrite of the WSQ LP (TGS-2025052343) as the non-WSQ twin."""
import re, shutil, docx
from docxutil import *

SRC = "source-wsq/courseware/LP-Sustainability-Reporting-and-Engineering-Strategies-for-Senior-Leaders-v5.0.docx"
OUT = "courseware/LP-Sustainability Reporting Masterclass (C797).docx"
shutil.copy(SRC, OUT)
d = docx.Document(OUT)

# Kept-slide map: source slides 2, 5, 7, 8, 9, 215, 216, 217 (1-based) were dropped.
DROPPED = [2, 5, 7, 8, 9, 215, 216, 217]
def m(n):
    n = int(n)
    assert n not in DROPPED, n
    return str(n - sum(1 for x in DROPPED if x < n))
def remap(text):
    return re.sub(r"\d+", lambda mo: m(mo.group(0)), text) if text.startswith("Slide") else text

replace_runs(d, [(OLD_TITLE, NEW_TITLE),
                 ("TGS Ref No: TGS-2025052343", "Course Code: C797"),
                 ("Version 5.0", "Version 1.0"),
                 ("TGS-2025052343", "C797")])

t0, t1, t2 = d.tables
single_version_row(t0, "First version of the Sustainability Reporting Masterclass lesson plan: two-day schedule "
                       "(9:30am – 5:30pm, 15 instructional hours) mapped to the v1.0 212-slide deck.")

# TOC + headings
set_text(para_by_text(d, "Delivery and Assessment Summary\t"), "Delivery Summary\t4")
set_text(para_by_text(d, "Day 1\t"), "Day 1 · 9:30am – 5:30pm\t4")
set_text(para_by_text(d, "Day 2\t"), "Day 2 · 9:30am – 5:30pm\t4")
for p in d.paragraphs:
    if p.style.name == "Heading 1" and p.text in ("Delivery and Assessment Summary", "Day 1", "Day 2"):
        set_text(p, {"Delivery and Assessment Summary": "Delivery Summary",
                     "Day 1": "Day 1 · 9:30am – 5:30pm", "Day 2": "Day 2 · 9:30am – 5:30pm"}[p.text])

set_text(para_by_text(d, "Mode: classroom facilitation."),
         "Mode: classroom facilitation. Duration: 15 instructional hours over 2 days, 7.5 hours a day from "
         "9:30am – 5:30pm with a single 30-minute lunch. Break durations are not counted as training time.")

s1 = [[c.text for c in r.cells] for r in t1.rows]
s2 = [[c.text for c in r.cells] for r in t2.rows]
CODES = re.compile(r"\s*\((?:[KA]\d+(?:,\s*)?)+\)")
def row(src, time, dur, topic=None, slides=None):
    return [time, dur, topic or CODES.sub("", src[2]), src[3], remap(src[4]) if slides is None else slides]
LUNCH = lambda t: [t, "30 min", "Lunch", "Break", "—"]

# Day 1: 485 teaching min (5/145/60/35/180/60) rescaled x450/485 onto 450 (5-min granularity);
# the 45-min lunch and 10-min break become a single 30-min lunch.
rebuild_rows(t1, [
    (1, row(s1[1], "09:30–09:35", "5 min", "Opening and course overview", "Slides 1–5")),
    (2, row(s1[2], "09:35–11:50", "2 h 15 min")),
    (3, LUNCH("11:50–12:20")),
    (4, row(s1[4], "12:20–13:15", "55 min")),
    (5, row(s1[5], "13:15–13:45", "30 min")),
    (6, row(s1[6], "13:45–16:35", "2 h 50 min")),
    (8, row(s1[8], "16:35–17:30", "55 min")),
])
# Day 2: 365 teaching min (5/145/35/100/80) once the 2-hour assessment is removed, rescaled x450/365;
# the 45-min lunch and 10-min break become a single 30-min lunch.
rebuild_rows(t2, [
    (1, row(s2[1], "09:30–09:35", "5 min", "Day 1 recap and opening", "—")),
    (2, row(s2[2], "09:35–12:30", "2 h 55 min")),
    (3, LUNCH("12:30–13:00")),
    (4, row(s2[4], "13:00–13:45", "45 min")),
    (5, row(s2[5], "13:45–15:50", "2 h 05 min")),
    (7, row(s2[7], "15:50–17:30", "1 h 40 min")),
])

fac = para_by_text(d, "Slides show models")
set_text(fac, fac.text.replace(" Never display completed learner assessment records.", ""))

d.core_properties.title = "LP-Sustainability Reporting Masterclass (C797)"
d.save(OUT)
print("saved", OUT)
