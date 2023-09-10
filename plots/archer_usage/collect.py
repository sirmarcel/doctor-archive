import requests

months = [(2021, 12)]
for month in range(1, 12):
    months.append((2022, month))

for year, month in months:
    with open(f"{year}-{month:02d}.csv", "w") as f:
        if year == 2022 and month >= 10:
            result = requests.get(f"https://raw.githubusercontent.com/ARCHER2-HPC/usage-data/main/allusers/{year}/{month:02d}/{year}-{month:02d}_CodeSize_weighted.csv")
        else:
            result = requests.get(f"https://raw.githubusercontent.com/ARCHER2-HPC/usage-data/main/allusers/{year}/{month:02d}/{year}-{month:02d}_stats_by_usage.csv")
        assert result.status_code == 200
        data = str(result.content, "utf-8")
        f.write(data)
