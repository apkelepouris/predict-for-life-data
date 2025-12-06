import csv, json, datetime

INPUT_CSV = "set_for_life.csv"
OUTPUT_JSON = "set_for_life_history.json"
VERSION = 20251127  # <-- bump this whenever you regenerate

rows = []

with open(INPUT_CSV, newline="", encoding="utf-8") as f:
  reader = csv.DictReader(f)
  for row in reader:
    # adjust format if your date is different
    date = datetime.datetime.strptime(row["Date"], "%d/%m/%Y").date()
    main = [
      int(row["N1"]),
      int(row["N2"]),
      int(row["N3"]),
      int(row["N4"]),
      int(row["N5"]),
    ]
    life = int(row["Life"])
    rows.append({
      "date": date.isoformat(),
      "mainBalls": main,
      "lifeBall": life,
    })

data = {
  "version": VERSION,
  "draws": rows,
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
  json.dump(data, f, indent=2)

print("Wrote", OUTPUT_JSON, "with", len(rows), "draws.")
