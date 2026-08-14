"""Hand-rolled tool-calling loop: model requests a tool -> we run it -> model uses the result.

No framework yet -- this is the mechanic module 04 (Agents) will wrap in LangGraph.

Run: python 03-tool-use-function-calling/tools_demo.py
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SANDBOX_DIR = Path(__file__).parent

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current UTC date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file by name from the current module's folder.",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
        },
    },
]


def get_current_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def read_file(filename: str):
    path = (SANDBOX_DIR / filename).resolve()
    if SANDBOX_DIR.resolve() not in path.parents and path != SANDBOX_DIR.resolve():
        return "Error: can only read files inside this module's folder."
    if not path.is_file():
        return f"Error: {filename} not found."
    return path.read_text()


DISPATCH = {"get_current_time": get_current_time, "read_file": read_file}


def run_tool(name: str, arguments: dict):
    print(f"  -> running tool: {name}({arguments})")
    result = DISPATCH[name](**arguments)
    print(f"  <- tool result: {result!r}")
    return result


def main():
    client = OpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key="not-needed",
    )
    model = os.environ.get("LLM_MODEL", "llama3.2:3b")

    messages = [
        {
            "role": "user",
            "content": "Read sample_note.txt and tell me what it says, then tell me what time it is right now.",
        }
    ]

    while True:
        response = client.chat.completions.create(
            model=model, messages=messages, tools=TOOLS, temperature=0
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            print(f"\nFinal answer:\n{message.content}")
            break

        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            result = run_tool(call.function.name, arguments)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": str(result)}
            )


if __name__ == "__main__":
    main()
