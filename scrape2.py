import requests 
from bs4 import BeautifulSoup

r = requests.get("https://www.surf-forecast.com/breaks/Meia-Praia/forecasts/latest/six_day")
c = r.content
soup = BeautifulSoup(c, "html.parser")


###
# things to scrape:
# wave height DONE
# colors DONE
# wind direction and km/h DONE
# temp DONE
###

wave_height = []
wind_vel = []
wind_dir = []
temp = []
colors = []


all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wave-height__cell"})
for i in all:
    wave_height.append(i.find("text", {"class":"swell-icon__val"}).text)

all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wind__cell"})
for i in all:
    wind_vel.append(i.find("text", {"class":"wind-icon__val"}).text)
    wind_dir.append(i.find("div", {"class":"wind-icon__letters"}).text)

all = soup.find_all("tr", {"class":"forecast-table__row"})
tds = all[19].find_all("td", limit=24)
for i in tds:
    temp.append(i.find("span").text)

for td in soup.find_all("svg", {"class":"swell-icon__svg"}, limit=24):
    if "fill" in td.attrs:
        colors.append(td["fill"])

