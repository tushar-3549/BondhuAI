import os
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI, RateLimitError, AuthenticationError

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def ask_openai(msg):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": msg}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        ans = response.choices[0].message.content.strip()
        return ans
    except RateLimitError:
        return "OpenAI API quota exceeded. Please try again later."
    except AuthenticationError:
        return "Invalid API key. Please check your OpenAI credentials."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def chatbot(request):
    if request.method == "POST":
        msg = request.POST.get("message")
        res = ask_openai(msg)
        return JsonResponse({'message': msg, 'response': res})
    return render(request, 'chatbot.html')
