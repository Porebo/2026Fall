"""Reproduce the random selection of Ventura field wells for the wellbore diagram sample.

Usage (from any folder; the CSV path defaults to ../05-data/calgem/):
    python select_ventura_wells.py [path/to/2021CaliforniaOilAndGasWells.csv]

Prints the first draw (seed 20261110) and the ordered replacement candidates
(seed 20261111), as recorded in PROVENANCE.md, section 7.1.
Requires only the Python standard library.
"""
import csv
import random
import sys
from pathlib import Path

FIRST_SEED = 20261110
REPLACEMENT_SEED = 20261111
CANDIDATES_PER_STRATUM = 12


def load_ventura_wells(path):
    """One row per API number (first occurrence in file order), Ventura field only."""
    wells = {}
    with open(path, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["FieldName"].strip().lower() == "ventura" and row["API"] not in wells:
                wells[row["API"]] = row
    return list(wells.values())


def is_active_og(r):
    return r["WellStatus"] == "Active" and r["WellTypeCode"] == "OG"


def is_active_wf(r):
    return r["WellStatus"] == "Active" and r["WellTypeCode"] == "WF"


def is_idle(r):
    return r["WellStatus"] == "Idle"


def is_plugged(r):
    return r["WellStatus"] == "Plugged"


STRATA = [
    ("Active OG", is_active_og, 4),
    ("Active WF", is_active_wf, 2),
    ("Idle", is_idle, 2),
    ("Plugged", is_plugged, 2),
]


def show(row, label):
    print(f"  {label:10} API10={row['API'][:10]}  API12={row['API']}  "
          f"{row['LeaseName']} {row['WellNumber']}  ({row['WellStatus']}, {row['WellTypeCode']})")


def main(path):
    wells = load_ventura_wells(path)
    print(f"Ventura field wells (distinct API): {len(wells)}\n")

    random.seed(FIRST_SEED)
    first = []
    for _, test, n in STRATA:
        first += random.sample([r for r in wells if test(r)], n)
    print(f"First draw (seed {FIRST_SEED}):")
    for r in first:
        show(r, "")
    picked = {r["API"] for r in first}

    random.seed(REPLACEMENT_SEED)
    print(f"\nReplacement candidates, in the order checked (seed {REPLACEMENT_SEED}):")
    for name, test, _ in STRATA:
        pool = [r for r in wells if test(r) and r["API"] not in picked]
        random.shuffle(pool)
        print(f" {name}:")
        for r in pool[:CANDIDATES_PER_STRATUM]:
            show(r, "")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "05-data" / "calgem" / "2021CaliforniaOilAndGasWells.csv")
