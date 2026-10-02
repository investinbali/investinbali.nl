"""Render the Seseh scenario table from one explicit set of assumptions."""
import json
from decimal import Decimal
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def calculate(model):
    d = lambda value: Decimal(str(value))
    rows = []
    for scenario in model["scenarios"]:
        nights = d(model["daysPerMonth"]) * d(scenario["occupancy"])
        gross = nights * d(model["dailyRate"])
        ota = gross * d(model["platformRate"])
        management = gross * d(model["managementRate"])
        extra = d(scenario["extraMonthlyRevenue"])
        fixed = d(model["fixedMonthlyCosts"])
        monthly = gross - ota - management - fixed + extra
        annual = monthly * d(model["monthsPerYear"])
        rows.append(dict(name=scenario["name"], occupancy=d(scenario["occupancy"])*100,
                         nights=nights, gross=gross, ota=-ota, management=-management,
                         fixed=-fixed, extra=extra, monthly=monthly, annual=annual,
                         yield_pct=annual/d(model["investment"])*100,
                         payback=d(model["investment"])/annual))
    return rows


def render(model):
    rows = calculate(model)
    money = lambda value: f"IDR {value / Decimal(1000000):.1f}M"
    fields = [
        ("Geboekte nachten / maand", "nights", lambda v: f"{v:.0f}"),
        ("Bruto verhuuromzet / maand", "gross", money),
        ("OTA / platform 15,5% van verhuuromzet", "ota", money),
        ("Management 20% van verhuuromzet", "management", money),
        ("Schoonmaak, onderhoud, nutsvoorzieningen, amenities", "fixed", money),
        ("Extra diensten: aanvullende omzet (aanname)", "extra", money),
        ("Operationeel resultaat / maand*", "monthly", money),
        ("Operationeel resultaat / jaar*", "annual", money),
        ("Operationeel resultaat / aankoopprijs*", "yield_pct", lambda v: f"{v:.1f}%"),
        ("Eenvoudige terugverdientijd vanaf exploitatie*", "payback", lambda v: f"{v:.1f} jaar"),
    ]
    markup = '<table class="seseh-return-table">\n<caption>Rekenscenario per villa; geen rendementsbelofte</caption>\n<thead><tr><th scope="col">Scenario</th>'
    markup += ''.join(f'<th scope="col">{escape(row["name"])}<br />{row["occupancy"]:.0f}% bezetting</th>' for row in rows)
    markup += '</tr></thead>\n<tbody>\n'
    for label, key, formatter in fields:
        markup += f'<tr><th scope="row">{escape(label)}</th>'
        markup += ''.join(f'<td>{formatter(row[key])}</td>' for row in rows) + '</tr>\n'
    return markup + '</tbody></table>'


if __name__ == "__main__":
    import re
    model = json.loads((ROOT / "data/seseh-scenarios.json").read_text(encoding="utf-8"))
    path = ROOT / "projecten/seseh-boutique-villas/index.html"
    markup = path.read_text(encoding="utf-8")
    markup, count = re.subn(r'<table class="seseh-return-table">.*?</table>', lambda _: render(model), markup, count=1, flags=re.S)
    assert count == 1, "Missing scenario table"
    path.write_text(markup, encoding="utf-8")
