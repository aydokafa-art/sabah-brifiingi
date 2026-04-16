import os
import urllib.request
import urllib.error
import json


_DATABASE_ID = "65fa92592fac4ebc92a46e35a3d6afaa"

_TUR_SIRASI = {"Günlük": 0, "Haftalık": 1, "Aylık": 2}


def get_notion_tasks() -> dict:
    """Notion veritabanından aktif görevleri çeker.

    Döndürür:
        {
          "Günlük":  ["görev 1", "görev 2"],
          "Haftalık": [...],
          "Aylık":   [...],
        }
    """
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        return {}

    url = f"https://api.notion.com/v1/databases/{_DATABASE_ID}/query"
    payload = json.dumps({
        "filter": {
            "property": "Aktif",
            "checkbox": {"equals": True}
        },
        "sorts": [{"property": "Tür", "direction": "ascending"}]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        print(f"  Notion yanıtı: {len(data.get('results', []))} kayıt bulundu")
    except urllib.error.HTTPError as e:
        print(f"  Notion API hatası {e.code}: {e.read().decode()}")
        return {}
    except Exception as e:
        print(f"  Notion bağlantı hatası: {e}")
        return {}

    tasks: dict[str, list[str]] = {}
    for page in data.get("results", []):
        props = page.get("properties", {})

        # Görev adı
        title_parts = props.get("Görev", {}).get("title", [])
        name = "".join(p.get("plain_text", "") for p in title_parts).strip()
        if not name:
            continue

        # Tür (Günlük / Haftalık / Aylık)
        tur_sel = props.get("Tür", {}).get("select") or {}
        tur = tur_sel.get("name", "Günlük")

        tasks.setdefault(tur, []).append(name)

    return tasks
