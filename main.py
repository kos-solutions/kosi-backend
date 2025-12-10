from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import base64
import uvicorn

app = FastAPI()

# IMPORTANT: cheia trebuie pusă în Railway → Variables
client = OpenAI(api_key="YOUR_OPENAI_KEY_HERE")


# ------------------ REQUEST MODELS ------------------

class StoryRequest(BaseModel):
    prompt: str

class TTSRequest(BaseModel):
    text: str


# ------------------ KOSI PROMPT ------------------

KOSI_SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald, blând și empatic, creat special pentru copii. "
    "Vorbesti cu o voce jucăușă și liniștitoare. "
    "Folosești propoziții scurte și simple. "
    "Nu folosești ton robotic sau cuvinte complicate. "
    "Nu moralizezi, nu dai ordine și nu sperii copilul. "
    "Oferi siguranță, încurajare și căldură. "
    "Răspunsurile tale trebuie să sune afectuos și pline de prietenie. "
)


# ------------------ STORY ENDPOINT ------------------

@app.post("/story")
async def story(request: StoryRequest):

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt invalid")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": KOSI_SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.75,
            max_tokens=500
        )

        story_text = completion.choices[0].message["content"]
        return {"story": story_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ TTS ENDPOINT ------------------

@app.post("/tts")
async def tts(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text invalid pentru TTS")

    try:
        # OpenAI TTS – model: gpt-4o-mini-tts (rapid, cald)
        audio_resp = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="verse",
            input=request.text
        )

        # Convertire în Base64 pentru Android
        audio_base64 = base64.b64encode(audio_resp).decode("utf-8")

        return {"audio": audio_base64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ------------------ SERVER START ------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
