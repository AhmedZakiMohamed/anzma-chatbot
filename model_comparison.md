# Local LLM Comparison: llama3.2:3b vs qwen2.5:7b

**Purpose:** choose a local model for the first Anzma AI Insight chatbot (offline, no external APIs).

## Test setup (hardware)

- **Machine:** MacBook Pro, Apple M3 Pro, 36 GB unified memory, macOS
- **Runtime:** Ollama (default context window: 32,768 tokens)

## Method

Each model answered the same three prompts:

1. "What is a CCTV system?" (general English)
2. "Explain the difference between access control and fire alarm systems." (technical English)
3. "اشرح لي إيه الفرق بين كاميرات IP والكاميرات التناظرية" (Arabic)


## Results

| | llama3.2:3b | qwen2.5:7b |
|---|---|---|
| Size on disk | 2.0 GB | 4.7 GB |
| Memory while loaded | 6.0 GB | 6.6 GB |
| Processor | 100% GPU | 100% GPU |
| Generation speed (tokens/s, 3 prompts) | 58.4 / 57.4 / 55.9 (avg **57.2**) | 29.2 / 28.9 / 29.0 (avg **29.0**) |
| Total response time (s, 3 prompts) | 8.1 / 12.1 / 12.2 | 11.1 / 19.7 / 15.4 |



## Hardware requirements

Both models ran entirely on the GPU of the machine above. Observed RAM while loaded was 6.0 GB (llama3.2:3b) and 6.6 GB (qwen2.5:7b), so either fits easily in 36 GB.

## Observations

- **Memory:** a model more than twice as large on disk used only about 0.6 GB more RAM. Most of the memory comes from Ollama's large default context window, not from the model weights. A smaller context would probably reduce it (not tested).
- **Speed:** llama3.2:3b is about twice as fast. qwen2.5:7b at about 29 tokens/s is still comfortable for a chat.
- **llama3.2:3b:** fast and well structured in English, but its Arabic answer was mostly incoherent (mixed scripts, invented phrases) and it mentioned CDs/DVDs as CCTV storage, which is outdated.
- **qwen2.5:7b:** clearer English and readable Arabic, but it still made mistakes. For example, it implied analog cameras need a network and did not mention PoE or DVR vs NVR. In the chatbot test, a few Korean characters also appeared inside an Arabic answer.
- **Both models** missed that access control is normally integrated with the fire alarm so doors release during a fire. They sound confident but are shallow on domain facts.

## Selection

**Chosen model: qwen2.5:7b.**

**Why:** Arabic support is the deciding factor, since the product will serve regional customers. It also gave better technical English, and its speed is adequate for interactive use. Its memory cost is close to the 3B model, and the machine has plenty of headroom.

**Trade-off:** half the speed of llama3.2:3b. The 3B model remains a reasonable fallback for simple, English-only, speed-critical tasks.

## Limitations and next steps

- Only three prompts and one run each; results are indicative, not a benchmark.
- llama3.2:3b's prompts ran in one session without clearing history, while qwen2.5:7b's were run with `/clear` between prompts. Generation speed is not affected, but prompt-processing numbers are not directly comparable.
- Because both models make domain errors, Anzma AI Insight should answer from verified system data (database queries or retrieval), not from model memory.
- Next: evaluate a larger model (e.g. qwen2.5:14b) and test with real system data.