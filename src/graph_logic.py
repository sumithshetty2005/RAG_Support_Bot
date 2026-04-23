from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from src.ingestion import IngestionPipeline
from src.llm_handler import LLMHandler, RAG_SYSTEM_PROMPT, ROUTING_PROMPT

class AgentState(TypedDict):
    query: str
    context: str
    response: str
    escalated: bool
    needs_confirmation: bool
    history: List[str]

class SupportGraph:
    def __init__(self):
        self.ingestion = IngestionPipeline()
        self.retriever = self.ingestion.get_retriever()
        self.llm = LLMHandler()
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def retrieve_node(self, state: AgentState):
        query = state["query"]
        docs = self.retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        return {"context": context}

    def router_node(self, state: AgentState):
        query = state["query"]
        context = state["context"]
        
        # Determine if we should answer or suggest escalation
        decision = self.llm.get_response(
            ROUTING_PROMPT.format(query=query, context=context), 
            "Respond only with ANSWER or ESCALATE."
        ).strip().upper()
        
        if "ESCALATE" in decision:
            return "suggest_escalate"
        return "generate"

    def generate_node(self, state: AgentState):
        query = state["query"]
        context = state["context"]
        response = self.llm.get_response(
            RAG_SYSTEM_PROMPT.format(context=context),
            query
        )
        return {"response": response, "escalated": False, "needs_confirmation": False}

    def suggest_escalate_node(self, state: AgentState):
        return {
            "response": "I'm having trouble finding the exact answer in our documentation. Would you like to speak with a human support agent for more specialized help?",
            "escalated": False,
            "needs_confirmation": True
        }

    def _build_graph(self):
        self.workflow.add_node("retrieve", self.retrieve_node)
        self.workflow.add_node("generate", self.generate_node)
        self.workflow.add_node("suggest_escalate", self.suggest_escalate_node)

        self.workflow.set_entry_point("retrieve")
        
        # Add conditional edges
        self.workflow.add_conditional_edges(
            "retrieve",
            self.router_node,
            {
                "generate": "generate",
                "suggest_escalate": "suggest_escalate"
            }
        )
        
        self.workflow.add_edge("generate", END)
        self.workflow.add_edge("suggest_escalate", END)

        self.app = self.workflow.compile()

    def run(self, query: str):
        initial_state = {
            "query": query,
            "context": "",
            "response": "",
            "escalated": False,
            "needs_confirmation": False,
            "history": []
        }
        return self.app.invoke(initial_state)

if __name__ == "__main__":
    graph = SupportGraph()
    result = graph.run("How do I cancel my order?")
    print(f"Response: {result['response']}")
    print(f"Escalated: {result['escalated']}")
