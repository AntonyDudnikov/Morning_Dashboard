"""
Created by: Antony Dudnikov
Project start date: April 15, 2020
Project Finish date: May 20, 2020

Idea:
Learn how to use API's and to extract TTC data. Goal is to isolate the time
and the bus that is heading North and/or the streetcar towards the city center.

"""

import requests
import json

def retrieve_market_data()-> dict:
    url = 'https://financialmodelingprep.com/api/v3/quote/%5EDJI'
    response = requests.get(url=url).json()
    url2 = 'https://financialmodelingprep.com/api/v3/quote/%5EGSPTSE'
    response2 = requests.get(url=url2).json()
    url3 = 'https://financialmodelingprep.com/api/v3/quote/USDCAD'
    response3 = requests.get(url= url3).json()
    market = {}
    market["Dow"]={'price': str(response[0]["price"]), "change": str(response[0]["change"]), "%change": str(response[0]["changesPercentage"])}
    market["TSX"]={'price':str(response2[0]["price"]), "change": str(response2[0]["change"]), "%change": str(response2[0]["changesPercentage"])}
    market["Dollar"] = {"exchange": str(response3[0]["price"]), "change": str(response3[0]["change"])}
    return market


def retrieve_data_N()-> dict:
    """Retrieves data from the API and extracts the data into a
    Northbound/Southbound dictionary with a list of all times
    """
    response = requests.get("https://myttc.ca/dufferin_and_liberty.json").json() #gets the data and turns it into a json tree
    bus_time = {"Northbound_Liberty":[]}
    for i in range(len(response["stops"][0]["routes"])): #append the times into the Northbound key
        for x in range(len(response["stops"][0]["routes"][i]["stop_times"])):
            bus_time["Northbound_Liberty"].append(response["stops"][0]["routes"][i]["stop_times"][x]["departure_time"])
    return bus_time

def retrieve_data_E() -> dict:
    response = requests.get("https://myttc.ca/dufferin_and_king.json").json()
    tram_time = {"Eastbound":[]}
    for i in range(len(response["stops"][0]["routes"])):
        for x in range(len(response["stops"][0]["routes"][i]["stop_times"])):
            tram_time["Eastbound"].append(response["stops"][0]["routes"][i]["stop_times"][x]["departure_time"])
    return tram_time

def retrieve_current() -> dict:
    url = 'https://api.climacell.co/v3/weather/realtime'
    querystring = {'fields': ['temp','feels_like', 'sunset', 'weather_code', 'wind_speed'],"unit_system":"si", "apikey":"XSs9JooJQ1vKLqUjycVrGrNd9dhxWi4t", "lat":"43.651070","lon":"-79.347015"}
    response = requests.request("GET", url, params=querystring).json()
    return response


def retrieve_hourly() -> dict:
    url = 'https://api.climacell.co/v3/weather/forecast/hourly'
    querystring = {'fields': ['temp', 'feels_like', 'weather_code'],"unit_system":"si","start_time":"now","apikey":"XSs9JooJQ1vKLqUjycVrGrNd9dhxWi4t", "lat":"43.651070","lon":"-79.347015"}
    response = requests.request("GET", url, params=querystring).json()
    print(json.dumps(response, indent=4))
    hourly = []
    for i in range(8):
        y = (int(response[i+1]["observation_time"]["value"][11:13])-4)
        x = 'pm' if y >=12 or y<0 else 'am'
        time = y%12
        if time == 0:
            time = 12
        value = response[i+1]["temp"]["value"]
        hourly.append([str(time) + ' {}'.format(x), value, response[i+1]['weather_code']['value']])
    return hourly

def retrieve_daily() -> dict:
    url = 'https://api.climacell.co/v3/weather/forecast/daily'
    querystring = {'fields': 'temp',"unit_system":"si","start_time":"now","apikey":"XSs9JooJQ1vKLqUjycVrGrNd9dhxWi4t", "lat":"43.651070","lon":"-79.347015"}
    response = requests.request("GET", url, params=querystring).json()
    daily = {}
    #print(json.dumps(response, indent= 4))
    for i in range(7):
        day = response[i]["observation_time"]["value"]
        value = {"min": response[i]["temp"][0]["min"]["value"], "max":response[i]["temp"][1]["max"]["value"]}
        daily[day] = value
    return daily

if __name__ == "__main__":
    while True:
        action = input("what would you like to do?\nGet times\nClose\nHourly Weather\ndaily weather\ncurrent weather\nmarket data\n")

        if action == "get times":
            print(retrieve_data_N())
            print(retrieve_data_E())
            print(retrieve_data_N()['Northbound_Liberty'])
        elif action == 'hourly weather':
            print(retrieve_hourly())
        elif action == 'daily weather':
            print(retrieve_daily())
        elif action == 'current weather':
            print( retrieve_current())
        elif action == 'market data':
            print(retrieve_market_data())
        elif action == "close":
            break
        else:
            print("Please type correctly with all lowercase letters")




