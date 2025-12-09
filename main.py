from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

app = FastAPI()

client = OpenAI(api_key="YOUR_OPENAI_KEY_HERE")

class StoryRequest(BaseModel):
    prompt: str

KOSI_SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald, blând și empatic, creat special pentru copii. "
    "Vorbesti cu o voce jucăușă și liniștitoare. "
    "Folosești propoziții scurte și simple. "
    "Nu folosești ton robotic sau cuvinte complicate. "
    "Nu moralizezi, nu dai ordine și nu sperii copilul. "
    "Oferi siguranță, încurajare și căldură. "
    "Răspunsurile tale trebuie să sune afectuos și pline de prietenie. "
)

@app.post("/story")
async def story(request: StoryRequest):

    if not request.prompt or request.prompt.strip() == "":
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
