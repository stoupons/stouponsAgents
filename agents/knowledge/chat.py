"""Chat with the Knowledge Agent in your terminal.

    python -m agents.knowledge.chat
"""
from agents.knowledge.agent import KnowledgeAgent


def main():
    agent = KnowledgeAgent()
    print("Stoupons Knowledge Assistant. Type 'quit' to exit.\n")
    total_cost = 0.0
    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if not question:
            continue
        result = agent.ask(question)
        total_cost += result.cost_usd
        print(f"\nAssistant: {result.answer}")
        print(f"   [status={result.status}  sources={result.citations or '-'}  "
              f"cost=${result.cost_usd:.4f}  txn={result.transaction_id}]\n")
    print(f"Session cost: ${total_cost:.4f}")


if __name__ == "__main__":
    main()
