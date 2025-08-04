# 🧠 LLM Service with FAISS Indexing, Data Analysis & Automated Emails

This project provides a RESTful service that integrates with a Large Language Model (LLM) to deliver powerful AI-driven
functionality for your applications.

Key features include:

- Creating and managing **FAISS indices** to support retrieval-augmented generation (RAG) systems
- Analyzing **CSV** and **XLSX** files with **natural language queries**
- Sending **automatic emails** based on LLM-generated content or custom logic

---

## 🚀 **Features**

✅ **RAG-ready indexing**

- Create FAISS indices from your documents
- Enable semantic search and retrieval to improve LLM context and answer quality

✅ **Natural language data analysis**

- Upload CSV or XLSX files
- Ask complex questions in plain English
- Get summaries, insights, and statistics powered by an LLM

✅ **Automated email sending**

- Generate professional emails automatically
- Connect to your email infrastructure to dispatch messages

---

## 📌 **API Documentation**

Interactive API documentation is available at:

http://localhost:8002/docs

Explore the available endpoints, test them, and see example requests/responses.

---

## ⚙️ **Installation & Usage**

```bash
# Clone the repository
git clone https://github.com/TimmStr/OllamaRAG

# Create a docker container
docker compose build llm-service
docker compose up -d llm-service

