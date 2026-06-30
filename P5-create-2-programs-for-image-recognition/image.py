"""
Image Recognition — Terminal Interface
Model : moondream (via Ollama, runs locally)
Usage : python image_recognition.py
"""

import os
import sys
import base64
from pathlib import Path

try:
    import ollama
except ImportError:
    print("Missing dependency. Run:  pip install ollama")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════

MODEL      = "moondream"
SUPPORTED  = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

BANNER = """
╔══════════════════════════════════════════════════════╗
║       Image Recognition  —  Terminal Interface       ║
║       Powered by Moondream (local via Ollama)        ║
╚══════════════════════════════════════════════════════╝

Commands:
  :load <image_path>    — load and analyse an image
  :help                 — show this message
  :quit / exit          — exit

After loading an image you can ask follow-up questions about it.
"""

# ═══════════════════════════════════════════════════════════════════════════
#  IMAGE LOADING
# ═══════════════════════════════════════════════════════════════════════════

def load_image(path_str: str) -> tuple[str, str] | None:
    """Load image from disk, return (path, base64_data) or None on error."""
    path = Path(path_str.strip('"').strip("'"))   # handle quoted paths
    if not path.exists():
        print(f"  [!] File not found: {path}")
        return None
    if path.suffix.lower() not in SUPPORTED:
        print(f"  [!] Unsupported format. Supported: {', '.join(SUPPORTED)}")
        return None

    data = path.read_bytes()
    b64  = base64.b64encode(data).decode("utf-8")
    size = len(data) / 1024
    print(f"  [+] Loaded: {path.name}  ({size:.1f} KB)")
    return str(path), b64


# ═══════════════════════════════════════════════════════════════════════════
#  INFERENCE
# ═══════════════════════════════════════════════════════════════════════════

def analyse(image_path: str, prompt: str) -> str:
    """Send image + prompt to moondream via Ollama."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role":    "user",
                "content": prompt,
                "images":  [image_path],   # Ollama accepts file path directly
            }
        ],
    )
    return response["message"]["content"].strip()


# ═══════════════════════════════════════════════════════════════════════════
#  TERMINAL REPL
# ═══════════════════════════════════════════════════════════════════════════

def repl():
    print(BANNER)

    current_image: str | None = None   # currently loaded image path

    while True:
        try:
            # Show prompt differently when image is loaded
            indicator = f"[{Path(current_image).name}]" if current_image else "[no image]"
            user_input = input(f"\n{indicator} > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nBye!")
            break

        if not user_input:
            continue

        # ── Commands ─────────────────────────────────────────────────────
        if user_input.lower() in (":quit", "exit", "quit"):
            print("Bye!")
            break

        elif user_input.lower() == ":help":
            print(BANNER)

        elif user_input.lower().startswith(":load"):
            parts = user_input.split(maxsplit=1)
            if len(parts) < 2:
                print("  Usage:  :load <image_path>")
                print("  Example: :load C:\\Users\\dell\\Pictures\\photo.jpg")
                continue

            result = load_image(parts[1])
            if result:
                current_image = result[0]
                print("  Analysing image…")
                try:
                    description = analyse(current_image, "Describe this image in detail. What do you see?")
                    print("\n" + "─" * 60)
                    print(description)
                    print("─" * 60)
                    print("\n  Image loaded! You can now ask follow-up questions.")
                except Exception as e:
                    print(f"  [Error] {e}")
                    print("  Make sure Ollama is running:  ollama serve")

        # ── Follow-up question about loaded image ─────────────────────────
        else:
            if not current_image:
                print("  [!] No image loaded. Use  :load <image_path>  first.")
                continue
            print("  Thinking…")
            try:
                answer = analyse(current_image, user_input)
                print("\n" + "─" * 60)
                print(answer)
                print("─" * 60)
            except Exception as e:
                print(f"  [Error] {e}")
                print("  Make sure Ollama is running:  ollama serve")


# ═══════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    # Check if Ollama is reachable and model exists
    print("  Checking Ollama…", end=" ")
    try:
        result = ollama.list()
        models = [m.model for m in result.models]   # new SDK uses objects not dicts
        if not any(MODEL in m for m in models):
            print(f"\n\n  [!] Model '{MODEL}' not found. Run:\n")
            print(f"      ollama pull {MODEL}\n")
            sys.exit(1)
        print("OK")
    except Exception as e:
        print(f"\n\n  [!] Could not connect to Ollama: {e}\n")
        sys.exit(1)

    repl()


if __name__ == "__main__":
    main()
