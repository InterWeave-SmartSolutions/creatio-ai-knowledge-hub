# InterWeave AI Server Setup Guide

## Overview

This guide provides comprehensive instructions for setting up an AI server to
support InterWeave SmartSolutions' AI-driven features including SmartFlows,
SmartAgents, FlowCopilot, and CRM/ERP/Payment integrations.

## 🔧 Base Operating System

### Recommended OS

- **Ubuntu Server 22.04 LTS** (or latest stable LTS version)
  - Lightweight, stable, and widely used for ML/AI workloads
  - Compatible with NVIDIA CUDA, Python, Docker, and Kubernetes
  - Long-term support ensures stability

### Installation Resources

- Download: https://ubuntu.com/download/server
- Installation Guide: https://ubuntu.com/tutorials/install-ubuntu-server

## 📦 System Dependencies

### Essential Build Tools

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential python3-dev python3-pip python3-venv
sudo apt install -y git curl wget unzip
sudo apt install -y libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
```

## 🧠 AI/ML Frameworks & Libraries

### Core Python Environment

- **Python 3.10+** (required)
- **Virtual Environment Setup**:

```bash
python3 -m venv ai_server_env
source ai_server_env/bin/activate
```

### AI/ML Frameworks

1. **PyTorch** (preferred for LLaMA, BERT, Whisper models)
   - Installation: `pip install torch torchvision torchaudio`
   - Documentation: https://pytorch.org/get-started/locally/

2. **TensorFlow** (for TensorFlow/Keras models)
   - Installation: `pip install tensorflow`
   - Documentation: https://www.tensorflow.org/install

3. **Hugging Face Transformers** (model orchestration)
   - Installation: `pip install transformers`
   - Documentation: https://huggingface.co/docs/transformers

4. **LangChain** (prompt orchestration and RAG)
   - Installation: `pip install langchain`
   - Documentation: https://python.langchain.com/docs/get_started

5. **Additional Libraries**:

```bash
pip install spacy scikit-learn xgboost pandas numpy
pip install fastapi uvicorn redis-py psycopg2-binary
```

## 🔄 Integration Services

### API Server Options

1. **FastAPI** (recommended)
   - Installation: `pip install fastapi uvicorn`
   - Documentation: https://fastapi.tiangolo.com/

2. **Flask** (alternative)
   - Installation: `pip install flask`
   - Documentation: https://flask.palletsprojects.com/

### Database Solutions

1. **PostgreSQL**
   - Installation: `sudo apt install postgresql postgresql-contrib`
   - Setup Guide: https://www.postgresql.org/docs/current/tutorial-start.html

2. **MongoDB** (alternative)
   - Installation Guide:
     https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

3. **Redis** (caching/session management)
   - Installation: `sudo apt install redis-server`
   - Documentation: https://redis.io/docs/getting-started/

## 📚 Vector Database Solutions

### Option 1: FAISS (Free, Local)

- **Best for**: Budget-conscious deployments
- Installation: `pip install faiss-cpu` (or `faiss-gpu` for GPU acceleration)
- Documentation: https://github.com/facebookresearch/faiss

### Option 2: Weaviate

- **Self-hosted**: Free
- **Cloud**: Starts ~$20/month
- Installation: https://weaviate.io/developers/weaviate/installation
- Documentation: https://weaviate.io/developers/weaviate

### Option 3: Pinecone

- **Cloud-only**: Starts free, scales to $500+/month
- Setup: https://www.pinecone.io/
- Documentation: https://docs.pinecone.io/

### Option 4: ChromaDB

- **Free, Local**
- Installation: `pip install chromadb`
- Documentation: https://docs.trychroma.com/

## 🧰 DevOps & Orchestration

### Docker Setup

```bash
# Install Docker
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

### NGINX (Reverse Proxy)

```bash
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Kubernetes (Optional)

- For larger deployments or multi-tenant AI workloads
- Installation Guide: https://kubernetes.io/docs/setup/

## ⚙️ Model Hosting Solutions

### Option 1: Ollama (Recommended for Local LLMs)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run a model
ollama run mistral
ollama run llama2
ollama run codellama
```

- **Benefits**: Free, local, no token costs
- **Documentation**: https://ollama.ai/

### Option 2: Hugging Face Text Generation Inference (TGI)

- **Installation**: Via Docker
- **Documentation**: https://github.com/huggingface/text-generation-inference

### Option 3: vLLM

- **Installation**: `pip install vllm`
- **Documentation**: https://vllm.readthedocs.io/

### Option 4: llama.cpp

- **Installation**: https://github.com/ggerganov/llama.cpp
- **Benefits**: Lightweight, CPU-optimized

## 🔐 Security & Access Control

### SSL Certificates

- **Let's Encrypt**: Free SSL certificates
- **Setup**: `sudo certbot --nginx`

### Authentication

- **OAuth 2.0**: Industry standard
- **JWT**: For stateless authentication
- **Implementation**: FastAPI supports both natively

### Server Hardening

```bash
# Install fail2ban for intrusion prevention
sudo apt install fail2ban

# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

## 🛠️ Optional Monitoring & Add-ons

### Monitoring Stack

1. **Grafana + Prometheus**
   - Installation: https://grafana.com/docs/grafana/latest/installation/
   - Free, comprehensive monitoring

2. **ELK Stack** (Elasticsearch, Logstash, Kibana)
   - For advanced logging and analytics
   - Installation: https://www.elastic.co/guide/index.html

### Development Tools

- **JupyterLab**: `pip install jupyterlab`
- **VS Code Server**: Remote development capability

## 💰 Cost Analysis

### Self-Hosted Stack (Recommended)

| Category       | Software/Tools                    | Monthly Cost     |
| -------------- | --------------------------------- | ---------------- |
| OS & Base      | Ubuntu Server, Python, etc.       | $0               |
| AI Frameworks  | PyTorch, TensorFlow, Transformers | $0               |
| Vector DB      | FAISS, ChromaDB                   | $0               |
| API & Database | FastAPI, PostgreSQL, Redis        | $0               |
| Model Hosting  | Ollama, llama.cpp                 | $0               |
| Security       | Let's Encrypt, UFW, Fail2Ban      | $0               |
| **Total**      | **All Self-Hosted**               | **$0-$20/month** |

### Cloud/Hybrid Options

| Service    | Provider          | Cost Range       |
| ---------- | ----------------- | ---------------- |
| Vector DB  | Pinecone          | $0-$500+/month   |
| Vector DB  | Weaviate Cloud    | $20+/month       |
| LLM APIs   | OpenAI, Anthropic | $20-$1000+/month |
| Database   | MongoDB Atlas     | $0-$50/month     |
| Monitoring | Elastic Cloud     | $0-$100+/month   |

## 🖥️ Hardware Requirements

### Minimum Requirements

- **CPU**: 4-core x86_64
- **RAM**: 16 GB
- **Storage**: 200 GB SSD
- **GPU**: Optional for smaller models

### Recommended for LLMs

- **CPU**: 8+ cores
- **RAM**: 32-64 GB
- **Storage**: NVMe SSD (500 GB+)
- **GPU**: NVIDIA RTX 3090/4090 (for 7B-13B LLMs)

## 🔁 Architecture Overview

```
[Clients: CRM / ERP / Web Apps]
              ↕
         [NGINX Proxy]
              ↕
         [FastAPI Server]
              ↕
    +------------------------+
    | Vector DB (FAISS)      |
    | Ollama LLMs (Mistral)  |
    | LangChain Agents/RAG   |
    +------------------------+
              ↕
    [PostgreSQL / Redis / Local Data]
```

## 📦 Docker Deployment Example

### Sample docker-compose.yml

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - '8000:8000'
    depends_on:
      - redis
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aidb
      - REDIS_URL=redis://redis:6379

  redis:
    image: redis:alpine
    ports:
      - '6379:6379'

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: aidb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  nginx:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt

volumes:
  postgres_data:
```

## 🚀 Quick Start Guide

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git docker.io nginx

# Create virtual environment
python3 -m venv ai_env
source ai_env/bin/activate
```

### 2. Install AI Stack

```bash
# Install core AI libraries
pip install torch transformers langchain fastapi uvicorn
pip install faiss-cpu redis-py psycopg2-binary

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Download Models

```bash
# Pull LLM models
ollama pull mistral
ollama pull llama2
```

### 4. Setup Security

```bash
# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# Install SSL
sudo apt install certbot python3-certbot-nginx
```

## 📋 Deployment Checklist

### Pre-deployment

- [ ] Server provisioned with adequate resources
- [ ] Ubuntu Server 22.04 LTS installed
- [ ] SSH access configured
- [ ] Domain name configured (if using SSL)

### Core Installation

- [ ] System dependencies installed
- [ ] Python 3.10+ with virtual environment
- [ ] Docker and Docker Compose installed
- [ ] NGINX installed and configured

### AI Stack

- [ ] PyTorch/TensorFlow installed
- [ ] Transformers and LangChain installed
- [ ] Vector database configured (FAISS/Weaviate/etc.)
- [ ] Ollama installed with models downloaded

### Security

- [ ] Firewall configured (UFW)
- [ ] SSL certificates installed (Let's Encrypt)
- [ ] Fail2Ban configured
- [ ] Authentication system implemented

### Integration

- [ ] FastAPI server configured
- [ ] Database connections tested
- [ ] Redis caching operational
- [ ] API endpoints functional

### Monitoring (Optional)

- [ ] Grafana/Prometheus configured
- [ ] Log aggregation setup
- [ ] Health check endpoints created

## 🆘 Troubleshooting & Support

### Common Issues

1. **CUDA/GPU Issues**: Ensure NVIDIA drivers are properly installed
2. **Memory Issues**: Monitor RAM usage, consider model quantization
3. **Network Issues**: Check firewall rules and port configurations
4. **Performance Issues**: Profile CPU/memory usage, optimize models

### Useful Commands

```bash
# Check system resources
htop
nvidia-smi  # For GPU systems
df -h       # Disk usage
free -h     # Memory usage

# Check services
sudo systemctl status nginx
sudo systemctl status docker
docker ps   # Running containers

# View logs
sudo journalctl -u nginx
docker logs <container_name>
```

### Documentation Links

- **Ollama**: https://ollama.ai/
- **LangChain**: https://python.langchain.com/docs/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker**: https://docs.docker.com/
- **Ubuntu Server**: https://ubuntu.com/server/docs

## 🎯 Next Steps

Once your AI server is deployed, consider:

1. **Model Fine-tuning**: Customize models for your specific use cases
2. **API Integration**: Connect to your CRM/ERP systems
3. **Scaling**: Implement load balancing and horizontal scaling
4. **Monitoring**: Set up comprehensive observability
5. **Backup Strategy**: Implement data backup and disaster recovery

---

_This guide provides a comprehensive foundation for setting up your InterWeave
AI Server. Adjust configurations based on your specific requirements and scale._
