from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from searching.embedded_search import get_selected_fields
from searching.input import set_input

class Text(BaseModel):
    text: str

app = FastAPI()

origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "Hệ thống tư vấn giữa nhân viên tư vấn laptop tại siêu thị điện máy Thế giới di động và An Phát PC. Chỉ sử dụng những thông tin được cho trong context."},
]

@app.post("/api/")
async def get_openai_response(item: Text):
    set_input(item.text)
    selected_fields = get_selected_fields()
    # Convert selected_fields to a string
    selected_fields_str = str(selected_fields)
    messages[0] = {"role": "system", "content": selected_fields_str}
    messages.append({"role": "user", "content": item.text})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(f"Assistant's response: {response.choices[0].message.content}")
    print(f"Messages: {messages}")
    return {"response": response.choices[0].message.content, "selected_fields": selected_fields}

@app.get("/api/reset")
async def reset_messages():
    global messages
    messages = [
        {"role": "system", "content": "Hệ thống tư vấn giữa nhân viên tư vấn tại siêu thị điện máy Thế giới di động và An Phát PC. Chỉ sử dụng những thông tin được cho trong context"},
    ]
    print(f"Messages: {messages}")   
    return {"status": "Messages reset"}