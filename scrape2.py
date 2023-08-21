import requests 
from bs4 import BeautifulSoup

r = requests.get("https://www.surf-forecast.com/breaks/Meia-Praia/forecasts/latest/six_day")
c = r.content
soup = BeautifulSoup(c, "html.parser")


###
# things to scrape:
# wave height DONE
# wave graph DONE
# wind direction and km/h DONE
# temp DONE
###

wave_height = []
wind = {}
temp = []
graph_wave = []


all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wave-height__cell"})
for i in all:
    wave_height.append(i.find("text", {"class":"swell-icon__val"}).text)

all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wind__cell"})
for i in all:
    wind[i.find("text", {"class":"wind-icon__val"}).text] = i.find("div", {"class":"wind-icon__letters"}).text

all = soup.find_all("tr", {"class":"forecast-table__row"})
tds = all[19].find_all("td")
for i in tds:
    temp.append(i.find("span").text)

all = soup.find_all("svg", {"class":"forecast-table-wave-graph__wave"})
for i in all:
    graph_wave.append(i)