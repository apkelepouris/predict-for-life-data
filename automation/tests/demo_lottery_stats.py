from automation.sources.lottery_stats import LotteryStatsSource

source = LotteryStatsSource()

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