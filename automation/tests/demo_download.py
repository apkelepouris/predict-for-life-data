from automation.sources.national_lottery import NationalLotterySource

source = NationalLotterySource()

result = source.fetch()

print(result)

if result.success:
    print()
    print("Latest draw:")
    print(result.draw)