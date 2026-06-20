"""
Vat Arabische tekst samen met een lokaal LLM via Ollama.
"""
import ollama
from app.config import settings

SUMMARY_PROMPT = """أنت مساعد متخصص في تلخيص النصوص العربية.
اقرأ النص التالي واكتب:
1. ملخص موجز في 3-5 جمل.
2. قائمة من 3 إلى 6 نقاط رئيسية (key points).

أجب فقط بصيغة JSON بهذا الشكل بالضبط، بدون أي نص إضافي قبله أو بعده:
{{"summary": "...", "key_points": ["...", "..."]}}

النص:
{text}
"""


def summarize_text(text: str) -> dict:
    """
    Stuurt de tekst naar het lokale Ollama model en parsed het
    JSON-antwoord met summary en key_points.
    """
    client = ollama.Client(host=settings.ollama_host)

    response = client.chat(
        model=settings.ollama_model,
        messages=[{
            "role": "user",
            "content": SUMMARY_PROMPT.format(text=text),
        }],
        format="json",
    )

    content = response["message"]["content"]

    import json
    try:
        parsed = json.loads(content)
        return {
            "summary": parsed.get("summary", ""),
            "key_points": parsed.get("key_points", []),
        }
    except json.JSONDecodeError:
        # Fallback: als het model geen geldige JSON teruggeeft,
        # geven we de ruwe tekst terug als summary.
        return {"summary": content, "key_points": []}
