#!/usr/bin/env python3
"""Build a monthly startup financial model from an assumptions file.

Usage:
    python build_model.py assumptions.json [--out model] [--lang en|ar] [--no-xlsx]

Writes:
    <out>.md    summary, unit economics and warnings (always)
    <out>.csv   month-by-month figures (always)
    <out>.xlsx  workbook with live formulas (when openpyxl is installed)

The workbook recalculates when you change the Assumptions sheet. The .md and
.csv are computed in Python with the same logic, so the two can be compared.

Exit status: 0 built, 1 built with blocking warnings (cash runs out), 2 bad input.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REQUIRED = [
    "company", "currency", "start", "months", "starting_cash",
    "new_customers_month_1", "new_customer_growth", "monthly_churn",
    "revenue_per_customer", "gross_margin", "acquisition_cost_per_customer",
    "other_opex_month_1", "other_opex_growth", "team", "funding",
]
RATES = ["new_customer_growth", "monthly_churn", "gross_margin", "other_opex_growth"]

L = {
    "en": {
        "sheets": ["Assumptions", "Team", "Funding", "Monthly", "Summary"],
        "assump": ["Company", "Currency", "First month", "Starting cash",
                   "New customers in month 1", "Monthly growth in new customers",
                   "Monthly churn", "Monthly revenue per customer", "Gross margin",
                   "Acquisition cost per customer", "Other operating costs in month 1",
                   "Monthly growth in other operating costs"],
        "item": "Item", "value": "Value",
        "team": ["Role", "Monthly cost", "Start month"],
        "funding": ["Month", "Amount", "Label"],
        "monthly": ["Month", "Period", "New customers", "Churned customers",
                    "Customers at month end", "Revenue", "Cost of revenue",
                    "Gross profit", "Acquisition spend", "Payroll",
                    "Other operating costs", "Operating result", "Funding received",
                    "Cash at month end", "Break-even flag", "Cash-out flag"],
        "year": "Year", "metric": "Metric",
        "sum": ["Revenue", "Gross profit", "Operating result", "Funding received",
                "Customers at year end", "Cash at year end"],
        "ue": ["Lifetime value per customer", "Lifetime value to acquisition cost",
               "Payback on acquisition cost (months)", "First break-even month",
               "Lowest cash balance", "Month of lowest cash", "First month cash is negative"],
        "na": "none", "span": "{months} months from {start}, in {cur}.",
        "title": "Financial model summary", "years": "Yearly summary",
        "unit": "Unit economics and cash", "warn": "Checks", "ok": "No warnings.",
        "note": "Figures are projections built from the assumptions file. They are not a forecast audited by anyone, and not financial advice.",
    },
    "ar": {
        "sheets": ["الافتراضات", "الفريق", "التمويل", "الشهري", "الملخص"],
        "assump": ["المنشأة", "العملة", "الشهر الأول", "النقد الافتتاحي",
                   "العملاء الجدد في الشهر الأول", "النمو الشهري للعملاء الجدد",
                   "التسرب الشهري", "الإيراد الشهري لكل عميل", "هامش الربح الإجمالي",
                   "كلفة الاستحواذ لكل عميل", "المصروفات التشغيلية الأخرى في الشهر الأول",
                   "النمو الشهري للمصروفات التشغيلية الأخرى"],
        "item": "البند", "value": "القيمة",
        "team": ["الدور", "الكلفة الشهرية", "شهر البدء"],
        "funding": ["الشهر", "المبلغ", "البيان"],
        "monthly": ["الشهر", "الفترة", "العملاء الجدد", "العملاء المتسربون",
                    "العملاء نهاية الشهر", "الإيراد", "كلفة الإيراد",
                    "الربح الإجمالي", "إنفاق الاستحواذ", "الرواتب",
                    "مصروفات تشغيلية أخرى", "النتيجة التشغيلية", "التمويل المستلم",
                    "النقد نهاية الشهر", "مؤشر التعادل", "مؤشر نفاد النقد"],
        "year": "السنة", "metric": "المؤشر",
        "sum": ["الإيراد", "الربح الإجمالي", "النتيجة التشغيلية", "التمويل المستلم",
                "العملاء نهاية السنة", "النقد نهاية السنة"],
        "ue": ["القيمة الدائمة للعميل", "نسبة القيمة الدائمة إلى كلفة الاستحواذ",
               "مدة استرداد كلفة الاستحواذ (بالأشهر)", "أول شهر تعادل",
               "أدنى رصيد نقدي", "شهر أدنى رصيد نقدي", "أول شهر يصبح فيه النقد سالبًا"],
        "na": "لا يوجد", "span": "{months} شهرًا ابتداءً من {start}، بعملة {cur}.",
        "title": "ملخص النموذج المالي", "years": "الملخص السنوي",
        "unit": "اقتصاديات الوحدة والنقد", "warn": "الفحوص", "ok": "لا توجد تنبيهات.",
        "note": "الأرقام توقعات مبنية على ملف الافتراضات. ليست توقعات مدققة وليست استشارة مالية.",
    },
}


def fail(msg: str):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def load(path: Path) -> dict:
    try:
        a = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        fail(f"cannot read {path}: {e}")
    missing = [k for k in REQUIRED if k not in a]
    if missing:
        fail("missing fields: " + ", ".join(missing))
    for k in RATES:
        if not isinstance(a[k], (int, float)) or not 0 <= a[k] <= 1:
            fail(f"{k} must be a decimal between 0 and 1 (0.03 means 3%), got {a[k]!r}")
    if not isinstance(a["months"], int) or not 12 <= a["months"] <= 60:
        fail("months must be a whole number from 12 to 60")
    try:
        y, m = (int(x) for x in str(a["start"]).split("-"))
        assert 1 <= m <= 12
    except Exception:
        fail("start must look like 2027-01")
    for t in a["team"]:
        if not {"role", "monthly_cost", "start_month"} <= set(t):
            fail("each team entry needs role, monthly_cost, start_month")
    for f in a["funding"]:
        if not {"month", "amount"} <= set(f):
            fail("each funding entry needs month and amount")
    for k in ["starting_cash", "new_customers_month_1", "revenue_per_customer",
              "acquisition_cost_per_customer", "other_opex_month_1"]:
        if not isinstance(a[k], (int, float)) or a[k] < 0:
            fail(f"{k} must be a number, zero or more")
    return a


def period(start: str, i: int) -> str:
    y, m = (int(x) for x in start.split("-"))
    m0 = (m - 1) + (i - 1)
    return f"{y + m0 // 12}-{m0 % 12 + 1:02d}"


def compute(a: dict) -> list:
    rows, customers, cash = [], 0.0, float(a["starting_cash"])
    for i in range(1, a["months"] + 1):
        new = a["new_customers_month_1"] * (1 + a["new_customer_growth"]) ** (i - 1)
        churned = customers * a["monthly_churn"]
        customers = customers - churned + new
        revenue = customers * a["revenue_per_customer"]
        cogs = revenue * (1 - a["gross_margin"])
        gross = revenue - cogs
        acq = new * a["acquisition_cost_per_customer"]
        payroll = sum(t["monthly_cost"] for t in a["team"] if t["start_month"] <= i)
        opex = a["other_opex_month_1"] * (1 + a["other_opex_growth"]) ** (i - 1)
        result = gross - acq - payroll - opex
        funding = sum(f["amount"] for f in a["funding"] if f["month"] == i)
        cash = cash + result + funding
        rows.append([i, period(a["start"], i), new, churned, customers, revenue, cogs,
                     gross, acq, payroll, opex, result, funding, cash])
    return rows


def metrics(a: dict, rows: list) -> dict:
    margin_per_customer = a["revenue_per_customer"] * a["gross_margin"]
    ltv = margin_per_customer / a["monthly_churn"] if a["monthly_churn"] else None
    cac = a["acquisition_cost_per_customer"]
    cash = [r[13] for r in rows]
    low = min(cash)
    return {
        "ltv": ltv,
        "ltv_cac": (ltv / cac) if (ltv is not None and cac) else None,
        "payback": (cac / margin_per_customer) if margin_per_customer else None,
        "breakeven": next((r[0] for r in rows if r[11] >= 0), None),
        "low_cash": low,
        "low_month": rows[cash.index(low)][0],
        "cash_out": next((r[0] for r in rows if r[13] < 0), None),
    }


def yearly(rows: list) -> list:
    out = []
    for y in range((len(rows) + 11) // 12):
        chunk = rows[y * 12:(y + 1) * 12]
        out.append([sum(r[5] for r in chunk), sum(r[7] for r in chunk),
                    sum(r[11] for r in chunk), sum(r[12] for r in chunk),
                    chunk[-1][4], chunk[-1][13]])
    return out


def checks(a: dict, rows: list, m: dict, lang: str) -> list:
    """Return (blocking, text) pairs."""
    ar = lang == "ar"
    out = []
    cur = a["currency"]
    if m["cash_out"]:
        out.append((True,
            f"النقد يصبح سالبًا في الشهر {m['cash_out']}. الخطة غير ممولة: زد التمويل أو أخّر التوظيف أو خفّض المصروفات."
            if ar else
            f"Cash turns negative in month {m['cash_out']}. The plan is not funded: raise more, delay hires or cut costs."))
    churn = a["monthly_churn"]
    if churn >= 0.05:
        yr = 1 - (1 - churn) ** 12
        out.append((False,
            f"التسرب الشهري {churn:.1%} يعني خسارة {yr:.0%} من العملاء خلال سنة. عالج الاحتفاظ قبل الإنفاق على النمو."
            if ar else
            f"Monthly churn of {churn:.1%} loses {yr:.0%} of customers within a year. Fix retention before spending on growth."))
    if churn == 0:
        out.append((False,
            "التسرب صفر. لا توجد منشأة بلا تسرب؛ استخدم رقمًا مرصودًا أو افتراضًا متحفظًا."
            if ar else
            "Churn is zero. No business keeps every customer; use an observed figure or a cautious assumption."))
    if m["ltv_cac"] is not None and m["ltv_cac"] < 3:
        out.append((False,
            f"نسبة القيمة الدائمة إلى كلفة الاستحواذ {m['ltv_cac']:.1f}، وهي دون 3. كل عميل جديد يعيد أقل مما يُعدّ مريحًا."
            if ar else
            f"Lifetime value is {m['ltv_cac']:.1f} times acquisition cost, below 3. Each new customer returns less than is usually considered comfortable."))
    if m["payback"] is not None and m["payback"] > 18:
        out.append((False,
            f"استرداد كلفة الاستحواذ يستغرق {m['payback']:.0f} شهرًا. النمو سيستهلك النقد أسرع مما يولّده."
            if ar else
            f"Acquisition cost takes {m['payback']:.0f} months to pay back. Growth will consume cash faster than it produces it."))
    g = a["new_customer_growth"]
    if g > 0.10:
        mult = (1 + g) ** (a["months"] - 1)
        out.append((False,
            f"نمو شهري {g:.0%} في العملاء الجدد طوال {a['months']} شهرًا يعني مضاعفة الاستحواذ الشهري {mult:.0f} مرة. تحقق من أن القناة تتحمل ذلك."
            if ar else
            f"New-customer growth of {g:.0%} a month for {a['months']} months multiplies monthly acquisition {mult:.0f} times. Check that the channel can carry it."))
    if a["gross_margin"] > 0.9:
        out.append((False,
            "هامش الربح الإجمالي فوق 90%. تأكد من إدراج كلفة استخدام النماذج والاستضافة والدعم ضمن كلفة الإيراد."
            if ar else
            "Gross margin is above 90%. Confirm that model usage, hosting and support costs are inside cost of revenue."))
    if a["acquisition_cost_per_customer"] == 0:
        out.append((False,
            "كلفة الاستحواذ صفر. حتى القنوات المجانية تستهلك وقتًا مدفوعًا."
            if ar else
            "Acquisition cost is zero. Even free channels consume paid time."))
    end_customers = rows[-1][4]
    out.append((False,
        f"للمطابقة: النموذج يفترض {end_customers:,.0f} عميلًا وإيرادًا شهريًا {rows[-1][5]:,.0f} {cur} في الشهر {a['months']}. قارن ذلك بالحصة السوقية الممكنة."
        if ar else
        f"For cross-checking: the model implies {end_customers:,.0f} customers and {rows[-1][5]:,.0f} {cur} monthly revenue in month {a['months']}. Compare with your obtainable market."))
    return out


def fmt(v, digits=0):
    return "" if v is None else f"{v:,.{digits}f}"


def write_csv(path: Path, rows: list, lang: str):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(L[lang]["monthly"][:14])
        for r in rows:
            w.writerow(r[:2] + [round(x, 2) for x in r[2:]])


def write_md(path: Path, a: dict, rows: list, m: dict, warnings: list, lang: str):
    t = L[lang]
    ys = yearly(rows)
    cur = a["currency"]
    out = [f"# {t['title']}: {a['company']}", "",
           t["span"].format(months=a["months"], start=a["start"], cur=cur), "",
           f"## {t['years']}", "",
           "| " + t["metric"] + " | " + " | ".join(f"{t['year']} {i + 1}" for i in range(len(ys))) + " |",
           "|---|" + "---:|" * len(ys)]
    for k, name in enumerate(t["sum"]):
        out.append(f"| {name} | " + " | ".join(fmt(y[k]) for y in ys) + " |")
    na = t["na"]
    vals = [fmt(m["ltv"]) or na, fmt(m["ltv_cac"], 1) or na, fmt(m["payback"], 1) or na,
            str(m["breakeven"] or na), fmt(m["low_cash"]), str(m["low_month"]),
            str(m["cash_out"] or na)]
    out += ["", f"## {t['unit']}", "", f"| {t['metric']} | {t['value']} |", "|---|---:|"]
    out += [f"| {n} | {v} |" for n, v in zip(t["ue"], vals)]
    out += ["", f"## {t['warn']}", ""]
    out += [f"- {'**' if b else ''}{w}{'**' if b else ''}" for b, w in warnings] or [t["ok"]]
    out += ["", t["note"], ""]
    path.write_text("\n".join(out), encoding="utf-8")


def write_xlsx(path: Path, a: dict, lang: str) -> bool:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter as col
    except ImportError:
        return False
    t = L[lang]
    sa, st, sf, sm, ss = t["sheets"]
    q = lambda name: f"'{name}'"
    n = a["months"]
    last = n + 1
    rtl = lang == "ar"
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor="1F3A5F")
    input_fill = PatternFill("solid", fgColor="FFF4CC")

    def header(ws, labels, row=1):
        for c, label in enumerate(labels, 1):
            cell = ws.cell(row=row, column=c, value=label)
            cell.font, cell.fill = head_font, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.freeze_panes = ws.cell(row=row + 1, column=1)
        ws.sheet_view.rightToLeft = rtl

    wb = Workbook()
    ws = wb.active
    ws.title = sa
    header(ws, [t["item"], t["value"]])
    keys = ["company", "currency", "start", "starting_cash", "new_customers_month_1",
            "new_customer_growth", "monthly_churn", "revenue_per_customer", "gross_margin",
            "acquisition_cost_per_customer", "other_opex_month_1", "other_opex_growth"]
    for r, (label, key) in enumerate(zip(t["assump"], keys), 2):
        ws.cell(row=r, column=1, value=label)
        c = ws.cell(row=r, column=2, value=a[key])
        c.fill = input_fill
        if key in RATES:
            c.number_format = "0.0%"
        elif isinstance(a[key], (int, float)):
            c.number_format = "#,##0"
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 44, 18
    A = lambda r: f"{q(sa)}!$B${r}"
    CASH0, NEW1, GROW, CHURN, ARPA, GM, CAC, OPEX1, OPEXG = (A(r) for r in range(5, 14))

    wt = wb.create_sheet(st)
    header(wt, t["team"])
    for r, m_ in enumerate(a["team"], 2):
        wt.cell(row=r, column=1, value=m_["role"])
        wt.cell(row=r, column=2, value=m_["monthly_cost"]).number_format = "#,##0"
        wt.cell(row=r, column=3, value=m_["start_month"])
        for c in (2, 3):
            wt.cell(row=r, column=c).fill = input_fill
    wt.column_dimensions["A"].width = 28
    wt.column_dimensions["B"].width = wt.column_dimensions["C"].width = 16

    wf = wb.create_sheet(sf)
    header(wf, t["funding"])
    for r, f_ in enumerate(a["funding"], 2):
        wf.cell(row=r, column=1, value=f_["month"]).fill = input_fill
        c = wf.cell(row=r, column=2, value=f_["amount"])
        c.fill, c.number_format = input_fill, "#,##0"
        wf.cell(row=r, column=3, value=f_.get("label", ""))
    wf.column_dimensions["B"].width, wf.column_dimensions["C"].width = 16, 30

    wm = wb.create_sheet(sm)
    header(wm, t["monthly"])
    for i in range(1, n + 1):
        r = i + 1
        p = r - 1
        wm.cell(row=r, column=1, value=i)
        wm.cell(row=r, column=2, value=period(a["start"], i))
        f = {
            3: f"={NEW1}*(1+{GROW})^(A{r}-1)",
            4: "=0" if i == 1 else f"=E{p}*{CHURN}",
            5: f"=C{r}" if i == 1 else f"=E{p}-D{r}+C{r}",
            6: f"=E{r}*{ARPA}",
            7: f"=F{r}*(1-{GM})",
            8: f"=F{r}-G{r}",
            9: f"=C{r}*{CAC}",
            10: f"=SUMIF({q(st)}!$C$2:$C$200,\"<=\"&A{r},{q(st)}!$B$2:$B$200)",
            11: f"={OPEX1}*(1+{OPEXG})^(A{r}-1)",
            12: f"=H{r}-I{r}-J{r}-K{r}",
            13: f"=SUMIF({q(sf)}!$A$2:$A$200,A{r},{q(sf)}!$B$2:$B$200)",
            14: (f"={CASH0}+L{r}+M{r}" if i == 1 else f"=N{p}+L{r}+M{r}"),
            15: f"=IF(L{r}>=0,A{r},\"\")",
            16: f"=IF(N{r}<0,A{r},\"\")",
        }
        for c, formula in f.items():
            cell = wm.cell(row=r, column=c, value=formula)
            if c <= 14:
                cell.number_format = "#,##0"
    for c in range(1, 17):
        wm.column_dimensions[col(c)].width = 15
    wm.row_dimensions[1].height = 34
    M = lambda letter: f"{q(sm)}!${letter}$2:${letter}${last}"

    wsu = wb.create_sheet(ss)
    years = (n + 11) // 12
    header(wsu, [t["metric"]] + [f"{t['year']} {y + 1}" for y in range(years)])
    cols = ["F", "H", "L", "M"]
    for k, name in enumerate(t["sum"]):
        r = k + 2
        wsu.cell(row=r, column=1, value=name)
        for y in range(years):
            lo, hi = y * 12 + 1, min((y + 1) * 12, n)
            if k < 4:
                v = (f"=SUMIFS({M(cols[k])},{M('A')},\">={lo}\",{M('A')},\"<={hi}\")")
            else:
                v = f"={q(sm)}!{'E' if k == 4 else 'N'}{hi + 1}"
            wsu.cell(row=r, column=y + 2, value=v).number_format = "#,##0"
    base = len(t["sum"]) + 4
    hcell = wsu.cell(row=base - 1, column=1, value=t["unit"])
    hcell.font = Font(bold=True)
    na = t["na"]
    ue = [
        (f"=IF({CHURN}=0,\"{na}\",{ARPA}*{GM}/{CHURN})", "#,##0"),
        (f"=IF(OR({CHURN}=0,{CAC}=0),\"{na}\",{ARPA}*{GM}/{CHURN}/{CAC})", "0.0"),
        (f"=IF({ARPA}*{GM}=0,\"{na}\",{CAC}/({ARPA}*{GM}))", "0.0"),
        (f"=IF(COUNT({M('O')})=0,\"{na}\",MIN({M('O')}))", "0"),
        (f"=MIN({M('N')})", "#,##0"),
        (f"=INDEX({M('A')},MATCH(MIN({M('N')}),{M('N')},0))", "0"),
        (f"=IF(COUNT({M('P')})=0,\"{na}\",MIN({M('P')}))", "0"),
    ]
    for k, (name, (formula, nf)) in enumerate(zip(t["ue"], ue)):
        wsu.cell(row=base + k, column=1, value=name)
        wsu.cell(row=base + k, column=2, value=formula).number_format = nf
    wsu.column_dimensions["A"].width = 46
    for y in range(years):
        wsu.column_dimensions[col(y + 2)].width = 18
    wb.move_sheet(ss, offset=-4)
    wb.save(path)
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("assumptions")
    ap.add_argument("--out", default="model", help="output path without extension")
    ap.add_argument("--lang", choices=["en", "ar"], default="en")
    ap.add_argument("--no-xlsx", action="store_true")
    args = ap.parse_args(argv)

    a = load(Path(args.assumptions))
    rows = compute(a)
    m = metrics(a, rows)
    warnings = checks(a, rows, m, args.lang)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ext = lambda e: out.parent / (out.name + e)   # keeps dots in names such as model.ar
    write_csv(ext(".csv"), rows, args.lang)
    write_md(ext(".md"), a, rows, m, warnings, args.lang)
    made = [ext(".md"), ext(".csv")]
    if not args.no_xlsx:
        if write_xlsx(ext(".xlsx"), a, args.lang):
            made.append(ext(".xlsx"))
        else:
            print("note: openpyxl is not installed, so no .xlsx was written "
                  "(pip install openpyxl)", file=sys.stderr)
    print("wrote " + ", ".join(str(p) for p in made))
    for blocking, w in warnings:
        print(("BLOCKING: " if blocking else "check: ") + w)
    return 1 if any(b for b, _ in warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
