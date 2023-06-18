from bs4 import BeautifulSoup
from selenium import webdriver
import csv

#配置无头浏览器，并禁用GPU加速和自动化
edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])

#启动浏览器
wd = webdriver.Edge(options=edge_options)

#设置等待时间
wd.implicitly_wait(10)

#打开指定的网页
wd.get('https://flightaware.com/live/flight/ANZ288/history/20230620/0625Z/ZSPD/NZAA')
#获取网页源代码
response_html = wd.page_source
#关闭浏览器
wd.quit()

#解析网页源代码
soup = BeautifulSoup(response_html, 'lxml')

#获取起飞机场代码和目的地机场代码
departure_airport_code = soup.find_all('span', class_='displayFlexElementContainer')[0].text.strip()
destination_airport_code = soup.find_all('span', class_='displayFlexElementContainer')[1].text.strip()

#获取起飞机场名称和目的地机场名称
takeoff_li = soup.find('a', href='/live/airport/ZSPD').text.split()
landing_li = soup.find('a', href='/live/airport/NZAA').text.split()
takeoff = ''
landing = ''
for i in takeoff_li:
    takeoff += i
for j in landing_li:
    landing += j

#获取出发到达时间
departure_time = soup.find('span', class_='flightPageSummaryDepartureDay').text.strip() + soup.find('span', class_='flightPageSummaryDeparture flightTime').text.strip()
arrival_time = soup.find('span', class_='flightPageSummaryArrivalDay').text.strip() + soup.find('span', class_='flightPageSummaryArrival flightTime').text.strip()
total_duration = soup.select('#flightPageTourStep1 > div.flightPageProgressContainer > div.flightPageProgress > span.flightPageProgressTotal > strong')[0].text.strip()

with open('1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Departure Airport Code', 'Destination Airport Code', 'Takeoff', 'Landing', 'Departure Time', 'Arrival Time', 'Total Duration'])
    writer.writerow([departure_airport_code, destination_airport_code, takeoff, landing, departure_time, arrival_time, total_duration])
