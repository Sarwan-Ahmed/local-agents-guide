"""CLI chat loop. Run `python ingest.py` once first, then `python main.py`."""

from dotenv import load_dotenv

from agent import ask, build_agent

load_dotenv()


def main():
    print("Loading agent... (first run may be slow while the model warms up)")
    agent = build_agent()
    print("Ready. Ask about your files, or ask it to extract fields into a CSV (Ctrl+D to quit).\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue

        answer = ask(agent, question)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()
