from automation.core.automation_runner import (
    AutomationRunner,
)

runner = AutomationRunner()

result = runner.run()

print()
print("Automation completed")
print("--------------------")
print(f"Result : {result.action.name}")
print(f"Message: {result.message}")

if hasattr(result, "validated_draw") and result.validated_draw:

    print()
    print("Validated draw:")
    print(result.validated_draw)