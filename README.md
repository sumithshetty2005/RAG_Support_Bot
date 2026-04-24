# Customer Support RAG Assistant

An intelligent, AI-powered customer support assistant built using Retrieval-Augmented Generation (RAG) and LangGraph, designed to provide accurate, context-aware responses while ensuring reliability through Human-in-the-Loop (HITL) escalation.

## 🚀 Overview

Traditional rule-based chatbots are often brittle and struggle with the nuances of natural language [cite: 3, 4]. This project addresses those limitations by leveraging a large knowledge base of support scenarios to provide instant, grounded answers. When the system encounters complex, urgent, or low-confidence queries, it proactively triggers a Human-in-the-Loop (HITL) workflow to ensure high-quality support [cite: 5, 55, 124].

## 🏗️ Architecture

The system is built on three core layers [cite: 13]:

1.  **Data Ingestion Layer**: Parses PDF/CSV documents, chunks text using recursive splitting, and stores semantic embeddings in ChromaDB [cite: 16, 22, 63].
2.  **Orchestration Layer**: Utilizes a LangGraph state machine to manage complex, non-linear workflows (Retrieve → Route → Generate/Escalate) [cite: 44, 72].
3.  **Presentation Layer**: A responsive React web interface for real-time chat interactions and agent escalation management [cite: 16, 121].

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **LLM** | Llama-3.3-70b (via Groq API) |
| **Orchestration** | LangGraph |
| **Vector Database** | ChromaDB |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Backend** | FastAPI |
| **Frontend** | React (TypeScript) |

## ✨ Key Features

* **Context-Aware RAG**: Grounds responses in verified organizational data to minimize hallucinations [cite: 7, 107].
* **Stateful Orchestration**: Uses LangGraph to handle conditional branching and complex agentic workflows [cite: 72, 73].
* **Human-in-the-Loop (HITL)**: Proactively escalates edge cases to human agents based on confidence scores, keyword heuristics, or user intent [cite: 52, 56, 124].
* **Performance-Driven**: Optimized for sub-second inference latency using Groq's LPU infrastructure [cite: 41, 75].

## 📝 Learning Outcomes

* **Beyond the LLM**: Realized that a robust RAG system depends heavily on the quality of the retrieval pipeline, including chunking strategies and embedding models [cite: 139, 140, 141].
* **Workflow Orchestration**: Learned the value of LangGraph in implementing decision-based routing and feedback loops [cite: 142, 143].
* **Reliability & Trust**: Understood that in enterprise applications, knowing *when* to escalate to a human is just as critical as the automation itself [cite: 144, 145].

---
*Built as a final project for the Innomatics Research Labs internship.*
