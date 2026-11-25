
from datetime import date

from langgraph.types import Command

from agent.graph import build_graph
from agent.case import init_db, get_existing_case


def main() -> None:
    init_db()
    graph = build_graph()
    config = {"configurable": {"thread_id": "cli-1"}}

    while True:
        text = input("You: ").strip()

        if text.lower() in {"quit", "exit"}:
            break

        if not text:
            continue

        payload = {
            "messages": [("user", text)],
            "reported_on": date.today()
        }

        approved_case = False
        declined_case = False

        while True:
            result = graph.invoke(payload, config=config)

            if "__interrupt__" in result:
                print("Bot:", result["__interrupt__"][0].value)

                answer = input("You (yes/no): ").strip().lower()

                if answer in {"yes", "y"}:
                    payload = Command(resume=True)
                    approved_case = True

                elif answer in {"no", "n"}:
                    payload = Command(resume=False)
                    declined_case = True

                else:
                    print("Please answer yes or no.")
                    continue

            else:
                if approved_case:
                    saved_case = get_existing_case(
                        result["order_id"],
                        result["request_type"]
                    )

                    if saved_case:
                        print(result["messages"][-1].content)
                        print(
                            f"Verified: Case #{saved_case['case_id']} "
                            "exists in database."
                        )
                        print("Chat ended.")
                        return

                    print("Error: Case was not found in database.")

                elif declined_case:
                    print("Bot: Understood. No case was opened.")

                else:
                    print("Bot:", result["messages"][-1].content)

                break


if __name__ == "__main__":
    main()
