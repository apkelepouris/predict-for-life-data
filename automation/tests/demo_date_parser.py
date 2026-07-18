from automation.utils.date_parser import parse_uk_date

tests = [
    "Thursday 16th July 2026",
    "Monday 1st March 2027",
    "Tuesday 2nd June 2026",
    "Wednesday 3rd April 2026",
    "Friday 21st August 2026",
]

for text in tests:
    print(text)
    print(parse_uk_date(text))
    print()