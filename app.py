import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class Topic(BaseModel):
    topic: str


def generate_post(topic):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
                Напиши подробный Telegram-пост на тему: {topic}

                Требования:
                - интересный заголовок
                - короткие абзацы
                - понятный стиль
                - подзаголовки
                - вывод в конце
                """
            }
        ],
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content


@app.get("/")
async def root():
    return {"message": "Blog GPT API работает"}


@app.get("/heartbeat")
async def heartbeat():
    return {"status": "OK"}


@app.post("/generate-post")
async def generate_post_api(data: Topic):

    post = generate_post(data.topic)

    return {
        "topic": data.topic,
        "post": post
    }
