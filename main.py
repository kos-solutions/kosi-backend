from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import uvicorn

app = FastAPI()

# Citește key + project din environment
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROJECT = os.getenv("OPENAI_PROJECT_ID")

if not OPENAI_KEY:
    raise RuntimeError("LIPSESTE OPENAI_API_KEY in Railway!")

if not OPENAI_PROJECT:
    raise RuntimeError("LIPSESTE OPENAI_PROJECT_ID in Railway!")

client = OpenAI(
    api_key=OPENAI_KEY,
    project=OPENAI_PROJECT
)

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    story: str

SYSTEM_PROMPT = (
    "Tu ești Kosi, un prieten AI cald și blând pentru copii. "
    "Vorbesti simplu, drăguț și liniștitor."
)

@app.post("/story", response_model=StoryResponse)
async def story(request: StoryRequest):

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt invalid")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        content = completion.choices[0].message.content

        # Dacă e direct string
        if isinstance(content, str):
            return StoryResponse(story=content)

        # Dacă e listă de text parts
        text = "".join(
            part.text for part in content
            if hasattr(part, "text")
        )

        return StoryResponse(story=text)

    except Exception as e:
        # Afișăm eroarea reală în log
        print("Eroare OpenAI:", e)
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI error: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
