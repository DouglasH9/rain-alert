import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
ACCT_SID = os.environ.get("ACCT_SID")
AUTH_TKN = os.environ.get("AUTH_TKN")
client = Client(ACCT_SID, AUTH_TKN, http_client=proxy_client)

LON = -87.65
LAT = 41.85
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

parameters = {
    "lat": LAT,
    "lon": LON,
    "appid": WEATHER_API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall?", params=parameters)
response.raise_for_status()
data = response.json()
sliced_data = data["hourly"][:12]

# for i in range(12):
#     if data["hourly"][i]["weather"][0]["id"] < 700:
#         print("Bring an umbrella!")
#     else:
#         print("Not gonna rain anytime soon.")
will_rain = False
for hour_data in sliced_data:
    condition_id = hour_data["weather"][0]["id"]
    if int(condition_id) < 700:
        will_rain = True

if will_rain:
    message = client.messages \
        .create(
        body="It's gonna rain! Bring an umbrella!",
        from_='+18065459159',
        to='+17733703689'
    )
    print(message.status)
else:
    message = client.messages \
        .create(
        body="Gonna be a lovely day!",
        from_='+18065459159',
        to='+17733703689'
    )
    print(message.status)
