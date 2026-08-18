"""CLI chat loop. Run `python ingest.py` once first, then `python main.py`."""

from dotenv import load_dotenv

from agent import build_agent

load_dotenv()


def main():
    print("Loading agent... (first run may be slow while the model warms up)")
    agent = build_agent()
    print("Ready. Ask about your files, or ask it to extract fields into a CSV (Ctrl+D to quit).\n")

    # Keeping the growing message list across turns is what lets a follow-up like
    # "whatever you find, no specific format" make sense to the agent -- without
    # this, each turn starts a brand new conversation with no memory of the last.
    messages = []

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue

        messages.append({"role": "user", "content": question})
        result = agent.invoke({"messages": messages}, config={"recursion_limit": 15})
        messages = result["messages"]
        print(f"\n{messages[-1].content}\n")


if __name__ == "__main__":
    main()
