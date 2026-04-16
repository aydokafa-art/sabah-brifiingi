from datetime import datetime, timezone, timedelta

_TRT = timezone(timedelta(hours=3))  # Turkey Time (UTC+3)

_DAYS = {
    "Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
    "Thursday": "Perşembe", "Friday": "Cuma",
    "Saturday": "Cumartesi", "Sunday": "Pazar",
}
_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
}


def get_today_date() -> str:
    now = datetime.now(_TRT)
    day = _DAYS.get(now.strftime("%A"), now.strftime("%A"))
    return f"{day}, {now.day} {_MONTHS[now.month]} {now.year}"


def _build_tasks_section(tasks: dict) -> str:
    if not tasks:
        return ""

    tur_renk = {
        "Günlük":  ("#eff6ff", "#1d4ed8", "📅"),
        "Haftalık": ("#f0fdf4", "#15803d", "📆"),
        "Aylık":   ("#faf5ff", "#7e22ce", "🗓️"),
    }

    rows = ""
    for tur in ["Günlük", "Haftalık", "Aylık"]:
        gorevler = tasks.get(tur)
        if not gorevler:
            continue
        bg, color, icon = tur_renk.get(tur, ("#f8fafc", "#334155", "•"))
        items = "".join(
            f'<li style="margin-bottom:6px;color:#374151;">{g}</li>'
            for g in gorevler
        )
        rows += f"""
        <tr>
          <td style="padding:0 0 14px;">
            <div style="background:{bg};border-radius:8px;padding:14px 18px;">
              <p style="margin:0 0 8px;color:{color};font-size:11px;
                        font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">
                {icon} {tur}
              </p>
              <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6;">
                {items}
              </ul>
            </div>
          </td>
        </tr>"""

    if not rows:
        return ""

    return f"""
        <!-- ── Görevler ─────────────────────────────────────────────── -->
        <tr>
          <td style="padding:24px 32px 0;border-top:1px solid #f1f5f9;">
            <p style="margin:0 0 16px;color:#94a3b8;font-size:10px;
                      letter-spacing:2px;text-transform:uppercase;">
              Yapılacaklar
            </p>
            <table width="100%" cellpadding="0" cellspacing="0">
              {rows}
            </table>
          </td>
        </tr>"""


def build_email_html(motivation: str, news: list, weather: dict, tasks: dict | None = None) -> str:
    date_str = get_today_date()

    # Haber satırları
    news_rows = ""
    for item in news:
        if item["link"]:
            title_html = (
                f'<a href="{item["link"]}" '
                f'style="color:#1d4ed8;text-decoration:none;font-weight:500;">'
                f'{item["title"]}</a>'
            )
        else:
            title_html = f'<span style="font-weight:500;">{item["title"]}</span>'

        source_html = (
            f'<span style="color:#9ca3af;font-size:12px;"> — {item["source"]}</span>'
            if item["source"]
            else ""
        )

        news_rows += f"""
        <li style="margin-bottom:11px;line-height:1.55;color:#374151;">
            {title_html}{source_html}
        </li>"""

    # Hava durumu detay satırı
    weather_detail = (
        f"Hissedilen {weather['feels_like']}°C"
        f" &nbsp;·&nbsp; Nem %{weather['humidity']}"
        f" &nbsp;·&nbsp; Rüzgar {weather['wind_speed']} km/s"
    )

    tasks_html = _build_tasks_section(tasks or {})

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Sabah Briefing</title>
</head>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:Arial,'Helvetica Neue',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9;padding:36px 0;">
    <tr><td align="center">
      <table width="580" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:10px;overflow:hidden;
                    box-shadow:0 4px 14px rgba(0,0,0,0.08);max-width:580px;">

        <!-- ── Başlık ─────────────────────────────────────────────────── -->
        <tr>
          <td style="background:#0f172a;padding:28px 32px 24px;">
            <p style="margin:0;color:#64748b;font-size:11px;letter-spacing:2px;
                      text-transform:uppercase;">Sabah Briefing</p>
            <h1 style="margin:8px 0 0;color:#f8fafc;font-size:20px;
                       font-weight:600;letter-spacing:-0.3px;">{date_str}</h1>
          </td>
        </tr>

        <!-- ── Motivasyon ─────────────────────────────────────────────── -->
        <tr>
          <td style="background:#1e293b;padding:22px 32px 24px;">
            <p style="margin:0 0 10px;color:#475569;font-size:10px;
                      letter-spacing:2px;text-transform:uppercase;">Günün Sesi</p>
            <p style="margin:0;color:#e2e8f0;font-size:16px;font-style:italic;
                      line-height:1.65;">&ldquo;{motivation}&rdquo;</p>
          </td>
        </tr>

        <!-- ── Hava Durumu ─────────────────────────────────────────────── -->
        <tr>
          <td style="padding:24px 32px 22px;border-bottom:1px solid #f1f5f9;">
            <p style="margin:0 0 14px;color:#94a3b8;font-size:10px;
                      letter-spacing:2px;text-transform:uppercase;">
              Hava Durumu &mdash; {weather['city']}
            </p>
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="font-size:40px;font-weight:700;color:#0f172a;
                           line-height:1;padding-right:18px;">{weather['temp']}°C</td>
                <td style="vertical-align:middle;">
                  <p style="margin:0;color:#1e293b;font-size:15px;">
                    {weather['description']}
                  </p>
                  <p style="margin:5px 0 0;color:#94a3b8;font-size:12px;">
                    {weather_detail}
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── Haberler ──────────────────────────────────────────────── -->
        <tr>
          <td style="padding:24px 32px 22px;border-bottom:1px solid #f1f5f9;">
            <p style="margin:0 0 16px;color:#94a3b8;font-size:10px;
                      letter-spacing:2px;text-transform:uppercase;">
              Ekonomi &amp; Piyasalar
            </p>
            <ul style="margin:0;padding-left:18px;font-size:14px;">
              {news_rows}
            </ul>
          </td>
        </tr>

        {tasks_html}

        <!-- ── Footer ────────────────────────────────────────────────── -->
        <tr>
          <td style="padding:18px 32px;background:#f8fafc;">
            <p style="margin:0;color:#94a3b8;font-size:12px;text-align:center;">
              Günü kazan. &nbsp;&mdash;&nbsp; Sabah Briefing
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""
