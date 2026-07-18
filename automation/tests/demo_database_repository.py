from automation.database.database_repository import (
    DatabaseRepository,
)

repository = DatabaseRepository(
    "set_for_life.csv",
)

draw = repository.latest_draw()

print(draw)