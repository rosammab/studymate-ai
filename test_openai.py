import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

response = client.chat.completions.create(
    model=settings.OPENAI_MODEL,
    messages=[
        {
            "role": "user",
            "content": "Explain Python in two sentences."
        }
    ]
)

print(response.choices[0].message.content)