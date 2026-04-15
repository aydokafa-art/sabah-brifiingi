import os
import random

# Claude API yoksa veya hata verirse kullanılacak yedek liste
_FALLBACK = [
    "Rakibin şu an uyumadığını düşün — sen ne yapıyorsun?",
    "Bugün acı çekmek istemiyorsan, yarın pişmanlık çekmeye hazır ol.",
    "Yatakta kalan adam hayatını seyretmeye mahkûmdur.",
    "Ortalama olmak için bile emek lazım — sen hangi taraftasın?",
    "Bugün kendini zorlamazsan hayat seni zorlar — seçim senin.",
    "Şu an yapmadıkların, ileride olamamayacakların olacak.",
    "Kimse seni kurtarmayacak. Kalk.",
    "Fırsatlar erken kalkanları bekler, hayal kuranları değil.",
    "Yorgunluk bahanedir — herkes yorgun, kazananlar yine de devam eder.",
    "Bugünden kaçarsan yarın daha ağır gelir.",
    "Hayat sana sormadan geçiyor — sen sormadan geçecek misin?",
    "Konfor alanın mezar alanına dönüşmeden çık.",
]


def get_motivation() -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return random.choice(_FALLBACK)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Türkçe olarak sabah motivasyonu için tek bir cümle yaz. "
                        "Ton: sert, acımasız, yataktan fırlatan cinsten. "
                        "Okuyunca insanın içinde bir şey kırılsın, kalksın. "
                        "Ucuz koç dili değil — gerçek, ham, doğrudan. "
                        "En fazla 15 kelime. Sadece cümleyi yaz, başka hiçbir şey."
                    ),
                }
            ],
        )
        quote = msg.content[0].text.strip().strip('"').strip("'")
        return quote if quote else random.choice(_FALLBACK)
    except Exception as e:
        print(f"Claude API hatası, fallback kullanılıyor: {e}")
        return random.choice(_FALLBACK)
