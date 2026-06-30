"""
AI Image Classifier — Streamlit App
LLM Vision : Groq (meta-llama/llama-4-scout-17b-16e-instruct)
API Key    : entered via sidebar in the UI (no .env needed)
"""

import base64
import io
import streamlit as st
from groq import Groq
from PIL import Image


# ═══════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SYSTEM_PROMPT = """You are an expert image analyst. When given an image:
1. Identify the main subject clearly
2. List the top 3 most likely labels with confidence estimates (as percentages)
3. Give a brief description of what you see
Be concise and structured."""

CLASSIFY_PROMPT = """Analyse this image and respond in exactly this format:

TOP PREDICTIONS:
1. <label>: <confidence>%
2. <label>: <confidence>%
3. <label>: <confidence>%

DESCRIPTION:
<2-3 sentence description of the image>"""


# ═══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL image to base64 string."""
    buffer = io.BytesIO()
    fmt = image.format if image.format else "JPEG"
    if fmt not in ("JPEG", "PNG", "WEBP", "GIF"):
        fmt = "JPEG"
    image.save(buffer, format=fmt)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def classify_image(client: Groq, image: Image.Image, extra_question: str = "") -> str:
    """Send image to Groq vision model and return response."""
    b64 = image_to_base64(image)
    fmt = (image.format or "JPEG").lower()
    if fmt not in ("jpeg", "png", "webp", "gif"):
        fmt = "jpeg"
    mime = f"image/{fmt}"

    prompt = CLASSIFY_PROMPT
    if extra_question:
        prompt += f"\n\nALSO ANSWER THIS QUESTION:\n{extra_question}"

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type":      "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        max_tokens=1024,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def ask_followup(client: Groq, image: Image.Image, question: str) -> str:
    """Ask a follow-up question about the image."""
    b64  = image_to_base64(image)
    fmt  = (image.format or "JPEG").lower()
    if fmt not in ("jpeg", "png", "webp", "gif"):
        fmt = "jpeg"
    mime = f"image/{fmt}"

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type":      "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                    {"type": "text", "text": question},
                ],
            }
        ],
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ═══════════════════════════════════════════════════════════════════════════
#  UI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="AI Image Classifier",
        page_icon="🔍",
        layout="centered",
    )

    st.title("🔍 AI Image Classifier")
    st.write("Upload an image and let Groq AI tell you what's in it!")

# ── Hardcoded API key ─────────────────────────────────────────────────
    api_key = "     "   # ← paste your key here

    with st.sidebar:
        st.markdown("**Model:** `llama-3.2-11b-vision`")
        st.markdown("**Provider:** [Groq](https://console.groq.com)")


    # Build Groq client
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialise Groq client: {e}")
        return

    # ── Image upload ──────────────────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "Choose an image…",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded_file is None:
        return

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # ── Classify button ───────────────────────────────────────────────────
    if st.button("🔍 Classify Image", use_container_width=True):
        with st.spinner("Analysing image with Groq AI…"):
            try:
                result = classify_image(client, image)
                st.session_state["last_result"] = result
                st.session_state["image"]       = image
            except Exception as e:
                st.error(f"Error: {e}")
                return

    # ── Show results ──────────────────────────────────────────────────────
    if "last_result" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Results")
        st.markdown(st.session_state["last_result"])

        # ── Follow-up questions ───────────────────────────────────────────
        st.markdown("---")
        st.subheader("💬 Ask a follow-up question")
        question = st.text_input(
            "Question about the image",
            placeholder="e.g. What colour is the car? Is there any text?",
        )
        if st.button("Ask", use_container_width=True) and question:
            with st.spinner("Thinking…"):
                try:
                    answer = ask_followup(client, st.session_state["image"], question)
                    st.markdown(f"**Answer:** {answer}")
                except Exception as e:
                    st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
