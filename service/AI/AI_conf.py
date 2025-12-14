# Python packages
import os
from dotenv import load_dotenv

# OpenAI
from openai import OpenAI, AsyncOpenAI

# load .env file content
load_dotenv()

# openai instance
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# async openai instance
async_openai_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)