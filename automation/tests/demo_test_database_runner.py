"""
Run the automation against the test database.
"""

from automation.core.automation_runner import (
    AutomationRunner,
)

runner = AutomationRunner(
    database_path="automation/tests/data/test_database.csv",
)

result = runner.run()

print(result)