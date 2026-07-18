from pathlib import Path

from automation.core import load_draw_history


draws = load_draw_history(Path("set_for_life.csv"))

print()
print("First draw")
print(draws[0])

print()

print("Latest draw")
print(draws[-1])