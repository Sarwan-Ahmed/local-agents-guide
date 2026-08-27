"""Module 03's hand-rolled loop, rebuilt as an explicit LangGraph StateGraph.

Compare this file to module 03's tools_demo.py -- same mechanic, expressed as a graph.

Run: python 04-agents/graph_agent.py
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from tools import TOOLS

load_dotenv()


def build_graph():
    llm = ChatOpenAI(
        base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"),
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        api_key="not-needed",
        temperature=0,
    ).bind_tools(TOOLS)

    def call_model(state: MessagesState):
        return {"messages": [llm.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("call_model", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.set_entry_point("call_model")
    graph.add_conditional_edges("call_model", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "call_model")

    return graph.compile()


def main():
    app = build_graph()
    result = app.invoke(
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
