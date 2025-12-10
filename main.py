from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = FastAPI()

client = OpenAI(api_key="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")

class StoryRequest(BaseModel):
    prompt: str

KOSI_SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald, blând și empatic, creat pentru copii. "
    "Răspunzi scurt, cald, jucăuș și prietenos. "
    "Eviți cuvintele grele. "
)

@app.post("/story")
async def story(request: StoryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Invalid prompt")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": KOSI_SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt},
            ]
        )

        # ACCES CORECT pentru noile modele OpenAI
        story_text = completion.choices[0].message.content

        return {"story": story_text}

    except Exception as e:
        return {"story": f"Kosi are o mică problemă acum: {str(e)}"}
