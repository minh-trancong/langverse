from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import logging

class Text(BaseModel):
    text: str

app = FastAPI()

client = OpenAI(api_key='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')

messages = [
    {"role": "system", "content": "Hệ thống tư vấn giữa nhân viên tư vấn tại siêu thị điện máy Thế giới di động và An Phát PC. Chỉ sử dụng những thông tin được cho trong context"},
]

@app.post("/api/")
async def get_openai_response(item: Text):
    messages.append({"role": "user", "content": item.text})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(f"Assistant's response: {response.choices[0].message.content}")
    print(f"Messages: {messages}")
    return {"response": response.choices[0].message.content}

@app.get("/api/reset")
async def reset_messages():
    global messages
    messages = [
        {"role": "system", "content": "Hệ thống tư vấn giữa nhân viên tư vấn tại siêu thị điện máy Thế giới di động và An Phát PC. Chỉ sử dụng những thông tin được cho trong context"},
    ]
    print(f"Messages: {messages}")   
    return {"status": "Messages reset"}