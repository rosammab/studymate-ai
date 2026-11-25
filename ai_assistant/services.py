
import json
import urllib.error
import urllib.request
from urllib.parse import quote

from django.conf import settings


class AIServiceError(Exception):
    """Raised when the AI service cannot generate a response."""


def generate_ai_response(messages):
    """
    Generate an AI response using the Google Gemini API.
    """

    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        raise AIServiceError(
            "Gemini API is not configured. "
            "Add GEMINI_API_KEY to your environment."
        )

    model = getattr(
        settings,
        "GEMINI_MODEL",
        "gemini-2.5-flash-lite"
    )

    # Convert Django chat messages into Gemini format.
    contents = []

    for message in messages:

        role = message.get("role")
        content = message.get("content")

        if role not in ["user", "assistant"]:
            raise AIServiceError("Invalid conversation message role.")

        if not isinstance(content, str) or not content.strip():
            continue

        gemini_role = (
            "model" if role == "assistant" else "user"
        )

        contents.append({
            "role": gemini_role,
            "parts": [
                {"text": content}
            ]
        })

    if not contents:
        raise AIServiceError("No valid messages were provided.")

    payload = {
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "You are StudyMate AI, a helpful educational "
                        "assistant. Help students understand concepts, "
                        "prepare for exams, summarize topics and improve "
                        "their learning. Give clear, accurate and "
                        "easy-to-understand answers."
                    )
                }
            ]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{quote(model, safe='')}:generateContent"
    )

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        candidates = result.get("candidates", [])

        if not candidates:
            raise AIServiceError(
                "Gemini did not return a response. "
                "The request may have been blocked by a safety filter."
            )

        parts = candidates[0].get(
            "content", {}
        ).get("parts", [])

        answer = "".join(
            part.get("text", "")
            for part in parts
        )

        if not answer.strip():
            raise AIServiceError(
                "Gemini returned an empty response."
            )

        return answer.strip()

    except urllib.error.HTTPError as error:

        try:
            error_data = json.loads(
                error.read().decode("utf-8")
            )

            error_message = error_data.get(
                "error", {}
            ).get(
                "message",
                "Unknown Gemini API error."
            )

        except (ValueError, AttributeError):
            error_message = "Unable to read the provider error."

        raise AIServiceError(
            f"Gemini API error ({error.code}): {error_message}"
        ) from error

    except (urllib.error.URLError, TimeoutError) as error:
        raise AIServiceError(
            "Could not connect to Gemini. Please try again."
        ) from error

    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise AIServiceError(
            "Invalid response received from Gemini."
        ) from error
