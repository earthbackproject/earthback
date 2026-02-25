#!/usr/bin/env python3
"""
generate-hotspots-sql.py
Reads hotspots-seed.csv and generates SQL INSERT statements for the
map_hotspots table. Run this after SCHEMA_V8_map.sql has been applied.

Usage:
    python generate-hotspots-sql.py              # writes hotspots-seed.sql
    python generate-hotspots-sql.py --preview    # print to terminal only
    python generate-hotspots-sql.py --skip-global  # skip entries with lat=0,lng=0
"""

import csv
import sys
import argparse
from pathlib import Path

INPUT  = Path(__file__).parent / "hotspots-seed.csv"
OUTPUT = Path(__file__).parent / "hotspots-seed.sql"

def escape(val):
    if val is None or val == "":
        return "NULL"
    return "'" + str(val).replace("'", "''") + "'"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview",      action="store_true")
    parser.add_argument("--skip-global",  action="store_true",
                        help="Skip entries with lat=0, lng=0 (global/no-pin entries)")
    args = parser.parse_args()

    rows = []
    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat = float(row["lat"])
            lng = float(row["lng"])
            if args.skip_global and lat == 0 and lng == 0:
                print(f"  [skip global] {row['title']}")
                continue
            rows.append(row)

    lines = [
        "-- Earthback map_hotspots seed data",
        "-- Generated from hotspots-seed.csv",
        "-- Run AFTER SCHEMA_V8_map.sql",
        "",
        "INSERT INTO public.map_hotspots",
        "  (latitude, longitude, location_name, category, title,",
        "   description, url, circle_slug, status, priority, is_visible)",
        "VALUES",
    ]

    value_rows = []
    for row in rows:
        lat  = float(row["lat"])
        lng  = float(row["lng"])
        vals = (
            f"  ({lat}, {lng}, "
            f"{escape(row['location_name'])}, "
            f"{escape(row['category'])}, "
            f"{escape(row['title'])}, "
            f"{escape(row['description'])}, "
            f"{escape(row['url'])}, "
            f"{escape(row['circle_slug'])}, "
            f"{escape(row.get('status','active'))}, "
            f"{int(row.get('priority', 1))}, "
            f"true)"
        )
        value_rows.append(vals)

    lines.append(",\n".join(value_rows) + ";")
    lines.append("")
    lines.append(f"-- {len(rows)} hotspots inserted")

    sql = "\n".join(lines)

    if args.preview:
        print(sql[:3000])
        print(f"\n... ({len(rows)} rows total)")
        return

    OUTPUT.write_text(sql, encoding="utf-8")
    print(f"Written: {OUTPUT}")
    print(f"Rows: {len(rows)}")
    print(f"\nNext: run hotspots-seed.sql in Supabase SQL Editor")

if __name__ == "__main__":
    main()
