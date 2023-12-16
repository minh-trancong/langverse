from openai import OpenAI
import os


os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "Đây là cuộc hội thoại giữa một nhân viên bán hàng của Thế giới di động và An Phát PC và khách hàng là một sinh viên nghèo cần mua máy tính. Các câu trả lời bằng tiếng Việt. Mục đích của assistant là tư vấn tận tình, khéo léo và đề nghị khách hàng vào website để mua hàng. Các thông tin chỉ được phép lấy từ: thegioidididong.com hoặc anphatpc.com.vn"
        },
        {
            "role": "user",
            "content": "Bạn là một nhân viên bán hàng, tư vấn cho tôi là một sinh viên nghèo cần mua máy tính. Nếu câu hỏi chưa rõ ràng, hãy hỏi lại. Ban đầu hãy hỏi bạn mua màu ở An Phát PC hay Thế giới di động để đưa ra đề xuất phù hợp."
        },
        {
            "role": "assistant",
            "content": "Đúng vậy, mời bạn đặt câu hỏi"
        },
    ]
}

while True:
    user_input = input("Hãy đưa ra câu hỏi của bạn: ")
    payload['messages'].append({"role": "user", "content": user_input})

    chat_completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=payload['messages'])
    assistant_message = chat_completion['choices'][0].get('text')
    print("Assistant's response: ", assistant_message)

    payload['messages'].append({"role": "assistant", "content": assistant_message})