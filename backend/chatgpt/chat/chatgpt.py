import openai
from django.conf import settings

API_KEY = settings.API_KEY

openai.api_key = API_KEY

def generate_response(request_text):
    response = openai.Completion.create(
        prompt=request_text,
        engine='gpt-3.5-turbo-instruct',
        # max_tokens=max(1000, len(request_text) * 5),
        max_tokens=3900,
        temperature=0,
        n=1,
        stop=None,
        timeout=15
    )
    return response.choices[0].text.strip()


