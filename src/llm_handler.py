import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class LLMHandler:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name=model_name,
            temperature=0.3
        )
        
    def get_response(self, system_prompt: str, user_query: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}")
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"query": user_query})

RAG_SYSTEM_PROMPT = """You are a helpful Customer Support Assistant. 
Use the following pieces of retrieved context to answer the user's question.

### Formatting Guidelines:
- Use **proper Markdown** for your response.
- Present lists or steps as **bullet points** or **numbered lists**.
- Use **bold text** for important terms or actions.
- Add **line breaks** between paragraphs to ensure readability.
- If the answer is not in the context, clearly state that you don't have that information and suggest escalating to a human agent.
- Do not make up facts.

Context:
{context}
"""

ROUTING_PROMPT = """Analyze the following user query and the retrieved context. 
Determine if the assistant can answer the query accurately or if it needs to be escalated to a human.
Output only 'ANSWER' or 'ESCALATE'.

Criteria for ESCALATE:
- The context does not contain enough information to answer.
- The user explicitly asks for a human.
- The query is too complex or involves sensitive personal data not covered in docs.

Query: {query}
Context: {context}

Result:"""

if __name__ == "__main__":
    handler = LLMHandler()
    print(handler.get_response("You are a helpful assistant.", "Hello!"))
