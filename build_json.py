import csv
import json
import datetime
import os

INPUT_CSV = "set_for_life.csv"
OUTPUT_JSON = "set_for_life_history.json"


def load_existing():
    """
    Load the existing JSON file (if any).
    Returns a dict or None.
    """
    if not os.path.exists(OUTPUT_JSON):
        return None

    try:
        with open(OUTPUT_JSON, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If the file is corrupt or unreadable, treat as if it doesn't exist
        return None


def build_rows_from_csv():
    """
    Read the CSV and build the list of draw dicts.
    """
    rows = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Adjust date format here if your CSV changes
            date = datetime.datetime.strptime(row["Date"], "%d/%m/%Y").date()
            main_balls = [
                int(row["N1"]),
                int(row["N2"]),
                int(row["N3"]),
                int(row["N4"]),
                int(row["N5"]),
            ]
            life = int(row["Life"])
            rows.append(
                {
                    "date": date.isoformat(),
                    "mainBalls": main_balls,
                    "lifeBall": life,
                }
            )
    return rows


def main():
    # 1) Build new draws list from the CSV
    new_rows = build_rows_from_csv()

    # 2) Load existing JSON (if it exists)
    existing = load_existing()
    if existing is not None:
        old_rows = existing.get("draws", [])
        old_version = int(existing.get("version", 0))
    else:
        old_rows = None
        old_version = 0

    # 3) Decide whether anything actually changed
    if old_rows == new_rows and old_version != 0:
        # No change in data; keep the same version and do NOT rewrite the JSON
        print(
            f"No changes detected in draws. "
            f"Keeping existing version {old_version} with {len(new_rows)} draws."
        )
        return

    # 4) Data changed (or first run) – bump version by 1
    new_version = old_version + 1

    data = {
        "version": new_version,
        "draws": new_rows,
    }

    # 5) Write JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(
        f"Wrote {OUTPUT_JSON} with {len(new_rows)} draws. "
        f"Version: {new_version} (was {old_version})"
    )


if __name__ == "__main__":
    main()
