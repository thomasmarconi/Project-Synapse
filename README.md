# 🧠 Project Synapse

**AI-powered platform for extracting, tagging, and mapping organizational knowledge from Microsoft 365 into a semantic knowledge graph.**

## ✨ Overview

This project connects to a Microsoft 365 tenant and automatically:

- 🔍 Ingests content and metadata from **SharePoint**, **OneDrive**, and **Teams**
- 🧠 Uses **LLMs** to classify and semantically tag files, messages, and workflows
- 🕸️ Builds a dynamic **ONgDB knowledge graph** linking people, documents, teams, and topics
- 💬 Enables **semantic search** and visual exploration of your organization’s knowledge structure

---

## 🧱 Tech Stack

| Layer        | Technology |
|--------------|------------|
| Backend API  | FastAPI (Python) |
| Frontend     | Next.js + TypeScript |
| AI/NLP       | OpenAI + spaCy |
| Graph DB     | Neo4j Community |
| Vector DB    | Milvus or Chroma TBD |
| M365 Data    | Microsoft Graph API |
| Auth         | Azure AD OAuth2 |
| Cloud Infra  | Azure (Functions, Blob Storage, CosmosDB) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/m365-ontology-mapper.git
cd m365-ontology-mapper
```

### 2. Set Up Environment Variables
Copy the example environment file and configure it:

```bash
cp .env.example .env
```
Fill in:

- Azure client ID, secret, tenant ID
- OpenAI API key

### 3. Start Services (Dev Mode) -- Not implemented yet
You can run the backend, frontend, and Neo4j using Docker Compose:

```bash
docker-compose up --build
```
Frontend will be at http://localhost:3000, and API at http://localhost:8000.

## ⚙️ Project Structure
```graphql
prroject-synapse/
│
├── backend/         # FastAPI backend for API + ingestion
├── frontend/        # Next.js frontend UI
├── graph-db/        # Neo4j queries and ontology schema
├── embeddings/      # Embedding + vector DB logic
├── infra/           # IaC (Terraform or ARM for Azure setup)
├── scripts/         # CLI tools for dev or ingestion
├── docker-compose.yml
└── .env.example
```
## 🧭 Roadmap
- [ ] M365 OAuth2 integration and Graph API file access
- [ ] LLM-powered file embedding + tagging
- [ ] Neo4j entity/workflow mapping
- [ ] Semantic search interface
- [ ] Multi-tenant support
- [ ] Live data change tracking (webhooks or polling)
- [ ] Graph-based insights + alerts
