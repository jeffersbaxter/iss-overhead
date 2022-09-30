import time

import requests
import datetime as dt
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email = os.environ.get("SECRET_EMAIL")
password = os.environ.get("SECRET_PASSWORD")

MY_LAT = 47.606209
MY_LONG = -122.332069

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


def within_latitude():
    return MY_LAT - 5.0 <= iss_latitude <= MY_LAT + 5.0


def within_longitude():
    return MY_LONG - 5.0 <= iss_longitude <= MY_LONG + 5.0


def is_overhead():
    return within_longitude() and within_latitude()


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now()
    hr = time_now
    return hr <= sunrise or hr >= sunset


while True:
    time.sleep(60)
    if is_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(user=email, password=password)
            server.sendmail(
                from_addr=email,
                to_addrs=email,
                msg="Subject:Look Up \n\nThe ISS is above you in the sky."
            )

# BONUS: run the code every 60 seconds.



