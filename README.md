# OllamaRAG# 🧠 AI Knowledge Platform – Modular RAG System with TimescaleDB, LLM, and Automation

This project is a modular AI-powered platform that integrates data collection, semantic search (RAG), automated
reporting, and high-performance storage — all orchestrated via Docker Compose.

It is built around four core microservices, a full observability stack, and a conversational UI for interacting with the
system.

---
# Demo Videos

This repository features two short demo videos:
1. **Excel AI Agent** – Demonstrating an AI-powered agent working directly inside Excel for intelligent data processing and automation.

[Excel Agent Demo.webm](https://github.com/user-attachments/assets/3dc6db4f-c400-4743-8b44-7165d03bac44)

3. **LLM WebUI Text Query** – Showcasing how to send a text request to a large language model through the web-based user interface.

[E-Mail Demo.webm](https://github.com/user-attachments/assets/cdd94cd8-44da-484b-bc82-a3c1b85ad831)


## 🧩 Services Overview

### 1. **collector_service**

🔎 *"Curate the knowledge."*  
Retrieves the 100 most influential AI papers, preprocesses them for downstream analysis, and feeds them into a RAG
pipeline. This service continuously collects new data to keep your system current.

### 2. **reporting_service** 

🧾 *"Turn data into action."*  
Generates automated reports and insights using LLMs. Supports email generation and dispatch for alerting, summaries, or
analytics delivery.

### 3. **db_service**

🗄️ *"Centralized, high-performance data storage."*  
Manages all data via a TimescaleDB instance, optimized for both structured and time-series workloads. Acts as the
backend for all other services.

### 4. **llm_service**

🤖 *"Conversational AI meets structured data."*  
A multi-purpose LLM interface that:

- Powers semantic search and retrieval through FAISS indices (RAG)
- Answers questions based on documents, files, or embedded content
- Analyzes `.csv` and `.xlsx` files using natural language
- Composes and sends professional emails

---

## 🛠 Infrastructure Stack

- **TimescaleDB** – High-performance time-series DB
- **Grafana** – Monitoring and dashboarding
- **EFK Stack** (Elasticsearch, Fluentd, Kibana) – Logging and observability
- **OpenWebUI** – Frontend interface for LLM interaction
- **Ollama** – Local LLM model provider
- **Docker Compose** – All services and components are containerized and orchestrated together

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose installed
- ~16GB+ RAM recommended for local LLM inference (Ollama)

### Start the stack

```bash
docker compose build
docker compose up -d

```

### Access points

| Component          | URL                          |
|--------------------|------------------------------|
| Collector-service  | `http://localhost:8000/docs` |
| DB-service         | `http://localhost:8001/docs` |
| LLM-service        | `http://localhost:8002/docs` |
| Reporting-service  | `http://localhost:8003/docs` |
| OpenWebUI (LLM UI) | `http://localhost:3000`      |
| Grafana            | `http://localhost:3000`      |
| Kibana             | `http://localhost:5601`      |
| Timescaledb (PG)   | `http://localhost:5432`      |
| Ollama             | `http://localhost:11434`     |
| Elasticsearch      | `http://localhost:9200`      |
| Fluentd            | `http://localhost:24224`     |
| Kibana             | `http://localhost:5601`      |

🧪 Example Use Cases

    Ask the system:
        "What are the key ideas in the most cited AI papers from last year?"

    Upload a spreadsheet and ask:
        "Which product had the highest profit margin over time?"

    Let the system send a report email automatically:
        "Weekly model drift summary and recommendations"

    Search your RAG database with natural questions like:
        "What methods does the AlphaFold paper use for protein folding?"
