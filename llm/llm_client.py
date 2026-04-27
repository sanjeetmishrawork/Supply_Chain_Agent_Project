from openai import OpenAI
from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()


def get_llm_client():
    """
    Create and return OpenAI client
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables."
        )

    client = OpenAI(api_key=api_key)

    return client


def call_llm(prompt: str) -> str:
    """
    Generic LLM call function

    Input:
        prompt (str)

    Output:
        response (str)
    """

    client = get_llm_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior supply chain strategy expert. "
                    "Provide concise, business-relevant reasoning."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()