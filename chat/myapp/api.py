from rest_framework.decorators import api_view
from rest_framework.response import Response
from .openai_key import key
import requests

openai_secret_key = key

@api_view(['GET', 'POST'])
def chat_api(request):
    try:
        # 获取用户发送的消息
        user_message = request.GET.get('msg', '')

        # 检查消息是否为空
        if not user_message:
            return Response({'error': 'Message is empty'}, status=400)

        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_secret_key}'
        }

        # 构建请求数据
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7
        }

        # 发送请求到OpenAI
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

        # 解析OpenAI的响应
        response_data = response.json()
        
        # 检查响应是否包含"choices"键
        if "choices" in response_data:
            text = response_data["choices"][0]
        else:
            text = "No response from OpenAI"

        # 返回OpenAI的响应
        return Response({'text': text})

    except Exception as e:
        return Response({'error': str(e)}, status=500)
