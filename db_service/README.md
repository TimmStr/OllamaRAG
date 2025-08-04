# 🛢️ Central Database Service (TimescaleDB)

This project provides a lightweight **centralized database service** built on **TimescaleDB** (a high-performance time-series extension for PostgreSQL).  
It is designed to store data efficiently and make it easily accessible to other internal services.

---

## 🚀 **Features**

✅ **High-performance storage**  
- Uses TimescaleDB to store and query large volumes of time-series and structured data efficiently

✅ **Central data hub**  
- Acts as the single source of truth for multiple microservices

✅ **REST API**  
- Exposes simple HTTP endpoints to insert, query, and manage data

---

## 📌 **API Documentation**

Interactive documentation is available at:

http://localhost:8001/docs


Explore endpoints, test requests, and see response schemas.

---

## ⚙️ **Installation & Usage**

```bash
# Clone the repository
git clone https://github.com/TimmStr/OllamaRAG

# Create a docker container
docker compose build db-service
docker compose up -d db-service