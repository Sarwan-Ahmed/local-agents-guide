"""Extracts structured fields from free text using JSON mode + Pydantic validation.

Run: python 02-prompting-and-structured-output/extract.py
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()

SAMPLE_NOTE = """
Quick note from today's standup (March 3rd): we need to migrate the billing
service off the old queue before the Q2 freeze. Priya's picking it up, tagging
this as backend and urgent.
"""

SYSTEM_PROMPT = """You extract structured fields from short notes.
Always reply with a single JSON object matching exactly this shape:
{"title": "<short title, under 8 words>", "date": "<date mentioned, or null>", "tags": ["<tag1>", "<tag2>"]}

Example:
Note: "Reminder to renew the office lease by April 1st, tag as admin and urgent."
Output: {"title": "Renew office lease", "date": "April 1st", "tags": ["admin", "urgent"]}
"""


class NoteFields(BaseModel):
    title: str
    date: str | None
    tags: list[str]


def extract(client: OpenAI, model: str, note: str) -> NoteFields:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": note},
    ]

    for attempt in range(2):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        try:
            return NoteFields.model_validate(json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 0:
                messages.append({"role": "assistant", "content": raw})
                messages.append(
                    {"role": "user", "content": f"That didn't match the required shape ({e}). Try again."}
                )
                continue
            raise


def main():
    client = OpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key="not-needed",
    )
    model = os.environ.get("LLM_MODEL", "llama3.2:3b")

    fields = extract(client, model, SAMPLE_NOTE)
    print(fields.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
