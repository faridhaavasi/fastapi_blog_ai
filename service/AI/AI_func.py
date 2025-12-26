# AI client
from .AI_conf import openai_client, async_openai_client

from typing import List


# get keywords from AI
def get_keywords(description: str) -> str:
    """
    Send request to OpenAI API and return keywords as a list of strings.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract 2-3 keywords from the text. "
                           "Return them as a comma-separated list only (no extra words)."
            },
            {"role": "user", "content": description}
        ]
    )

    keywords_text = response.choices[0].message.content.strip()
    return [k.strip() for k in keywords_text.split(",")]


# chatbot openai async client for chatbot
async def stream_chat_response(message: str):
    async with async_openai_client.responses.stream(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Never repeat, quote, or echo the user's message. "
                    "Answer directly without prefixes like 'you:' or 'user:'."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
    ) as response:

        async for event in response:
            if event.type == "response.output_text.delta":
                yield event.delta


# chatbot openai async client for post chatbot
async def stream_chat_response_post(message: str, last_posts: List[str]):
    posts_context = "\n".join(f"- {post}" for post in last_posts)

    async with async_openai_client.responses.stream(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                            "You are a professional content writing assistant.\n"
                            "Your job is to help the user write better posts.\n"
                            "Analyze the user's previous posts to understand their tone, "
                            "style, strengths, and weaknesses.\n"
                            "Do NOT repeat or quote the user's message.\n"
                            "Do NOT use prefixes like 'user:' or 'you:'.\n\n"
                            f"User's previous posts:\n{posts_context}"
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
    ) as response:

        async for event in response:
            if event.type == "response.output_text.delta":
                yield event.delta