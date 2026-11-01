import json
import os

import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")

SYSTEM_PROMPT = (
    "You are Anzma AI Insight, a helpful assistant for an ELV and "
    "smart-building systems company (CCTV, access control, fire alarm, "
    "BMS, networking). Answer in the same language the user writes in. "
    "Be concise. If you are not sure about something, say so instead of guessing."
)


def new_history():
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def ask(history):
    payload = {"model": MODEL, "messages": history, "stream": True}
    reply = ""
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            piece = chunk.get("message", {}).get("content", "")
            print(piece, end="", flush=True)
            reply += piece
            if chunk.get("done"):
                break
    print()
    return reply


def main():
    history = new_history()
    print(f"Anzma local chatbot (model: {MODEL})")
    print("Type 'exit' to quit, '/clear' to start a new conversation.\n")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            break
        if user == "/clear":
            history = new_history()
            print("(conversation cleared)\n")
            continue

        history.append({"role": "user", "content": user})
        print("Bot: ", end="", flush=True)
        try:
            reply = ask(history)
        except requests.exceptions.ConnectionError:
            print("\nCannot reach Ollama. Is the Ollama app running?")
            history.pop()
            continue
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {e}")
            history.pop()
            continue

        history.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    main()