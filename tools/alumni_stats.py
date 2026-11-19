#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse alumni data from team.html and generate a self-contained
visualization report (pure SVG, no external dependencies).

Usage:
    python3 tools/alumni_stats.py
Output:
    alumni-stats.html
"""
import re
import html
import collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM_HTML = ROOT / "team.html"
OUT_HTML = ROOT / "alumni-stats.html"

# ---------------------------------------------------------------- categories
CAT_LABEL = {
    "academia": "高校 / 科研院所",
    "industry": "企业就业",
    "further": "继续深造",
}
CAT_COLOR = {
    "academia": "#FEA116",
    "industry": "#0F172B",
    "further": "#4C8BF5",
}

FIELD_LABEL = [
    ("academia", "高校与科研机构"),
    ("internet", "互联网 / 科技"),
    ("telecom", "通信与智能硬件"),
    ("chip", "芯片与自动驾驶"),
    ("defense", "国防科技研究所"),
    ("finmed", "金融与医疗"),
    ("further", "继续深造"),
    ("school", "基础教育"),
]
FIELD_COLOR = {
    "academia": "#FEA116",
    "internet": "#0F172B",
    "telecom": "#3B7DD8",
    "chip": "#7C5CFF",
    "defense": "#2E9E8F",
    "finmed": "#E06666",
    "further": "#4C8BF5",
    "school": "#9AA5B1",
}

# name -> (category, field, employer_key, employer_zh)
PHD = {
    "Shengchuan Zhang": ("academia", "academia", "Xiamen Univ.", "厦门大学"),
    "Mingjin Zhang": ("academia", "academia", "XDU", "西安电子科技大学"),
    "Chunlei Peng": ("academia", "academia", "XDU", "西安电子科技大学"),
    "Adeel Akram": ("academia", "academia", "Xuzhou Inst. of Tech.", "徐州工程学院"),
    "Mingrui Zhu": ("academia", "academia", "XDU (ISN)", "西安电子科技大学"),
    "Bing Cao": ("academia", "academia", "Tianjin Univ.", "天津大学"),
    "Zhuoqi Ma": ("academia", "academia", "XDU", "西安电子科技大学"),
    "Yi Hao": ("industry", "telecom", "Huawei", "华为"),
    "Jingwei Xin": ("academia", "academia", "XDU (ISN)", "西安电子科技大学"),
    "Decheng Liu": ("academia", "academia", "XDU", "西安电子科技大学"),
    "Hangyu Li": ("academia", "academia", "HKBU (Postdoc); XDU", "香港浸会大学（博后）"),
    "Xinrui Jiang": ("academia", "academia", "HKUST (Postdoc); Tianjin Univ.", "香港科技大学（博后）/ 天津大学"),
    "Guozhang Li": ("academia", "academia", "Beijing Normal Univ. (Postdoc)", "北京师范大学（博后）"),
    "Dawei Zhou": ("academia", "academia", "City Univ. of Macau", "澳门城市大学"),
    "Liangchen Liu": ("academia", "academia", "Hefei Univ. of Tech.", "合肥工业大学"),
    "Kun Cheng": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Ruiyang Xia": ("academia", "academia", "CQUPT", "重庆邮电大学"),
    "Xiao He": ("industry", "internet", "Kuaishou", "快手"),
}

MASTER = {
    "Jiewei Zhang": ("industry", "internet", "Baidu", "百度"),
    "Yaxin Gao": ("industry", "defense", "CETC Inst. 54", "中国电科 54 所"),
    "Wenjun Ren": ("industry", "internet", "360", "360 集团"),
    "Xinye Yu": ("industry", "defense", "CETC Inst. of Intelligence", "中国电科智能院"),
    "Yuhang Zhang": ("industry", "telecom", "Huawei", "华为"),
    "Leiyu Sun": ("industry", "telecom", "Hikvision", "海康威视"),
    "Wenjin Zha": ("industry", "defense", "CETC Inst. 38", "中国电科 38 所"),
    "Yueying Yang": ("industry", "telecom", "Huawei", "华为"),
    "Xinpeng Ding": ("further", "further", "HKUST (PhD)", "香港科技大学（读博）"),
    "Chaori Gong": ("industry", "defense", "CETC Inst. 54", "中国电科 54 所"),
    "Hongbin Qu": ("industry", "telecom", "Huawei", "华为"),
    "Yingqi Jiang": ("industry", "telecom", "ZTE", "中兴通讯"),
    "Dawei Cao": ("industry", "telecom", "Hikvision", "海康威视"),
    "Jingyu Zhou": ("industry", "internet", "Longhu Digital Tech.", "龙湖数科"),
    "Keyu Li": ("industry", "chip", "Horizon Robotics", "地平线"),
    "Kun Cheng": ("further", "further", "XDU (PhD)", "西安电子科技大学（读博）"),
    "Changcheng Liang": ("industry", "chip", "Hengxuan Tech.", "恒玄科技"),
    "Zikai Wei": ("industry", "chip", "Hengxuan Tech.", "恒玄科技"),
    "Jingfei Tang": ("industry", "school", "Huzhou No.2 High School", "湖州二中"),
    "Yun Yi": ("industry", "internet", "Baidu", "百度"),
    "Zicheng Wu": ("industry", "finmed", "ABC (Fujian)", "农业银行福建分行"),
    "Yixiong Ning": ("industry", "chip", "Zhaoxin Semiconductor", "兆芯半导体"),
    "Zhiling Guo": ("industry", "finmed", "Mindray Medical", "迈瑞医疗"),
    "Yukun Chen": ("industry", "internet", "Baidu", "百度"),
    "Xiaolong Wang": ("industry", "internet", "iFlytek", "科大讯飞"),
    "Zhigang Su": ("industry", "telecom", "Hikvision", "海康威视"),
    "Liting Sun": ("industry", "internet", "ByteDance", "字节跳动"),
    "Haichun Tai": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Yifan Jiang": ("industry", "internet", "Meituan", "美团"),
    "Ruoyu Zhao": ("industry", "internet", "NetEase Games", "网易游戏"),
    "Yuxin Zhao": ("industry", "finmed", "Ant Group", "蚂蚁集团"),
    "Chaohua Shi": ("industry", "telecom", "Vivo", "vivo"),
    "Dongxin Chen": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Si Shi": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Shiyin Dong": ("industry", "internet", "JD.com", "京东"),
    "Yusong Hu": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Yihan Xu": ("industry", "telecom", "Vivo", "vivo"),
    "Zikun Chen": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Zhipeng Xu": ("further", "further", "HKUST (PhD)", "香港科技大学（读博）"),
    "Jianhang Chen": ("industry", "chip", "Pony.ai", "小马智行"),
    "Lingfeng He": ("further", "further", "HKUST (PhD)", "香港科技大学（读博）"),
    "Yibo Xu": ("industry", "internet", "iFlytek", "科大讯飞"),
    "Zhixin Wu": ("industry", "internet", "Baidu", "百度"),
    "Keyi Chen": ("industry", "telecom", "Huawei", "华为"),
    "Yingjie Han": ("industry", "internet", "Tencent", "腾讯"),
    "Jiaqi Shi": ("industry", "telecom", "Huawei", "华为"),
    "Derui Zhang": ("industry", "internet", "ByteDance", "字节跳动"),
    "Xiru Chen": ("industry", "internet", "Alibaba", "阿里巴巴"),
    "Lei Wei": ("further", "further", "XDU (PhD)", "西安电子科技大学（读博）"),
}

NAME_ZH = {
    "Shengchuan Zhang": "张胜川", "Mingjin Zhang": "张铭津", "Chunlei Peng": "彭春蕾",
    "Adeel Akram": "Adeel Akram", "Mingrui Zhu": "朱明瑞", "Bing Cao": "曹兵",
    "Zhuoqi Ma": "马卓奇", "Yi Hao": "郝怡", "Jingwei Xin": "辛经纬",
    "Decheng Liu": "刘德成", "Hangyu Li": "李航宇", "Xinrui Jiang": "姜新蕊",
    "Guozhang Li": "李国璋", "Dawei Zhou": "周大伟", "Liangchen Liu": "刘良辰",
    "Kun Cheng": "程坤", "Ruiyang Xia": "夏瑞阳", "Xiao He": "何潇",
    "Jiewei Zhang": "张杰伟", "Yaxin Gao": "高雅欣", "Wenjun Ren": "任文俊",
    "Xinye Yu": "于欣业", "Yuhang Zhang": "张宇航", "Leiyu Sun": "孙磊宇",
    "Wenjin Zha": "查文锦", "Yueying Yang": "杨月莹", "Xinpeng Ding": "丁鑫棚",
    "Chaori Gong": "龚超日", "Hongbin Qu": "曲宏斌", "Yingqi Jiang": "姜颖奇",
    "Dawei Cao": "曹大伟", "Jingyu Zhou": "周靖宇", "Keyu Li": "李科宇",
    "Changcheng Liang": "梁昌城", "Zikai Wei": "魏子凯", "Jingfei Tang": "唐静菲",
    "Yun Yi": "羿云", "Zicheng Wu": "吴子成", "Yixiong Ning": "宁一雄",
    "Zhiling Guo": "郭志玲", "Yukun Chen": "陈宇坤", "Xiaolong Wang": "王晓龙",
    "Zhigang Su": "苏志刚", "Liting Sun": "孙丽婷", "Haichun Tai": "邰海春",
    "Yifan Jiang": "姜一凡", "Ruoyu Zhao": "赵若羽", "Yuxin Zhao": "赵宇欣",
    "Chaohua Shi": "史超华", "Dongxin Chen": "陈栋鑫", "Si Shi": "施思",
    "Shiyin Dong": "董诗音", "Yusong Hu": "胡宇松", "Yihan Xu": "徐一涵",
    "Zikun Chen": "陈子坤", "Zhipeng Xu": "徐志鹏", "Jianhang Chen": "陈建行",
    "Lingfeng He": "贺凌峰", "Yibo Xu": "徐一博", "Zhixin Wu": "吴知鑫",
    "Keyi Chen": "陈科屹", "Yingjie Han": "韩英杰", "Jiaqi Shi": "史佳琦",
    "Derui Zhang": "张德蕊", "Xiru Chen": "陈曦如", "Lei Wei": "魏蕾",
}

FONT = "PingFang SC, Hiragino Sans GB, Microsoft YaHei, Noto Sans CJK SC, sans-serif"


# ------------------------------------------------------------------- parsing
def parse_team_html():
    """Return (phd_records, master_records) as list of (name, year, raw_text)."""
    text = TEAM_HTML.read_text(encoding="utf-8")
    start = text.index("Alumni &middot; PH.D.") if "Alumni &middot; PH.D." in text else text.index("Alumni · PH.D.")
    mid = text.index("Alumni &middot; Postgraduates")
    end = text.index("<!-- Alumni end-->")

    def grab(seg):
        out = []
        for m in re.finditer(
            r"<h5[^>]*>(.*?)</h5>\s*<small>(.*?)</small>", seg, re.S
        ):
            name = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            small = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
            year = int(small.split(",")[0])
            out.append((name, year, small))
        return out

    return grab(text[start:mid]), grab(text[mid:end])


# -------------------------------------------------------------- svg builders
def esc(s):
    return html.escape(str(s), quote=True)


def donut(data, size=260, hole=0.58, title=""):
    """data: list of (label, value, color)"""
    total = sum(v for _, v, _ in data) or 1
    cx = cy = size / 2
    r = size / 2 - 6
    ri = r * hole
    parts, a0 = [], -90.0
    for label, value, color in data:
        frac = value / total
        a1 = a0 + frac * 360.0
        large = 1 if (a1 - a0) > 180 else 0
        p0 = polar(cx, cy, r, a0)
        p1 = polar(cx, cy, r, a1)
        q0 = polar(cx, cy, ri, a1)
        q1 = polar(cx, cy, ri, a0)
        d = (
            f"M {p0[0]:.2f} {p0[1]:.2f} A {r} {r} 0 {large} 1 {p1[0]:.2f} {p1[1]:.2f} "
            f"L {q0[0]:.2f} {q0[1]:.2f} A {ri} {ri} 0 {large} 0 {q1[0]:.2f} {q1[1]:.2f} Z"
        )
        mid = (a0 + a1) / 2
        lp = polar(cx, cy, (r + ri) / 2, mid)
        pct = frac * 100
        if pct >= 5:
            parts.append(
                f'<text x="{lp[0]:.1f}" y="{lp[1]:.1f}" font-size="13" font-weight="700" '
                f'fill="#FFFFFF" text-anchor="middle" dominant-baseline="central" '
                f'font-family="{FONT}">{pct:.0f}%</text>'
            )
        parts.append(f'<path d="{d}" fill="{color}" stroke="#FFFFFF" stroke-width="1.5"/>')
        a0 = a1
    center = (
        f'<text x="{cx}" y="{cy - 6}" font-size="26" font-weight="700" fill="#0F172B" '
        f'text-anchor="middle" font-family="{FONT}">{total}</text>'
        f'<text x="{cx}" y="{cy + 14}" font-size="12" fill="#6B7280" text-anchor="middle" '
        f'font-family="{FONT}">{esc(title)}</text>'
    )
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">' + "".join(parts) + center + "</svg>"


def polar(cx, cy, r, deg):
    import math

    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def legend(data, unit="人"):
    items = []
    for label, value, color in data:
        items.append(
            f'<div class="lg-item"><span class="lg-dot" style="background:{color}"></span>'
            f'<span class="lg-label">{esc(label)}</span>'
            f'<span class="lg-val">{value} {unit}</span></div>'
        )
    return '<div class="legend">' + "".join(items) + "</div>"


def bars_html(data, unit="人", max_val=None):
    """Single-series horizontal bar chart built with CSS (font size stays fixed)."""
    if not data:
        return ""
    max_val = max_val or max(v for _, v, _ in data) or 1
    out = []
    for label, value, color in data:
        pct = value / max_val * 100
        out.append(
            f'<div class="bar-row"><div class="bar-lab">{esc(label)}</div>'
            f'<div class="bar-line" style="height:20px"><div class="bar-fill" style="width:{pct:.1f}%;'
            f'background:{color}"></div><span class="bar-num">{value} {unit}</span></div></div>'
        )
    return '<div class="bars">' + "".join(out) + "</div>"


def grouped_bars_html(rows):
    """Grouped horizontal bar chart built with CSS (font size stays fixed)."""
    max_val = max(max(v for _, v, _ in vals) for _, vals in rows) or 1
    out = []
    for label, vals in rows:
        segs = []
        for sname, value, color in vals:
            pct = value / max_val * 100
            segs.append(
                f'<div class="bar-line"><div class="bar-fill" style="width:{pct:.1f}%;background:{color}">'
                f'</div><span class="bar-num">{value}</span></div>'
            )
        out.append(
            f'<div class="bar-row"><div class="bar-lab">{esc(label)}</div>'
            f'<div class="bar-track">{"".join(segs)}</div></div>'
        )
    return '<div class="bars">' + "".join(out) + "</div>"


def stacked_columns(years, series, width=1000, height=260):
    """years: list of year labels; series: list of (name, [values], color)"""
    pad_l, pad_b, pad_t = 44, 34, 16
    plot_w = width - pad_l - 12
    plot_h = height - pad_b - pad_t
    n = len(years)
    slot = plot_w / n
    bar_w = min(slot * 0.6, 34)
    totals = [sum(s[1][i] for s in series) for i in range(n)]
    max_v = max(totals) or 1
    out = [
        f'<line x1="{pad_l}" y1="{height - pad_b}" x2="{width - 6}" y2="{height - pad_b}" '
        f'stroke="#CBD5E1" stroke-width="1"/>'
    ]
    # y grid
    for k in range(5):
        gv = max_v * k / 4
        gy = height - pad_b - plot_h * k / 4
        out.append(
            f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{width - 6}" y2="{gy:.1f}" stroke="#EEF2F7" stroke-width="1"/>'
        )
        out.append(
            f'<text x="{pad_l - 8}" y="{gy:.1f}" font-size="12" fill="#94A3B8" text-anchor="end" '
            f'dominant-baseline="central" font-family="{FONT}">{gv:.0f}</text>'
        )
    for i, year in enumerate(years):
        cx = pad_l + slot * i + slot / 2
        acc_h = 0.0
        for sname, values, color in series:
            v = values[i]
            if not v:
                continue
            h = plot_h * v / max_v
            y = height - pad_b - acc_h - h
            out.append(
                f'<rect x="{cx - bar_w / 2:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
                f'fill="{color}" rx="2"/>'
            )
            if h >= 14:
                out.append(
                    f'<text x="{cx:.1f}" y="{y + h / 2:.1f}" font-size="12" font-weight="700" '
                    f'fill="#FFFFFF" text-anchor="middle" dominant-baseline="central" '
                    f'font-family="{FONT}">{v}</text>'
                )
            acc_h += h
        if totals[i]:
            out.append(
                f'<text x="{cx:.1f}" y="{height - pad_b - acc_h - 6:.1f}" font-size="12" '
                f'font-weight="700" fill="#0F172B" text-anchor="middle" font-family="{FONT}">{totals[i]}</text>'
            )
        out.append(
            f'<text x="{cx:.1f}" y="{height - pad_b + 16}" font-size="12" fill="#64748B" '
            f'text-anchor="middle" font-family="{FONT}">{esc(year)}</text>'
        )
    return f'<svg viewBox="0 0 {width} {height}" width="100%" role="img">' + "".join(out) + "</svg>"


# ------------------------------------------------------------------- report
CSS = """
:root{--primary:#FEA116;--dark:#0F172B;--light:#F1F8FF;--muted:#6B7280;}
*{box-sizing:border-box;}
body{margin:0;background:#F7F9FC;color:#0F172B;
 font-family:PingFang SC,Hiragino Sans GB,Microsoft YaHei,Noto Sans CJK SC,sans-serif;
 -webkit-font-smoothing:antialiased;}
.wrap{max-width:1100px;margin:0 auto;padding:40px 24px 64px;}
header.hd{text-align:center;margin-bottom:34px;}
.hd .kicker{color:var(--primary);letter-spacing:.28em;font-size:12px;font-weight:700;text-transform:uppercase;}
.hd h1{font-size:32px;margin:10px 0 6px;letter-spacing:.5px;}
.hd p{color:var(--muted);margin:0;font-size:14px;}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:26px 0 34px;}
.kpi{background:#fff;border:1px solid #E6EDF5;border-radius:14px;padding:18px 16px;text-align:center;
 box-shadow:0 1px 2px rgba(15,23,43,.04);}
.kpi .num{font-size:30px;font-weight:800;color:var(--primary);line-height:1.1;}
.kpi .cap{font-size:12px;color:var(--muted);margin-top:6px;}
.card{background:#fff;border:1px solid #E6EDF5;border-radius:16px;padding:22px 24px;margin-bottom:22px;
 box-shadow:0 1px 3px rgba(15,23,43,.04);}
.card h2{font-size:18px;margin:0 0 4px;}
.card .sub{font-size:12.5px;color:var(--muted);margin:0 0 16px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:22px;}
@media(max-width:820px){.grid2{grid-template-columns:1fr;}}
.donut-row{display:flex;align-items:center;gap:20px;flex-wrap:wrap;justify-content:center;}
.legend{min-width:190px;}
.lg-item{display:flex;align-items:center;gap:8px;font-size:13px;padding:5px 0;border-bottom:1px dashed #EEF2F7;}
.lg-dot{width:11px;height:11px;border-radius:3px;flex:none;}
.lg-label{flex:1;color:#334155;}
.lg-val{font-weight:700;color:#0F172B;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th,td{padding:8px 10px;border-bottom:1px solid #EEF2F7;text-align:left;white-space:nowrap;}
th{background:#F8FAFD;color:#475569;font-size:12px;font-weight:700;position:sticky;top:0;}
td.en{color:#64748B;}
.tw{max-height:520px;overflow:auto;border:1px solid #EEF2F7;border-radius:12px;}
.bars{display:flex;flex-direction:column;gap:9px;}
.bar-row{display:flex;align-items:center;gap:12px;}
.bar-lab{flex:none;width:140px;text-align:right;font-size:13px;color:#0F172B;line-height:1.3;}
.bar-track{flex:1;display:flex;flex-direction:column;gap:5px;}
.bar-line{flex:1;display:flex;align-items:center;gap:6px;height:15px;background:#F1F5F9;border-radius:4px;}
.bar-fill{height:100%;border-radius:4px;min-width:2px;}
.bar-num{font-size:13px;font-weight:600;color:#0F172B;}
@media(max-width:820px){.bar-lab{width:104px;font-size:12.5px;}}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11.5px;font-weight:600;color:#fff;}
footer{text-align:center;color:#94A3B8;font-size:12px;margin-top:34px;}
"""


def build(phd_rows, mst_rows):
    phd = []
    for name, year, raw in phd_rows:
        cat, field, org, org_zh = PHD[name]
        phd.append(dict(name=name, zh=NAME_ZH.get(name, name), year=year,
                        raw=raw, cat=cat, field=field, org=org, org_zh=org_zh,
                        degree="Ph.D."))
    mst = []
    for name, year, raw in mst_rows:
        cat, field, org, org_zh = MASTER[name]
        mst.append(dict(name=name, zh=NAME_ZH.get(name, name), year=year,
                        raw=raw, cat=cat, field=field, org=org, org_zh=org_zh,
                        degree="Master"))
    allp = phd + mst

    # KPI
    employers = {p["org"] for p in allp}
    years = sorted({p["year"] for p in allp})
    acad = sum(1 for p in allp if p["cat"] == "academia")
    further = sum(1 for p in allp if p["cat"] == "further")
    industry = sum(1 for p in allp if p["cat"] == "industry")

    kpis = [
        (len(phd), "博士毕业生"),
        (len(mst), "硕士毕业生"),
        (len(allp), "毕业生总数"),
        (acad, "高校 / 科研院所"),
        (industry, "企业就业"),
        (further, "继续深造"),
    ]

    def cat_data(rows):
        c = collections.Counter(r["cat"] for r in rows)
        return [(CAT_LABEL[k], c[k], CAT_COLOR[k]) for k in ["academia", "industry", "further"] if c.get(k)]

    # field distribution (grouped)
    rows_field = []
    for key, label in FIELD_LABEL:
        p = sum(1 for r in phd if r["field"] == key)
        m = sum(1 for r in mst if r["field"] == key)
        if p or m:
            rows_field.append((label, [("博士", p, "#FEA116"), ("硕士", m, "#0F172B")]))

    # employers
    emp = collections.Counter()
    for r in allp:
        emp[(r["org"], r["org_zh"])] += 1
    top = emp.most_common(16)
    emp_rows = [(f"{zh}（{en}）" if zh != en else en, n, "#FEA116") for (en, zh), n in top]

    # by year
    year_labels = [str(y) for y in years]
    phd_by_year = [sum(1 for r in phd if r["year"] == y) for y in years]
    mst_by_year = [sum(1 for r in mst if r["year"] == y) for y in years]
    year_series = [("博士", phd_by_year, "#FEA116"), ("硕士", mst_by_year, "#0F172B")]

    # top destination type overall
    overall = cat_data(allp)

    parts = []
    parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>毕业生去向统计 · IIP Lab</title>
<style>{CSS}</style></head><body><div class="wrap">
<header class="hd">
  <div class="kicker">IIP Lab · Xidian University</div>
  <h1>毕业生去向统计与可视化</h1>
  <p>去向单位数 {len(employers)} 家 · 毕业年份跨度 {years[0]}–{years[-1]}</p>
</header>
<div class="kpis">""")
    for num, cap in kpis:
        parts.append(f'<div class="kpi"><div class="num">{num}</div><div class="cap">{cap}</div></div>')
    parts.append("</div>")

    # 1. donuts
    parts.append(f"""<div class="grid2">
  <div class="card"><h2>博士毕业生去向类型</h2><p class="sub">共 {len(phd)} 人，按就业性质划分</p>
    <div class="donut-row">{donut(cat_data(phd), title="博士")}{legend(cat_data(phd))}</div></div>
  <div class="card"><h2>硕士毕业生去向类型</h2><p class="sub">共 {len(mst)} 人，按就业性质划分</p>
    <div class="donut-row">{donut(cat_data(mst), title="硕士")}{legend(cat_data(mst))}</div></div>
</div>""")

    # 2. overall
    parts.append(f"""<div class="card"><h2>全体毕业生去向构成</h2>
<p class="sub">博士 + 硕士 共 {len(allp)} 人</p>
<div class="donut-row">{donut(overall, size=240, title="总计")}{legend(overall)}</div></div>""")

    # 3. fields
    parts.append(f"""<div class="card"><h2>行业领域分布（博士 vs 硕士）</h2>
<p class="sub">橙色为博士，深色为硕士；单位：人</p>
<div class="legend" style="margin-bottom:10px">
  <div class="lg-item"><span class="lg-dot" style="background:#FEA116"></span><span class="lg-label">博士</span></div>
  <div class="lg-item"><span class="lg-dot" style="background:#0F172B"></span><span class="lg-label">硕士</span></div>
</div>
{grouped_bars_html(rows_field)}</div>""")

    # 4. employers
    parts.append(f"""<div class="card"><h2>主要去向单位 Top {len(emp_rows)}</h2>
<p class="sub">博士与硕士合并统计，共覆盖 {len(employers)} 家单位/机构</p>
{bars_html(emp_rows)}</div>""")

    # 5. by year
    parts.append(f"""<div class="card"><h2>各年份毕业人数</h2>
<p class="sub">柱顶数字为该年毕业生总数</p>
{stacked_columns(year_labels, year_series)}</div>""")

    parts.append("<footer>数据来源：team.html · Alumni（PH.D. / Postgraduates）· 由 tools/alumni_stats.py 自动生成</footer></div></body></html>")
    return "".join(parts)


def main():
    phd_rows, mst_rows = parse_team_html()
    missing_p = [n for n, _, _ in phd_rows if n not in PHD]
    missing_m = [n for n, _, _ in mst_rows if n not in MASTER]
    if missing_p or missing_m:
        print("!! 以下姓名缺少分类映射，请补充：", missing_p, missing_m)
        return 1
    print(f"博士 {len(phd_rows)} 人 / 硕士 {len(mst_rows)} 人，共 {len(phd_rows)+len(mst_rows)} 人")
    OUT_HTML.write_text(build(phd_rows, mst_rows), encoding="utf-8")
    print("written:", OUT_HTML)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
