# AI Coding Agent

A small command-line coding agent for learning how tool-calling agents work. It reads a prompt, asks a model on [OpenRouter](https://openrouter.ai/) what to do next, and can list, read, write, and run Python inside a single working directory.

**This is a learning project.** It does not include the safeguards a production coding agent needs. Run it only on the included `calculator` sample, or on another directory you are willing to have overwritten and executed.

## What it does

`main.py` takes one prompt and talks to OpenRouter with the OpenAI Python SDK (`openrouter/free`). The model gets a system prompt that tells it to explore the working directory, change code, and run both the app and its tests.

Each model response is one step:

1. The model either calls tools or writes a final answer.
2. Tool calls are dispatched in `call_function.py`. The working directory is added in code. The model cannot choose it.
3. Tool results are appended to the conversation and the loop continues.

The loop stops when the model replies without calling a tool, or after 20 model calls.

The working directory is `./calculator` (`WORKING_DIR` in `config.py`). That folder is a small infix calculator (`+`, `-`, `*`, `/`) with operator precedence, a CLI in `calculator/main.py`, and unit tests in `calculator/tests.py`.

## Tools

| Tool | Purpose | Boundary in this project |
| --- | --- | --- |
| `get_files_info` | List a directory and report each entry's size and whether it is a directory | Path must stay inside the working directory |
| `get_file_content` | Read a file | Path must stay inside the working directory. Output is cut off at `MAX_CHARS` (10,000) |
| `write_file` | Create or overwrite a file, creating parent directories as needed | Path must stay inside the working directory. Writes the full contents in one shot |
| `run_python_file` | Run a `.py` file with optional arguments | Path must stay inside the working directory and must end in `.py`. The process times out after 30 seconds |

Path checks use `os.path.commonpath` against the working directory. They are a basic containment check for this exercise. They are not a sandbox.

## What this project leaves out

Use this list as a map of what a real agent would still need. The code here does not provide:

- A review step before a file is overwritten or Python is executed
- A sandbox. `run_python_file` runs `python` as the same user who started the agent, with that user's permissions, and passes the model's arguments through
- Secret redaction, output filtering, or handling for prompt injection in files the agent reads
- A fixed model. `openrouter/free` routes to whatever free model OpenRouter selects, so behavior can change between runs
- Protection for anything you point `WORKING_DIR` at. That constant is the entire scope of the tools

## Requirements

- Python 3.13 (`requires-python` in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/)
- An [OpenRouter](https://openrouter.ai/) API key

## Setup

```bash
git clone https://github.com/GreyNewfie/ai-coding-agent.git
cd ai-coding-agent
uv sync
```

Create a `.env` file in the repo root. `.gitignore` already excludes it.

```bash
OPENROUTER_API_KEY=your_key_here
```

## Usage

```bash
uv run python main.py "Show me how the calculator evaluates 3 * 4 + 5"
```

`--verbose` prints the prompt, token counts, tool arguments, and tool results.

```bash
uv run python main.py "Add a power operator and cover it with a test" --verbose
```

The agent prints each tool name as it runs, then prints the model's final answer. A run that never finishes inside 20 calls exits with status 1.

The scripts named `test_*.py` exercise the tools directly and print their results. They are not a unit-test suite.

```bash
uv run python test_get_files_info.py
uv run python test_get_file_content.py
uv run python test_write_file.py
uv run python test_run_python_file.py
```

Run the sample calculator on its own from the repo root:

```bash
uv run python calculator/main.py "3 + 5"
uv run python calculator/tests.py
```

## Layout

```text
main.py                  CLI, OpenRouter client, and the 20-step loop
prompts.py               System prompt
call_function.py         Tool schemas and dispatch
config.py                WORKING_DIR and MAX_CHARS
functions/               list, read, write, and run implementations
calculator/              Sample project the agent is allowed to touch
test_*.py                Manual checks for each tool
```
