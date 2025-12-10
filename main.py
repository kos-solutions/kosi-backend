from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import os

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    story: str

KOSI_SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald, blând și empatic, creat special pentru copii. "
    "Vorbesti cu o voce jucăușă și liniștitoare. "
    "Folosești propoziții scurte și simple. "
    "Nu folosești ton robotic sau cuvinte complicate. "
    "Nu moralizezi, nu dai ordine și nu sperii copilul. "
    "Oferi siguranță, încurajare și căldură. "
    "Răspunsurile tale trebuie să sune afectuos și prietenoase. "
)


@app.post("/story", response_model=StoryResponse)
async def story(request: StoryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt invalid")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": KOSI_SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt},
            ],
            temperature=0.7,
            max_tokens=300
        )

        # 👇 FIX: noul SDK returnează content ca LISTĂ de ContentParts
        content = completion.choices[0].message.content

        # content poate fi:
        # 1) un string simplu
        # 2) o listă de obiecte {"type":"text","text":"..."}
        if isinstance(content, str):
            story_text = content
        else:
            # extrage și concatenează textul
            story_text = "".join(
                part.text for part in content if hasattr(part, "text")
            )

        return StoryResponse(story=story_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
