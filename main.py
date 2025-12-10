from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import base64
import uvicorn
import os

app = FastAPI()

# IMPORTANT: cheia trebuie pusă în Railway → Variables
client = OpenAI(api_key="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")


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
@app.post("/story")
async def story(request: StoryRequest):

    if not request.prompt or request.prompt.strip() == "":
        return {"story": "Nu am înțeles ce ai spus. Vrei să mai zici o dată? 😊"}

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": KOSI_SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )

        story_text = completion.choices[0].message["content"]
        return {"story": story_text}

    except Exception as e:
        # 🔥 IMPORTANT: returnează ÎNTOTDEAUNA story, chiar și la eroare
        return {"story": f"Kosi are o mică problemă acum, dar revine imediat. ({str(e)})"}



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
