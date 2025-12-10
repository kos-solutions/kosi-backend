from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = FastAPI()

client = OpenAI(
    api_key="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",
    project="default"
)
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
