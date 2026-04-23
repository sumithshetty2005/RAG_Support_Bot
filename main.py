import os
import argparse
from src.ingestion import IngestionPipeline
from src.graph_logic import SupportGraph

def main():
    parser = argparse.ArgumentParser(description="RAG-Based Customer Support Assistant with HITL")
    parser.add_argument("--ingest", action="store_true", help="Run the ingestion pipeline")
    parser.add_argument("--query", type=str, help="Single query to process")
    args = parser.parse_args()

    pipeline = IngestionPipeline()
    
    # Run ingestion if requested or if index is empty
    if args.ingest or not os.path.exists("index"):
        print("Initializing Knowledge Base...")
        csv_path = "Customer_Support_Training_Dataset.csv"
        if os.path.exists(csv_path):
            pipeline.ingest([csv_path])
        else:
            print(f"Error: Knowledge base {csv_path} not found.")
            return

    graph = SupportGraph()

    if args.query:
        process_query(graph, args.query)
    else:
        print("\n=== Customer Support Assistant (Type 'exit' to quit) ===")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            process_query(graph, user_input)

def process_query(graph, query):
    result = graph.run(query)
    
    if result.get("escalated"):
        print("\n--- SYSTEM: Escalation Triggered (HITL Mode) ---")
        print(f"Query: {query}")
        print("Retrieved Context was insufficient.")
        human_response = input("Human Agent, please provide the answer: ")
        print(f"\nAssistant (Filtered): {human_response}")
    else:
        print(f"\nAssistant: {result['response']}")

if __name__ == "__main__":
    main()
