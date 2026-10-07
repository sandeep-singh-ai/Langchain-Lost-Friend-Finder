# Langchain Lost Friend Finder Agent

A LangChain command-line agent that looks up a person you have lost touch with. You pick how the lookup runs: a live web search, an OpenAI model, or a local Ollama model.

Each path asks for a name and returns public information, including at least two interesting facts when a language model is used.

## How it works

| Mode | Command | What it uses | Best for |
| --- | --- | --- | --- |
| Web | `web` | [SerpAPI](https://serpapi.com/) Google search | Fresh public results from the web |
| OpenAI | `agent` | `gpt-4o-mini` via LangChain | A short summary from a hosted model |
| Local | `local` | Ollama `gemma2:2b` | The same summary without sending the name to OpenAI |

```
You
  │
  ▼
main.py  ── web ──► SerpAPI search
         ── agent ─► ChatOpenAI (gpt-4o-mini)
         ── local ─► ChatOllama (gemma2:2b)
  │
  ▼
Printed facts or search snippets
```

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (or another way to install the dependencies in `pyproject.toml`)
- An [OpenAI API key](https://platform.openai.com/api-keys) for `agent`
- A [SerpAPI key](https://serpapi.com/manage-api-key) for `web`
- [Ollama](https://ollama.com/) with the `gemma2:2b` model for `local`

## Setup

```bash
uv sync
```

Create a `.env` file in the project root. Do not commit it.

```bash
OPENAI_API_KEY=your_openai_key
SERPAPI_API_KEY=your_serpapi_key
LANGSMITH_API_KEY=langsmith api key
TAVILY_API_KEY= talivy api key to search with LLM
```

`OPENAI_API_KEY` is required for `agent`. `SERPAPI_API_KEY` is required for `web`. `local` does not call those APIs.

For the local model:

```bash
ollama pull gemma2:2b
ollama serve
```

## Run

```bash
uv run python main.py
```

You will be asked which lookup to use:

```text
You like you use the web search or the openAI agent? (web/agent/local):
```

Then enter the person's name. The result is printed in the terminal.

### Web search

```text
web
```

Runs a SerpAPI query for that name and prints the search summary.

### OpenAI agent

```text
agent
```

Sends the name to `gpt-4o-mini` with a prompt that asks for a helpful lookup and at least two interesting facts.

### Local agent

```text
local
```

Uses the same prompt against Ollama `gemma2:2b` on your machine. Ollama must be running and the model must already be pulled.

## Project layout

```text
lang_chain/
├── main.py          # CLI and the three lookup paths
├── pyproject.toml   # Python version and dependencies
├── uv.lock
└── .env             # API keys (local only, gitignored)
```

## Notes

Results come from public web data or from a language model's training knowledge. They can be incomplete or wrong, especially for common names. Treat anything you find as a lead, and confirm it before contacting someone.
