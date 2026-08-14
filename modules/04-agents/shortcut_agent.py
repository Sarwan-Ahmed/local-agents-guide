"""Same agent as graph_agent.py, built with the create_react_agent shortcut instead of a manual graph.

Run: python 04-agents/shortcut_agent.py
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import TOOLS

load_dotenv()


def main():
    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        api_key="not-needed",
        temperature=0,
    )
    agent = create_react_agent(llm, tools=TOOLS)

    result = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    "Read sample_note.txt and tell me what it says, then tell me what time it is right now.",
                )
            ]
        },
        config={"recursion_limit": 10},
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
