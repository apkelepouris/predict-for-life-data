from automation.sources.national_lottery_com import NationalLotteryComSource

source = NationalLotteryComSource()

result = source.fetch()

print(result)

if result.success:
    print()
    print("Latest draw:")
    print(result.draw)
else:
    print()
    print("Error:")
    print(result.error_message)