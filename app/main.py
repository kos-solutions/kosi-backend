from fastapi import FastAPI
from pydantic import BaseModel
from app.story_engine import generate_story

app = FastAPI()

class StoryRequest(BaseModel):
    child_name: str
    age: int
    prompt: str

@app.get("/")
def root():
    return {"status": "KOSI backend running"}

@app.post("/story")
def story_endpoint(data: StoryRequest):
    story = generate_story(
        child_name=data.child_name,
        age=data.age,
        prompt=data.prompt
    )
    return {"story": story}
