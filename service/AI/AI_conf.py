# Python packages
import os
from dotenv import load_dotenv

# OpenAI
from openai import OpenAI

# load .env file content
load_dotenv()

# openai instance
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)