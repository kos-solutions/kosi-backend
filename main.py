from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class StoryRequest(BaseModel):
    child_name: str
    age: int
    prompt: str

class StoryResponse(BaseModel):
    story: str

@app.post("/story", response_model=StoryResponse)
async def generate_story(req: StoryRequest):
    # TODO: aici adaugi AI-ul real mai târziu
    fake_story = (
        f"O poveste despre {req.child_name}, "
        f"care la varsta de {req.age} ani a descoperit {req.prompt}. "
        f"A fost o aventura minunata!"
    )

    return StoryResponse(story=fake_story)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
