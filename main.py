import os
import sys
from dotenv import load_dotenv

load_dotenv()

from modules.weather import get_weather
from modules.news import get_economy_news
from modules.motivation import get_motivation
from modules.mailer import send_mail
from modules.template import build_email_html, get_today_date


def main():
    print("Sabah briefing hazırlanıyor...")

    motivation = get_motivation()
    print(f"  Motivasyon: OK")

    weather = get_weather()
    print(f"  Hava durumu: {weather['city']} {weather['temp']}°C")

    news = get_economy_news()
    print(f"  Haberler: {len(news)} adet")

    html_body = build_email_html(motivation, news, weather)

    recipient = os.getenv("MAIL_TO")
    if not recipient:
        print("HATA: MAIL_TO tanımlı değil.")
        sys.exit(1)

    send_mail(
        to=recipient,
        subject=f"Günaydın — {get_today_date()}",
        html_body=html_body,
    )

    print("Mail başarıyla gönderildi.")


if __name__ == "__main__":
    main()
