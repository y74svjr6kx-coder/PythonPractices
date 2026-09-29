from datetime import datetime, timedelta


# 1
today = datetime.now()
five_days_ago = today - timedelta(days=5)

print(five_days_ago)


# 2
today = datetime.now()

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3
now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print(without_microseconds)


# 4
date1 = datetime(2026, 9, 20, 10, 0, 0)
date2 = datetime(2026, 9, 20, 12, 0, 0)

difference = date2 - date1

print(difference.total_seconds())
