# Arabic Content Analyzer

Een tool die Arabische YouTube-video's automatisch transcribeert en samenvat.
Geef een YouTube-link op, en de tool downloadt de audio, transcribeert deze
naar Arabische tekst (via Whisper) en genereert een samenvatting met
belangrijkste punten (via een lokaal LLM met Ollama).

## Waarom dit project?

Arabische NLP-tools zijn schaars vergeleken met Engelstalige tools. Dit project
combineert speech-to-text en samenvatting specifiek geoptimaliseerd voor
Arabische content (podcasts, lezingen, interviews, nieuws).

## Architectuur

```
YouTube URL --> yt-dlp (audio download) --> faster-whisper (transcriptie)
            --> Ollama / lokaal LLM (samenvatting) --> JSON resultaat
```

De verwerking draait asynchroon: je krijgt direct een `job_id` terug en kunt
de status pollen totdat de job klaar is.

## Vereisten

- Python 3.10+
- [Ollama](https://ollama.com) geinstalleerd en draaiend
- ffmpeg geinstalleerd (nodig voor audio-extractie door yt-dlp)

## Installatie

```bash
# 1. Virtuele omgeving aanmaken
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Dependencies installeren
pip install -r requirements.txt

# 3. Ollama model downloaden
ollama pull qwen2.5:7b

# 4. .env aanmaken (optioneel, anders worden defaults gebruikt)
cp .env.example .env
```

## Starten

```bash
uvicorn app.main:app --reload
```

De API draait nu op `http://localhost:8000`. Interactieve documentatie (Swagger)
is te vinden op `http://localhost:8000/docs`.

## Gebruik

### 1. Start een analyse

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

Antwoord:
```json
{"job_id": "abc-123", "status": "pending"}
```

### 2. Status checken

```bash
curl http://localhost:8000/status/abc-123
```

### 3. Resultaat ophalen (zodra status "done" is)

```bash
curl http://localhost:8000/result/abc-123
```

Antwoord:
```json
{
  "job_id": "abc-123",
  "status": "done",
  "video_title": "...",
  "transcript": "...",
  "summary": "...",
  "key_points": ["...", "..."]
}
```

## Roadmap

- [ ] Sentiment-analyse van reacties/transcript
- [ ] Ondersteuning voor meerdere Arabische dialecten
- [ ] Web-interface (React of Streamlit)
- [ ] Persistente opslag (database i.p.v. in-memory)
- [ ] Ondersteuning voor lokale audiobestanden naast YouTube-links
- [ ] Timestamps koppelen aan key points

## Licentie

MIT
