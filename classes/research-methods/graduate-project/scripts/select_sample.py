"""Draw the random sample of wells for the wellbore diagram pilot study.

Usage (from any folder; the CSV path defaults to ../05-data/calgem/):
    python select_sample.py [path/to/2021CaliforniaOilAndGasWells.csv]

Writes ../06-study/sample/screening-log.csv: every Active or Idle well in one random order.
Rows 1-30 are the primary sample; every later row is the replacement queue,
used strictly in order. See ../06-study/sample/sampling-plan.txt for the rules.

Requires only the Python standard library.
"""
import csv
import random
import sys
from pathlib import Path

SEED = 20261111          # fixed before any well was screened; recorded in the plan
PRIMARY_N = 30           # pilot sample size (sampling-plan.txt, section 3)
STATUSES = {"Active", "Idle"}
HERE = Path(__file__).parent
OUT = HERE.parent / "06-study" / "sample" / "screening-log.csv"
DEFAULT_CSV = HERE.parent / "05-data" / "calgem" / "2021CaliforniaOilAndGasWells.csv"

# Columns kept from the CalGEM file. Operator fields are deliberately left out:
# the operator plays no part in selection and is not recorded in the log.
KEEP = ["API", "LeaseName", "WellNumber", "WellStatus", "WellTypeCode",
        "FieldName", "County", "District"]
LOG_FIELDS = ["Order", "Role", "API10"] + KEEP + [
    "Outcome", "WellSTAR_Status", "DocumentID", "DocumentRelevantDate",
    "DocumentDescription", "CheckedOn", "Notes"]


def load_population(path):
    """One row per distinct 12-digit API (first row in file order), Active or Idle only."""
    wells = {}
    with open(path, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["API"] not in wells:
                wells[row["API"]] = row
    return [r for r in wells.values() if r["WellStatus"] in STATUSES]


def main(path):
    population = load_population(path)
    population.sort(key=lambda r: r["API"])      # fixed starting order before shuffling
    rng = random.Random(SEED)
    rng.shuffle(population)

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writeheader()
        for order, r in enumerate(population, start=1):
            row = {k: r[k] for k in KEEP}
            row.update(Order=order, API10=r["API"][:10],
                       Role="Primary" if order <= PRIMARY_N else "Replacement")
            writer.writerow(row)

    print(f"Population (Active + Idle, distinct API): {len(population):,}")
    print(f"Seed: {SEED}   Primary: rows 1-{PRIMARY_N}   Replacements: rows {PRIMARY_N + 1}-{len(population):,}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
