import os
import time
import logging

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Configure Logger
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# Gemini API Key
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY is missing in the .env file.")


# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Models to try (Fallback System)
# --------------------------------------------------

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest"
]


# --------------------------------------------------
# AI Code Review
# --------------------------------------------------

def review_with_gemini(code: str) -> str:
    """
    Generate AI Code Review using Gemini.
    Automatically switches to another model if one fails.
    """

    prompt = f"""
You are an experienced Senior Software Engineer.

Review the following Python code.

Return the response in Markdown.

# Code Review Report

## 1. Summary

## 2. Bugs

## 3. Improvements

## 4. Best Practices

## 5. Performance

## 6. Security

## 7. Complexity

## 8. Code Quality Score (/10)

## 9. Final Recommendation

Python Code:

{code}
"""

    last_error = ""

    for model in MODELS:

        logger.info(f"Trying Gemini Model: {model}")

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if response.text:
                    logger.info(f"Success using {model}")
                    return response.text

                return "No response generated."

            except Exception as e:

                last_error = str(e)

                logger.warning(
                    f"{model} | Attempt {attempt + 1} failed\n{e}"
                )

                time.sleep(2)

        logger.warning(f"Switching to next model...")

    logger.exception("All Gemini models failed.")

    return (
        "Unable to generate AI review.\n\n"
        "All Gemini models failed.\n\n"
        f"Last Error:\n{last_error}"
    )