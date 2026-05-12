import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


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
async def generate_post_api(request: Request):

    body = await request.json()

    topic = body.get("topic")

    if not topic:
        topic = "Искусственный интеллект в бизнесе"

    post = generate_post(topic)

    return {
        "topic": topic,
        "post": post
    }
