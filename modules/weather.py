import os
import requests


def get_weather() -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("WEATHER_CITY", "Istanbul")

    if not api_key:
        return _fallback(city, "API anahtarı eksik")

    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
                "lang": "tr",
            },
            timeout=10,
        )
        resp.raise_for_status()
        d = resp.json()

        return {
            "city": city,
            "temp": round(d["main"]["temp"]),
            "feels_like": round(d["main"]["feels_like"]),
            "description": d["weather"][0]["description"].capitalize(),
            "humidity": d["main"]["humidity"],
            "wind_speed": round(d["wind"]["speed"] * 3.6),  # m/s → km/h
        }
    except Exception as e:
        print(f"Hava durumu alınamadı: {e}")
        return _fallback(city, "Veri alınamadı")


def _fallback(city: str, msg: str) -> dict:
    return {
        "city": city,
        "temp": "—",
        "feels_like": "—",
        "description": msg,
        "humidity": "—",
        "wind_speed": "—",
    }
