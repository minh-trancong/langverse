import requests

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
}

payload = {
    "model": "mistral-7b-instruct",
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

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    assistant_message = response_json.get('choices', [{}])[0].get('message', {}).get('content')
    print("Assistant's response: ", assistant_message)

    payload['messages'].append({"role": "assistant", "content": assistant_message})