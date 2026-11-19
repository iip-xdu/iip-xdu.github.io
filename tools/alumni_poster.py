#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a one-page alumni destination poster (PNG) from team.html data.

Layout: 1200 x 1680 portrait poster, rendered with headless Chromium.
Usage:
    python3 tools/alumni_poster.py
Output:
    alumni-poster.html  (intermediate layout)
    alumni-poster.png   (final poster image)
"""
import collections
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

# reuse data + helpers from alumni_stats.py
spec = importlib.util.spec_from_file_location("alumni_stats", TOOLS / "alumni_stats.py")
S = importlib.util.module_from_spec(spec)
sys.modules["alumni_stats"] = S
spec.loader.exec_module(S)

OUT_HTML = ROOT / "alumni-poster.html"
OUT_PNG = ROOT / "alumni-poster.png"

W, H = 1200, 1680
ACCENT = "#FEA116"
DARK = "#0F172B"

POSTER_CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#FFFFFF;}}
body{{font-family:{S.FONT};color:{DARK};-webkit-font-smoothing:antialiased;}}
.poster{{width:{W}px;height:{H}px;display:flex;flex-direction:column;}}

/* header */
.hd{{background:{DARK};color:#fff;padding:26px 46px 22px;display:flex;align-items:center;
  justify-content:space-between;flex:none;}}
.hd-l{{display:flex;align-items:center;gap:16px;}}
.logo{{width:56px;height:56px;border-radius:50%;background:#fff;object-fit:contain;padding:4px;}}
.hd-l .org{{font-size:13px;letter-spacing:.24em;color:#FEA116;font-weight:700;}}
.hd-l .ti{{font-size:30px;font-weight:800;letter-spacing:1px;margin-top:4px;}}
.hd-r{{text-align:right;font-size:13px;color:#CBD5E1;line-height:1.9;}}
.hd-r b{{color:#fff;font-size:16px;}}

/* kpi strip */
.kpis{{display:flex;background:#FFF7EA;border-bottom:1px solid #F3E3C7;flex:none;}}
.kpi{{flex:1;padding:14px 6px;text-align:center;border-right:1px solid #F3E3C7;}}
.kpi:last-child{{border-right:none;}}
.kpi .n{{font-size:30px;font-weight:800;color:{ACCENT};line-height:1;}}
.kpi .n.small{{font-size:22px;}}
.kpi .c{{font-size:12.5px;color:#6B7280;margin-top:7px;}}

.body{{flex:1;padding:20px 46px 0;display:flex;flex-direction:column;gap:16px;}}

.sec-t{{font-size:15px;font-weight:800;letter-spacing:.5px;display:flex;align-items:center;gap:8px;}}
.sec-t:before{{content:"";width:5px;height:16px;border-radius:2px;background:{ACCENT};}}

/* donut row */
.donuts{{display:grid;grid-template-columns:1fr 1fr;gap:22px;}}
.dcard{{border:1px solid #E8EDF4;border-radius:12px;padding:14px 16px 12px;}}
.dcard h3{{font-size:14px;font-weight:700;margin-bottom:2px;}}
.dcard .s{{font-size:12px;color:#8A94A6;margin-bottom:6px;}}
.drow{{display:flex;align-items:center;gap:14px;}}
.legend{{flex:1;}}
.lg-item{{display:flex;align-items:center;gap:8px;font-size:13px;padding:4px 0;
  border-bottom:1px dashed #EEF2F7;}}
.lg-item:last-child{{border-bottom:none;}}
.lg-dot{{width:11px;height:11px;border-radius:3px;flex:none;}}
.lg-label{{flex:1;color:#334155;}}
.lg-val{{font-weight:700;}}

/* bars */
.bars{{display:flex;flex-direction:column;gap:7px;}}
.bar-row{{display:flex;align-items:center;gap:10px;}}
.bar-lab{{flex:none;width:118px;text-align:right;font-size:13px;line-height:1.25;}}
.bar-track{{flex:1;display:flex;flex-direction:column;gap:4px;}}
.bar-line{{display:flex;align-items:center;gap:6px;height:15px;background:#F1F5F9;border-radius:4px;}}
.bar-fill{{height:100%;border-radius:4px;min-width:2px;}}
.bar-num{{font-size:13px;font-weight:700;color:#0F172B;white-space:nowrap;flex:none;}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:22px;}}
.pill{{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#475569;margin-left:auto;}}
.pill i{{width:10px;height:10px;border-radius:3px;display:inline-block;}}

/* footer */
.ft{{flex:none;margin:0 46px 18px;padding:12px 18px;background:#F8FAFD;border:1px solid #E8EDF4;
  border-radius:12px;display:flex;align-items:center;gap:18px;}}
.ft .lead{{font-size:13px;line-height:1.7;color:#334155;}}
.ft .lead b{{color:{ACCENT};}}
.ft .src{{margin-left:auto;font-size:11.5px;color:#9AA5B1;text-align:right;line-height:1.7;white-space:nowrap;}}
"""


def build():
    phd_rows, mst_rows = S.parse_team_html()
    phd, mst = [], []
    for name, year, raw in phd_rows:
        cat, field, org, org_zh = S.PHD[name]
        phd.append(dict(name=name, year=year, cat=cat, field=field, org=org, org_zh=org_zh))
    for name, year, raw in mst_rows:
        cat, field, org, org_zh = S.MASTER[name]
        mst.append(dict(name=name, year=year, cat=cat, field=field, org=org, org_zh=org_zh))
    allp = phd + mst

    years = sorted({p["year"] for p in allp})
    employers = {p["org"] for p in allp}
    acad = sum(1 for p in allp if p["cat"] == "academia")
    industry = sum(1 for p in allp if p["cat"] == "industry")
    further = sum(1 for p in allp if p["cat"] == "further")

    def cat_data(rows):
        c = collections.Counter(r["cat"] for r in rows)
        return [(S.CAT_LABEL[k], c[k], S.CAT_COLOR[k]) for k in ["academia", "industry", "further"] if c.get(k)]

    # field distribution
    rows_field = []
    for key, label in S.FIELD_LABEL:
        p = sum(1 for r in phd if r["field"] == key)
        m = sum(1 for r in mst if r["field"] == key)
        if p or m:
            rows_field.append((label, [("博士", p, ACCENT), ("硕士", m, DARK)]))

    # employers -> two balanced columns
    emp = collections.Counter()
    for r in allp:
        emp[(r["org"], r["org_zh"])] += 1
    top = emp.most_common(16)
    emp_rows = [(f"{zh}" if zh != en else en, n, ACCENT) for (en, zh), n in top]
    gmax = max(v for _, v, _ in emp_rows)
    left_col = emp_rows[0::2]
    right_col = emp_rows[1::2]

    year_series = [
        ("博士", [sum(1 for r in phd if r["year"] == y) for y in years], ACCENT),
        ("硕士", [sum(1 for r in mst if r["year"] == y) for y in years], DARK),
    ]

    kpis = [
        (len(phd), "博士毕业生", False),
        (len(mst), "硕士毕业生", False),
        (len(allp), "毕业生总数", False),
        (acad, "高校 / 科研院所", False),
        (industry, "企业就业", False),
        (further, "继续深造", False),
        (len(employers), "去向单位（家）", False),
        (f"{years[0]}–{years[-1]}", "毕业年份", True),
    ]

    pct_acad_phd = round(acad / len(phd) * 100)
    top3 = "、".join(f"{zh} {n} 人" for (en, zh), n in top[:3])

    kpi_html = "".join(
        f'<div class="kpi"><div class="n{" small" if small else ""}">{n}</div><div class="c">{c}</div></div>'
        for n, c, small in kpis
    )

    legend_phd = S.legend(cat_data(phd))
    legend_mst = S.legend(cat_data(mst))

    html_doc = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>IIP Lab 毕业生去向海报</title><style>{POSTER_CSS}</style></head>
<body><div class="poster">

<div class="hd">
  <div class="hd-l">
    <img class="logo" src="img/iip_xm.png" alt="IIP">
    <div>
      <div class="org">IIP LAB · XIDIAN UNIVERSITY</div>
      <div class="ti">毕业生去向统计</div>
    </div>
  </div>
  <div class="hd-r">
    去向单位 <b>{len(employers)}</b> 家<br>
    毕业年份跨度 <b>{years[0]}–{years[-1]}</b>
  </div>
</div>

<div class="kpis">{kpi_html}</div>

<div class="body">

  <div class="donuts">
    <div class="dcard">
      <h3>博士毕业生去向类型</h3><div class="s">共 {len(phd)} 人 · 按就业性质划分</div>
      <div class="drow">{S.donut(cat_data(phd), size=200, title="博士")}{legend_phd}</div>
    </div>
    <div class="dcard">
      <h3>硕士毕业生去向类型</h3><div class="s">共 {len(mst)} 人 · 按就业性质划分</div>
      <div class="drow">{S.donut(cat_data(mst), size=200, title="硕士")}{legend_mst}</div>
    </div>
  </div>

  <div>
    <div class="sec-t">行业领域分布
      <span class="pill"><i style="background:{ACCENT}"></i>博士</span>
      <span class="pill" style="margin-left:0"><i style="background:{DARK}"></i>硕士</span>
    </div>
    <div style="margin-top:10px">{S.grouped_bars_html(rows_field)}</div>
  </div>

  <div>
    <div class="sec-t">主要去向单位 TOP 16</div>
    <div class="two-col" style="margin-top:10px">
      {S.bars_html(left_col, max_val=gmax)}
      {S.bars_html(right_col, max_val=gmax)}
    </div>
  </div>

  <div>
    <div class="sec-t">各年份毕业人数</div>
    <div style="margin-top:8px">{S.stacked_columns([str(y) for y in years], year_series, width=1108, height=200)}</div>
  </div>

</div>

<div class="ft">
  <div class="lead">
    <b>{len(allp)} 名毕业生</b>中，<b>{industry} 人</b>进入企业就业，<b>{acad} 人</b>任职高校或科研院所，
    <b>{further} 人</b>赴境内外高校继续深造；博士毕业生有 <b>{pct_acad_phd}%</b> 进入学术界。
    人数最多的三家去向单位为 <b>{top3}</b>。
  </div>
  <div class="src">数据来源：team.html · Alumni<br>由 tools/alumni_poster.py 自动生成</div>
</div>

</div></body></html>"""
    print("gmax", gmax, "top3", top3)
    OUT_HTML.write_text(html_doc, encoding="utf-8")
    print("html:", OUT_HTML)


def shoot():
    edge = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    cmd = [
        edge, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        "--force-device-scale-factor=2", f"--window-size={W},{H}",
        f"--screenshot={OUT_PNG}", f"file://{OUT_HTML}",
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    print("png:", OUT_PNG, OUT_PNG.stat().st_size if OUT_PNG.exists() else "MISSING")


if __name__ == "__main__":
    build()
    shoot()
