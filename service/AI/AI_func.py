# AI client
from .AI_conf import openai_client


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


# async chat streamer
async def stream_chat_response(messages: list):
    response = openai_client.responses.stream(
        model="gpt-4.1-mini",
        input=messages,
    )

    for event in response:
        if event.type == "response.output_text.delta":
            yield event.delta