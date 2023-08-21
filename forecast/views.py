from django.shortcuts import render
import requests
# Create your views here.
import requests 
from bs4 import BeautifulSoup


def index(request):
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

    waveheight = []
    wind = {}
    temp = []
    graphwave = []


    all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wave-height__cell"})
    for i in all:
        waveheight.append(i.find("text", {"class":"swell-icon__val"}).text)

    all = soup.find_all("td", {"class":"forecast-table__cell forecast-table-wind__cell"})
    for i in all:
        wind[i.find("text", {"class":"wind-icon__val"}).text] = i.find("div", {"class":"wind-icon__letters"}).text

    all = soup.find_all("tr", {"class":"forecast-table__row"})
    tds = all[19].find_all("td")
    for i in tds:
        temp.append(i.find("span").text)

    all = soup.find_all("svg", {"class":"forecast-table-wave-graph__wave"})
    for i in all:
        graphwave.append(i)

    weather = {
        "temp": temp,
        "wind": wind,
        "wave height": waveheight,
        "graph wave": graphwave
    }

    context = {"weather" : weather}
    return render(request, "forecast.html", context)

