import os
import time

from dotenv import load_dotenv
from google import genai


# =================================
# Load Environment Variables
# =================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


# =================================
# Gemini Client
# =================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =================================
# Ask Gemini
# =================================

def ask_gemini(question: str):

    model_name = "gemini-3.6-flash"

    last_error = None

    for attempt in range(3):

        try:

            chat = client.chats.create(
                model=model_name
            )

            response = chat.send_message(
                message=question
            )

            return response.text

        except Exception as e:

            last_error = e
            error_text = str(e)

            # Retry temporary server errors
            if "503" in error_text or "UNAVAILABLE" in error_text:

                time.sleep(2 ** attempt)

            else:

                raise e

    raise RuntimeError(
        f"Gemini is temporarily unavailable. "
        f"Please try again later. Details: {last_error}"
    )
