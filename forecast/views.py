import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.shortcuts import render

def surf_breaks(request):
    url = "https://www.surf-forecast.com/countries/Portugal/breaks"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # Extract the list of surf breaks organized by category
    surf_breaks = {}
    tbody = soup.find("table")
    current_category = None
    if tbody:
        for link in tbody.find_all("a"):
            parent_h2 = link.find_parent("h2")
            if parent_h2:
                current_category = link.text.strip()
                surf_breaks[current_category] = []
            elif current_category:
                surf_breaks[current_category].append({
                    "name": link.text.strip(),
                    "url": link["href"]
                })
    
    context = {
        "surf_breaks": surf_breaks
    }
    
    return render(request, "surf_breaks.html", context)

def index(request, break_name="Meia-Praia"):
    break_name = break_name.replace(" ", "-")
    url = f"https://www.surf-forecast.com/breaks/{break_name}/forecasts/latest/six_day"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # Extract the entire forecast table
    forecast_table = soup.find("table", class_="js-forecast-table-content forecast-table__table forecast-table__table--content")
    
    # Remove all buttons from the table
    if forecast_table:
        for button in forecast_table.find_all("button"):
            button.decompose()
    
    # Remove images that come from a file (keep URL-based ones)
    if forecast_table:
        for img in forecast_table.find_all("img"):
            if not img.get("src", "").startswith("http"):
                img.decompose()
    
    # Remove wave graph row
    if forecast_table:
        for wave_graph in forecast_table.find_all("tr", class_="forecast-table__row", attrs={"data-row-name": "wave-graph"}):
            wave_graph.decompose()
    
    # Remove energy row
    if forecast_table:
        for energy_row in forecast_table.find_all("tr", class_="forecast-table__row", attrs={"data-row-name": "energy"}):
            energy_row.decompose()
    
    # Remove all hyperlinks except those inside images
    if forecast_table:
        for link in forecast_table.find_all("a"):
            if not link.find("img"):
                link.decompose()
    
    # Remove specific rows inside tfoot
    if forecast_table:
        tfoot = forecast_table.find("tfoot")
        if tfoot:
            for days_row in tfoot.find_all("tr", class_="forecast-table__row forecast-table-days not_in_print forecast-table__bottom-table-row", attrs={"data-row-name": "days"}):
                days_row.decompose()
            for weather_summary in tfoot.find_all("tr", class_="forecast-table__row forecast-table-weather-summary", attrs={"data-row-name": "weather-summary"}):
                weather_summary.decompose()
    
    # Remove star rating SVGs
    if forecast_table:
        for star_svg in forecast_table.find_all("svg", class_="star-rating__star"):
            star_svg.decompose()
    
    table_html = f'{str(forecast_table)}' if forecast_table else "<p>No forecast data available.</p>"
    
    # Fetch the surf breaks for the sidebar
    surf_breaks_url = "https://www.surf-forecast.com/countries/Portugal/breaks"
    r_breaks = requests.get(surf_breaks_url)
    soup_breaks = BeautifulSoup(r_breaks.content, "html.parser")
    
    surf_breaks = {}
    tbody = soup_breaks.find("table")
    current_category = None
    if tbody:
        for link in tbody.find_all("a"):
            parent_h2 = link.find_parent("h2")
            if parent_h2:
                current_category = link.text.strip()
                surf_breaks[current_category] = []
            elif current_category:
                surf_breaks[current_category].append({
                    "name": link.text.strip(),
                    "url": link["href"]
                })
    
    context = {
        "forecast_table": table_html,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "break_name": break_name,
        "surf_breaks": surf_breaks
    }
    
    return render(request, "forecast.html", context)