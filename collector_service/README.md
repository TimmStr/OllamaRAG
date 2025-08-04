# 📚 AI Paper Collector Service

This project is a lightweight **collector service** that automatically pulls the 100 most influential AI research
papers, stores them in a **high-performance TimescaleDB**, and makes them available to other services — such as a **retrieval-augmented generation (RAG) system**.

---

## 🚀 **Features**

✅ **Automated paper collection**

- Periodically fetches metadata and abstracts of the top 100 influential AI papers from selected sources

✅ **Central storage**

- Saves all data in TimescaleDB to support fast queries and historical tracking

✅ **RAG-ready data**

- Designed to provide relevant paper content and embeddings to power a retrieval-augmented generation system

---

## 📌 **API Documentation**

Interactive API docs are available at:

http://localhost:8000/docs

Use this to test endpoints and see how to trigger collection, query papers, or manage stored data.

---

## ⚙️ **Installation & Usage**

```bash
# Clone the repository
git clone https://github.com/TimmStr/OllamaRAG

# Create a docker container
docker compose build collector-service
docker compose up -d collector-service