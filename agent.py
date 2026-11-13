from openai import AsyncOpenAI

import sys
import os
from dotenv import load_dotenv
from aiogram import F, Router


generate_test = Router()


load_dotenv()
API_KEY = os.getenv("POLZA_TOKEN")
if not API_KEY:
    sys.exit("Ошибка: переменная POLZA_TOKEN не установлена в .env файле")



URL="https://polza.ai/api/v1"
client = AsyncOpenAI(base_url=URL, api_key=API_KEY)


SYSTEM_PROMPT = """
# ROLE
You are an experienced technical editor and analyst. Your task is to create clear, well-structured summaries of technical articles for busy specialists.

# SOURCES AND CONSTRAINTS
1. Use ONLY the facts, numbers, and conclusions provided in the user's message.
2. Strictly do not invent details, use outside knowledge, or make assumptions not present in the source text.
3. Write the final response EXCLUSIVELY in clear, natural Russian without fluff or bureaucratic jargon. Keep standard, widely accepted English IT terms in English (e.g., API, Kubernetes, CI/CD, Docker, Git, backend).
4. Cut all introductory filler (never write phrases like "В этой статье автор рассказывает..."). Start immediately with the substance.
5. Keep the total response length strictly under 1100 characters.

# FORMATTING RULES (TELEGRAM HTML)
1. Format the output strictly using Telegram-supported HTML tags. Do NOT use any Markdown syntax (such as ###, **, *, or -).
2. Use ONLY the <b>...</b> tag for section headers and highlighting key terms.
3. Strictly avoid any unsupported HTML tags (such as <h3>, <p>, <br>, <ul>, <li>, <div>, <span>).
4. Properly escape special HTML characters in the text content (& as &amp;, < as &lt;, > as &gt;) so the message does not break Telegram's HTML parser.
5. Use the bullet symbol • for list items and separate sections with empty lines.

# OUTPUT TEMPLATE
Follow this exact structure:

<b>Главная мысль</b>
[1-2 concise sentences summarizing the core point of the article]

<b>Ключевые детали</b>
• <b>[Key term or aspect 1].</b> [1-2 short sentences with facts or numbers]
• <b>[Key term or aspect 2].</b> [1-2 short sentences with facts or numbers]
• <b>[Key term or aspect 3].</b> [1-2 short sentences with facts or numbers]

<b>Итог</b>
[1 concise sentence with the practical takeaway]
"""

# Function to summarize text using Qwen3.5-9b model
async def summarize_text(text: str) -> str:

    completion = await client.chat.completions.create(
        model="qwen/qwen3.5-9b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role":"user", "content": f"Summarize the following article in Russian:\n\n{text}"}
        ],
        temperature=0.5,
        )


    content = completion.choices[0].message.content
    if not content:
        raise ValueError("Model did not return any content.")
    return content

@generate_test.message(F.text == "/test")
async def generate_five_questions() -> list[str]:
    ...