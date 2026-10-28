"""Load the CalGEM CSV files into calgem.db (SQLite).

Tables:
  wells             - 2021 well list (dimension), one row per well + pool
  water_production  - 2020 quarterly produced water (fact)

Views:
  wells_api         - wells with the API number split into its parts

Codes (API, FieldCode, PoolCode, ...) are stored as TEXT to keep leading zeros.
Rows whose DisposalRecipientName contained an unquoted comma are repaired by
rejoining the split name, and flagged in water_production.load_note.

Usage: python load_calgem.py
"""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "calgem.db"
WELLS_CSV = HERE / "2021CaliforniaOilAndGasWells.xls"
WATER_CSV = HERE / "2020CaliforniaOilAndGasWellQuarterlyProduction.xls"

WATER_NUMERIC = {"WaterProduced"}


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        return header, list(reader)


def load_wells(con):
    header, rows = read_rows(WELLS_CSV)
    bad = [r for r in rows if len(r) != len(header)]
    if bad:
        raise ValueError(f"{len(bad)} well rows have the wrong number of fields")
    cols = ", ".join(f'"{c}" TEXT' for c in header)
    con.execute(f"CREATE TABLE wells ({cols})")
    con.executemany(f"INSERT INTO wells VALUES ({', '.join('?' * len(header))})", rows)
    con.execute('CREATE INDEX ix_wells_key ON wells (API, FieldCode, AreaCode, PoolCode)')
    # API = SS CCC UUUUU XX: state, county code, serial within county, wellbore (00 = original hole)
    con.execute("""
        CREATE VIEW wells_api AS
        SELECT substr(API, 1, 2)  AS state_code,
               substr(API, 3, 3)  AS county_code,
               substr(API, 6, 5)  AS serial,
               substr(API, 11, 2) AS wellbore,
               substr(API, 1, 10) AS surface_well,
               *
        FROM wells""")
    return len(rows)


def load_water(con):
    header, rows = read_rows(WATER_CSV)
    n = len(header)
    name_i = header.index("DisposalRecipientName")  # second-to-last column
    repaired, out = 0, []
    for r in rows:
        note = None
        if len(r) > n:
            # Unquoted comma inside the name: rejoin the pieces, last field is the type code
            r = r[:name_i] + [",".join(r[name_i:-1]), r[-1]]
            note = "repaired: unquoted comma in DisposalRecipientName"
            repaired += 1
        elif len(r) < n:
            raise ValueError(f"short row: {r}")
        out.append(r + [note])

    cols = ", ".join(f'"{c}" {"INTEGER" if c in WATER_NUMERIC else "TEXT"}' for c in header)
    con.execute(f"CREATE TABLE water_production ({cols}, load_note TEXT)")
    con.executemany(
        f"INSERT INTO water_production VALUES ({', '.join('?' * (n + 1))})", out)
    con.execute('CREATE INDEX ix_water_key ON water_production '
                '(APINumber, FieldCode, AreaCode, PoolCode)')
    return len(out), repaired


def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    with con:
        wells = load_wells(con)
        water, repaired = load_water(con)
    con.close()
    print(f"wells: {wells:,} rows")
    print(f"water_production: {water:,} rows ({repaired} repaired)")
    print(f"database: {DB}")


if __name__ == "__main__":
    main()
