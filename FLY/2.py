import requests
from bs4 import BeautifulSoup
import csv

url = 'https://flightaware.com/live/flight/ANZ288/history/20230616/0625Z/ZSPD/NZAA/tracklog'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

rows = soup.find('tr', attrs={'class': 'thirdHeader'})
with open("2.csv", mode="w",encoding="utf-8") as file:
    writer = csv.writer(file)
    cols = rows.find_all('th')
    cols = [col.text.strip() for col in cols]
    # Write the row to CSV file
    writer.writerow(cols)

table = soup.find('table', attrs={'class': 'prettyTable fullWidth'})
rows = table.find_all('tr')

with open("2.csv", mode="a+", encoding="utf-8") as file:
    writer = csv.writer(file)

    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]

        # Write the row to CSV file
        writer.writerow(cols)

print("Data saved to 2.csv")