
import json
import urllib.error
import urllib.request
from io import BytesIO
from urllib.parse import quote

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from xml.sax.saxutils import escape

from .models import GeneratedArtifact
from .services import generate_ai_response, AIServiceError


def generate_pdf(user, prompt):
    """Generate educational content and save it as a PDF."""

    content = generate_ai_response([
        {
            "role": "user",
            "content": (
                "Create well-organized educational study material "
                "about the following topic. Use a clear title, "
                "section headings, examples and a conclusion. "
                "Return plain text with headings on separate lines. "
                "Do not include Markdown formatting.\n\n"
                f"Topic: {prompt}"
            )
        }
    ])

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "StudyTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4338ca"),
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "StudyHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4338ca"),
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = styles["BodyText"]
    body_style.leading = 16
    body_style.spaceAfter = 8

    story = [
        Paragraph(escape(prompt), title_style),
        Spacer(1, 10),
    ]

    for line in content.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        safe_line = escape(line)

        # Simple heading detection.
        if (
            len(line) < 100
            and (
                line.isupper()
                or line.endswith(":")
                or line.lower().startswith("conclusion")
            )
        ):
            story.append(
                Paragraph(safe_line, heading_style)
            )
        else:
            story.append(
                Paragraph(safe_line, body_style)
            )

    document.build(story)

    filename = f"{slugify(prompt[:60]) or 'study-notes'}.pdf"

    artifact = GeneratedArtifact(
        user=user,
        artifact_type="pdf",
        title=prompt[:200],
        prompt=prompt,
    )

    artifact.file.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=True,
    )

    return artifact


def generate_image(user, prompt):
    """Generate an image using the Gemini image model."""

    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        raise AIServiceError("Gemini API is not configured.")

    model = getattr(
        settings,
        "GEMINI_IMAGE_MODEL",
        "gemini-3.1-flash-image"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Create a high-quality educational image "
                            "based on this description: " + prompt
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": "1:1"
            }
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
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        try:
            details = json.loads(error.read().decode("utf-8"))
            message = details.get("error", {}).get(
                "message", "Image generation failed."
            )
        except (ValueError, AttributeError):
            message = "Could not read the Gemini error."

        raise AIServiceError(
            f"Gemini image error ({error.code}): {message}"
        ) from error

    except (urllib.error.URLError, TimeoutError) as error:
        raise AIServiceError(
            "Could not connect to the Gemini image service."
        ) from error

    candidates = result.get("candidates", [])

    if not candidates:
        raise AIServiceError(
            "Gemini did not return an image. Try another prompt."
        )

    image_data = None
    mime_type = "image/png"

    for part in candidates[0].get("content", {}).get("parts", []):
        inline_data = part.get("inlineData")

        if inline_data and inline_data.get("data"):
            image_data = inline_data["data"]
            mime_type = inline_data.get(
                "mimeType", "image/png"
            )
            break

    if not image_data:
        raise AIServiceError(
            "Gemini returned no image data. Try a more specific prompt."
        )

    import base64

    try:
        image_bytes = base64.b64decode(
            image_data,
            validate=True
        )
    except (ValueError, TypeError) as error:
        raise AIServiceError(
            "Gemini returned invalid image data."
        ) from error

    extension = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
    }.get(mime_type, "png")

    filename = (
        f"{slugify(prompt[:50]) or 'study-image'}.{extension}"
    )

    artifact = GeneratedArtifact(
        user=user,
        artifact_type="image",
        title=prompt[:200],
        prompt=prompt,
    )

    artifact.file.save(
        filename,
        ContentFile(image_bytes),
        save=True,
    )

    return artifact
