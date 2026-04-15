import html
import re
import feedparser

# Türkçe ekonomi haberleri RSS kaynakları
RSS_SOURCES = [
    ("Bloomberg HT",    "https://www.bloomberght.com/rss"),
    ("NTV Ekonomi",     "https://www.ntv.com.tr/ekonomi.rss"),
    ("Haberturk",       "https://www.haberturk.com/rss?category=ekonomi"),
    ("Sabah Ekonomi",   "https://www.sabah.com.tr/rss/ekonomi.xml"),
]

_HTML_TAG = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    """HTML etiketlerini ve encode'ları temizler."""
    if not text:
        return ""
    text = _HTML_TAG.sub("", text)
    text = html.unescape(text)
    return text.strip()


def get_economy_news(max_items: int = 5) -> list[dict]:
    items: list[dict] = []

    for source_name, url in RSS_SOURCES:
        if len(items) >= max_items:
            break
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                if len(items) >= max_items:
                    break
                title = _clean(entry.get("title", ""))
                if not title:
                    continue
                items.append({
                    "title": title,
                    "source": source_name,
                    "link": entry.get("link", ""),
                })
        except Exception as e:
            print(f"{source_name} RSS alınamadı: {e}")

    if not items:
        items = [{"title": "Haberler şu an alınamıyor.", "source": "", "link": ""}]

    return items
