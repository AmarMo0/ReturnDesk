from datetime import date

from langgraph.types import Command

from agent.graph import build_graph


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "cli-1"}}

    while True:
        text = input("You: ").strip()
        if text.lower() in {"quit", "exit"}:
            break
        if not text:
            continue

        payload = {"messages": [("user", text)], "reported_on": date.today()}

        while True:
            result = graph.invoke(payload, config)
            if "__interrupt__" in result:
                print("Bot:", result["__interrupt__"][0].value)
                payload = Command(resume=input("You: "))
            else:
                print("Bot:", result["messages"][-1].content)
                break


if __name__ == "__main__":
    main()