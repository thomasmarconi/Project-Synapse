# 🚀 Project Synapse - Backend API

This is the FastAPI backend service for Project Synapse, providing REST API endpoints for the AI-powered knowledge graph platform.

## 📋 Overview

The backend API handles:

- 🔗 Microsoft 365 integration via Graph API
- 🧠 AI-powered content processing and semantic tagging
- 📊 Knowledge graph data management
- 🔍 Semantic search capabilities
- 🔐 Authentication and authorization

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.13+)
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Environment Management**: python-dotenv
- **Development Server**: Uvicorn with hot reload
- **Validation**: Pydantic models

## 🚀 Quick Start

### 1. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Configure the following environment variables:

```env
# API Configuration
API_HOST=localhost
API_PORT=8000
DEBUG=true

# Microsoft 365 / Azure AD
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_TENANT_ID=your_tenant_id

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 4. Run the Development Server

```bash
# Start the FastAPI development server with hot reload
fastapi dev main.py

# Alternative using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── app/
│   ├── __init__.py
│   ├── api/            # API route handlers
│   ├── core/           # Core functionality and config
│   ├── models/         # Pydantic models
│   ├── services/       # Business logic services
│   └── utils/          # Utility functions
├── tests/              # Unit and integration tests
└── docs/               # Additional documentation
```

## 🔧 Development

### Code Quality

This project uses:

- **Type Hints**: Full type annotation support
- **Pydantic**: Data validation and serialization
- **FastAPI**: Automatic API documentation

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🐳 Docker Support

Build and run using Docker:

```bash
# Build the Docker image
docker build -t project-synapse-backend .

# Run the container
docker run -p 8000:8000 project-synapse-backend
```

Or use Docker Compose from the project root:

```bash
docker-compose up backend
```

## 📚 API Endpoints

| Method | Endpoint           | Description                      |
| ------ | ------------------ | -------------------------------- |
| GET    | `/`                | Health check and API information |
| GET    | `/docs`            | Interactive API documentation    |
| POST   | `/auth/login`      | User authentication              |
| GET    | `/graph/nodes`     | Retrieve knowledge graph nodes   |
| POST   | `/search/semantic` | Semantic search across content   |
| GET    | `/m365/files`      | List Microsoft 365 files         |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
