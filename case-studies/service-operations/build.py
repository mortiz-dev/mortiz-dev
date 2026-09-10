"""Generate synthetic service-operations data and validate/export its analysis.

Python 3.11+; matplotlib is required only to render the chart.
Run: python3 build.py
"""
from pathlib import Path
import csv
import sqlite3

ROOT = Path(__file__).resolve().parent
CHANNELS = ("Mobile app", "Web", "Contact center", "Branch")
# Explicit fictional scenario: volumes rise; channel service levels diverge.
BASE_VOLUME = (1000, 700, 550, 350)
MONTHLY_GROWTH = (35, 20, 10, 5)
START_SLA = (96, 95, 93, 92)
MONTHLY_CHANGE = (0.1, 0.05, -0.45, -0.65)


def write_csv(path, names, rows):
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(names)
        writer.writerows(rows)


def main():
    rows = []
    for month_index in range(12):
        for i, channel in enumerate(CHANNELS):
            volume = BASE_VOLUME[i] + month_index * MONTHLY_GROWTH[i]
            rate = START_SLA[i] + month_index * MONTHLY_CHANGE[i]
            within = round(volume * rate / 100)
            rows.append((f"2025-{month_index + 1:02d}", channel, volume, within, "synthetic"))
    assert len(rows) == 48
    assert len({(r[0], r[1]) for r in rows}) == len(rows)
    assert all(0 <= r[3] <= r[2] and r[2] > 0 and r[4] == "synthetic" for r in rows)
    write_csv(ROOT / "data.csv", ("month", "channel", "closed_cases", "within_sla", "source"), rows)
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE service_operations (month TEXT, channel TEXT, closed_cases INTEGER, within_sla INTEGER, source TEXT, PRIMARY KEY (month, channel), CHECK (closed_cases > 0 AND within_sla BETWEEN 0 AND closed_cases))")
        db.executemany("INSERT INTO service_operations VALUES (?, ?, ?, ?, ?)", rows)
        monthly = db.execute((ROOT / "metrics.sql").read_text()).fetchall()
        latest = db.execute("SELECT channel, closed_cases, within_sla, 100.0 * within_sla / closed_cases FROM service_operations WHERE month = '2025-12' ORDER BY 4 DESC").fetchall()
    # Independently reconcile SQL aggregates against source records.
    assert len(monthly) == 12
    for month, volume, within, rate in monthly:
        source = [r for r in rows if r[0] == month]
        assert volume == sum(r[2] for r in source)
        assert within == sum(r[3] for r in source)
        assert abs(rate - 100 * within / volume) <= 0.0051
    write_csv(ROOT / "monthly-kpis.csv", ("month", "closed_cases", "within_sla", "sla_pct"), monthly)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none"})
    ink, blue, neutral = "#18212F", "#2563EB", "#64748B"
    fig, axes = plt.subplots(2, 1, figsize=(10, 9), gridspec_kw={"height_ratios": [1, 1.2]})
    fig.patch.set_facecolor("white")
    fig.suptitle("Service operations | synthetic portfolio case", x=0.1, y=0.98, ha="left", fontsize=19, color=ink, weight="bold")
    fig.text(0.1, 0.925, "Illustrative closed cases, Jan–Dec 2025. No real customer or bank data.", color=neutral)
    ax = axes[0]
    ax.plot(range(12), [r[3] for r in monthly], color=blue, marker="o", linewidth=2)
    ax.set_xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Within SLA (%)")
    ax.set_title("Overall compliance hides channel differences", loc="left", pad=17, color=ink, weight="bold")
    for index in (0, 11):
        ax.annotate(f"{monthly[index][3]:.1f}%", (index, monthly[index][3]), xytext=(0, -22), textcoords="offset points", ha="center", color=ink)
    ax = axes[1]
    ax.barh([r[0] for r in latest], [r[3] for r in latest], color=blue, edgecolor=ink, linewidth=0.6, height=0.55)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Closed cases within the illustrative SLA (%)")
    ax.set_title("December: branch has the lowest compliance", loc="left", pad=20, color=ink, weight="bold")
    for index, (_, volume, _, rate) in enumerate(latest):
        ax.text(3, index, f"{rate:.1f}%  |  n={volume:,}", va="center", color="white", weight="bold")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(neutral)
        ax.tick_params(colors=ink)
        ax.set_axisbelow(True)
    fig.text(0.1, 0.025, "SLA = cases closed within 2 business days / all closed cases.\nSource: generated data.csv (48 month-channel rows); weighted ratios, no causal inference.", fontsize=10, color=neutral)
    fig.subplots_adjust(left=0.18, right=0.95, top=0.85, bottom=0.13, hspace=0.55)
    fig.savefig(ROOT / "service-operations.png", dpi=160, facecolor="white")
    plt.close(fig)
    print(f"Validated {len(rows)} rows and {len(monthly)} monthly aggregates.")
    print("December:", latest)


if __name__ == "__main__":
    main()
