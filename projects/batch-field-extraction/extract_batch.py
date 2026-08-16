"""Extracts the fields defined in schema.py from every .txt file in INPUT_DIR,
writing one row per file to OUTPUT_FILE. Generalizes module 02's single-note
extract.py into a batch pipeline that keeps going if one file fails.

Run: python extract_batch.py
"""

import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from schema import CustomerRecord

load_dotenv()

INPUT_DIR = Path(os.environ.get("INPUT_DIR", "input_docs"))
OUTPUT_FILE = Path(os.environ.get("OUTPUT_FILE", "output/extracted.csv"))

FIELD_TEMPLATE = json.dumps({name: "<value or null>" for name in CustomerRecord.model_fields}, indent=2)

SYSTEM_PROMPT = f"""You extract structured fields from a customer record.
Always reply with a single JSON object with exactly these keys, replacing each
placeholder with the actual value found in the text:
{FIELD_TEMPLATE}
Use null for any field not present in the text. Do not invent values that aren't there."""


def extract_one(client: OpenAI, model: str, text: str) -> CustomerRecord:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]

    for attempt in range(2):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
        )
        raw = response.choices[0].message.content
        try:
            return CustomerRecord.model_validate(json.loads(raw))
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

    files = sorted(INPUT_DIR.glob("*.txt"))
    if not files:
        print(f"No .txt files found in {INPUT_DIR}")
        return

    rows = []
    failures = []
    for path in files:
        try:
            record = extract_one(client, model, path.read_text())
            rows.append({"source_file": path.name, **record.model_dump()})
            print(f"OK    {path.name}")
        except Exception as e:
            failures.append((path.name, str(e)))
            print(f"FAIL  {path.name}: {e}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["source_file", *CustomerRecord.model_fields.keys()]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{len(rows)}/{len(files)} extracted -> {OUTPUT_FILE}")
    if failures:
        print(f"{len(failures)} failed after retry: {[name for name, _ in failures]}")


if __name__ == "__main__":
    main()
