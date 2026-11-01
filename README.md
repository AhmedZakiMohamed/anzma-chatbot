# Anzma Local Chatbot

A minimal command-line chatbot that runs a language model **entirely on your own machine** using [Ollama](https://ollama.com). No external model APIs are called, so it works fully offline once the model is downloaded.

This is the first building block of Anzma AI Insight, where data from ELV and building systems should stay local.

## Requirements

- Python 3.9 or newer
- Git
- [Ollama](https://ollama.com/download)
- Enough free memory for the model. The default model (`qwen2.5:7b`) used about 6.6 GB of RAM while loaded in our tests (see `model_comparison.md`).

## Installation

1. **Install Ollama** from https://ollama.com/download and open it once so the local service is running.

2. **Download the model** (needs internet, only once):

   ```bash
   ollama pull qwen2.5:7b
   ```

3. **Clone this repository and enter it:**

   ```bash
   git clone https://github.com/AhmedZakiMohamed/anzma-chatbot.git
   cd anzma-chatbot
   ```

4. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

5. **Install the Python dependency:**

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python chatbot.py
```

Commands inside the chat:

| Input | Action |
|---|---|
| `/clear` | Start a new conversation (clears history) |
| `exit` or `quit` | Leave the chatbot |

## Choosing another model

The model and server address can be changed with environment variables, with no code changes:

```bash
OLLAMA_MODEL=llama3.2:3b python chatbot.py
OLLAMA_URL=http://localhost:11434/api/chat python chatbot.py
```

Download any other model first with `ollama pull <name>`.

## Verifying it works offline

1. Make sure the model is already downloaded (`ollama list`).
2. Turn off Wi-Fi / disconnect the network.
3. Run `python chatbot.py` and ask a question. It should still answer.

The code only talks to `localhost`, so no data leaves the machine.

## Project structure

```
chatbot.py                 Chatbot (talks to Ollama's local HTTP API)
requirements.txt           Python dependencies
model_comparison.md   Comparison of llama3.2:3b and qwen2.5:7b
```

## How it works

Ollama exposes a local HTTP API on port 11434. The script sends the conversation to `/api/chat` and prints the reply as it streams back. The model has no memory of its own, so the script keeps the message history and sends it with every request. A system prompt sets the assistant's role and asks it to say when it is unsure.

## Troubleshooting

- **"Cannot reach Ollama"**: open the Ollama app (or run `ollama serve`) and try again.
- **Model not found**: run `ollama pull qwen2.5:7b`, or set `OLLAMA_MODEL` to a model shown by `ollama list`.
- **Slow or out of memory**: use a smaller model such as `llama3.2:3b`.

## Known limitations

Small local models can sound confident while being wrong, especially on technical topics and in Arabic. Answers about real system data should come from verified data sources rather than from the model's own knowledge.
