import os
import pandas as pd
from typing import List
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class IngestionPipeline:
    def __init__(self, db_dir: str = r"C:\Users\user\OneDrive\Desktop\Cutomer Support RAG\index", collection_name: str = "customer_support"):
        self.db_dir = db_dir
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def load_pdf(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load_and_split(self.text_splitter)

    def load_csv(self, file_path: str, sample_size: int = 5000) -> List[Document]:
        """
        Loads the customer support CSV. 
        Maps 'instruction' as context and 'response' as content.
        """
        df = pd.read_csv(file_path)
        if sample_size and sample_size < len(df):
            df = df.sample(sample_size, random_state=42)
        
        documents = []
        for _, row in df.iterrows():
            content = f"Instruction: {row['instruction']}\nResponse: {row['response']}"
            metadata = {
                "category": row.get('category', 'N/A'),
                "intent": row.get('intent', 'N/A'),
                "source": "csv_dataset"
            }
            documents.append(Document(page_content=content, metadata=metadata))
        return documents

    def ingest(self, data_sources: List[str]):
        all_docs = []
        for source in data_sources:
            if source.endswith(".pdf"):
                all_docs.extend(self.load_pdf(source))
            elif source.endswith(".csv"):
                all_docs.extend(self.load_csv(source))
        
        if not all_docs:
            print("No documents found to ingest.")
            return

        print(f"Ingesting {len(all_docs)} chunks into ChromaDB at '{self.db_dir}'...")
        
        # Batch ingestion to handle large datasets
        batch_size = 500
        vectorstore = None
        
        for i in range(0, len(all_docs), batch_size):
            batch = all_docs[i:i + batch_size]
            if vectorstore is None:
                vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=self.embeddings,
                    persist_directory=self.db_dir,
                    collection_name=self.collection_name
                )
            else:
                vectorstore.add_documents(batch)
            print(f"Progress: {min(i + batch_size, len(all_docs))}/{len(all_docs)} ingested...")
            
        print("Ingestion complete.")
        return vectorstore

    def get_retriever(self):
        vectorstore = Chroma(
            persist_directory=self.db_dir,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        return vectorstore.as_retriever(search_kwargs={"k": 3})

if __name__ == "__main__":
    # Test ingestion
    pipeline = IngestionPipeline()
    csv_path = r"C:\Users\user\OneDrive\Desktop\Cutomer Support RAG\Customer_Support_Training_Dataset.csv"
    if os.path.exists(csv_path):
        pipeline.ingest([csv_path])
    else:
        print(f"CSV not found at {csv_path}")
