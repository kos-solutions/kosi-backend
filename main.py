from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROJECT = os.getenv("OPENAI_PROJECT_ID", "default")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    project=OPENAI_PROJECT
)

class StoryRequest(BaseModel):
    prompt: str

KOSI_SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald..."
)

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
            max_tokens=400,
            temperature=0.7
        )

        story_text = completion.choices[0].message["content"]
        return {"story": story_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
