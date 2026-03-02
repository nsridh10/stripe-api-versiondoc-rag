# End-to-End AWS EC2 Deployment Guide

## Stripe RAG Agent (FastAPI + LangGraph) + Frontend (Vite + React)

---

## Architecture Overview

```
Internet
   │
   ▼ :80
[EC2 – t3.small (2 vCPU / 2 GB RAM)]
 ┌─────────────────────────────────┐
 │  Docker network: rag-net        │
 │                                 │
 │  ┌──────────────────────────┐   │
 │  │  nginx (frontend)  :80   │   │  ← only this port is open to internet
 │  │  serves static React app │   │
 │  │  proxies /query          │   │
 │  │         /sessions        │   │
 │  │         /session/*       │   │
 │  │         /ingest   ──────────────► backend:8000 (internal only)
 │  └──────────────────────────┘   │
 │                                 │
 │  ┌──────────────────────────┐   │
 │  │  FastAPI backend   :8000 │   │  ← NOT exposed externally
 │  │  ChromaDB (in container) │   │
 │  │  HF embeddings (local)   │   │
 │  └──────────────────────────┘   │
 └─────────────────────────────────┘
```

**No port config changes needed** – the frontend makes same-origin requests (`/query`, `/sessions`, etc.) and nginx proxies them to the backend container over the Docker internal network. Both containers are on the same EC2 instance.

---

## Dependencies Packaged in Docker

| Dependency                             | Where            | Notes                              |
| -------------------------------------- | ---------------- | ---------------------------------- |
| FastAPI + uvicorn                      | backend image    | via requirements.txt               |
| LangGraph / LangChain                  | backend image    | via requirements.txt               |
| ChromaDB (langchain-chroma)            | backend image    | via requirements.txt               |
| **Pre-built vector store**             | backend image    | `data/chroma_db/` copied in        |
| **Raw Stripe docs**                    | backend image    | `data/raw/*.rst/*.md` copied in    |
| HuggingFace BAAI/bge-small-en-v1.5     | backend image    | downloaded at build time           |
| pandoc                                 | backend image    | system apt package for pypandoc    |
| LLM API keys (groq/gemini/openai/grok) | **runtime only** | provided by browser UI per-request |
| React + nginx                          | frontend image   | built at Docker build time         |

---

## Step 1 – AWS Account & EC2 Instance

### 1.1 Log in to AWS Console

Go to https://console.aws.amazon.com and sign in.

### 1.2 Launch EC2

> **Cost note**: t3.small is **not** free tier. It costs ~$0.023/hr ≈ **$17/month**.
> If cost is a hard constraint you can use t2.micro (free for 12 months) but expect
> sluggish responses and mandatory swap usage.

1. **EC2 → Instances → Launch instances**
2. **Name**: `stripe-rag-app`
3. **AMI**: Ubuntu Server 22.04 LTS
4. **Instance type**: `t3.small` (2 vCPU / 2 GB RAM) – recommended for stable operation
   - The HuggingFace model + Python overhead uses ~500–700 MB RAM; 2 GB gives comfortable headroom.
   - Swap is still added as a safety net (see Step 3) but is not load-bearing.
5. **Key pair**: Create a new key pair → download `stripe-rag-key.pem` somewhere safe
6. **Security group** – Add inbound rules:

   | Type | Protocol | Port | Source    |
   | ---- | -------- | ---- | --------- |
   | SSH  | TCP      | 22   | My IP     |
   | HTTP | TCP      | 80   | 0.0.0.0/0 |

7. **Storage**: 20 GB gp3 (within free tier – enough for Docker images + model cache)
8. Click **Launch instance**

### 1.3 Note the Public IP

Go to Instances → select `stripe-rag-app` → copy **Public IPv4 address** (e.g. `3.94.12.200`).
You will visit `http://3.94.12.200` in your browser once deployed.

---

## Step 2 – SSH into EC2

```bash
chmod 400 ~/Downloads/stripe-rag-key.pem
ssh -i ~/Downloads/stripe-rag-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

## Step 3 – Prepare the EC2 Instance

### 3.1 Create a Swap File (safety net – not critical on t3.small)

2 GB RAM is enough for normal operation, but adding 1 GB swap protects against
edge cases (e.g. background OS processes during heavy ingestion).

```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make it permanent across reboots
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Verify:

```bash
free -h   # should show ~1G swap
```

### 3.2 Install Docker

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
                        docker-buildx-plugin docker-compose-plugin

# Allow ubuntu user to run Docker without sudo
sudo usermod -aG docker ubuntu
newgrp docker

# Verify
docker --version && docker compose version
```

---

## Step 4 – Deploy the Code

### Option A: Push code via SSH/SCP (simpler for private repos)

On your **local machine**:

```bash
# Create a deployment directory on EC2
ssh -i ~/Downloads/stripe-rag-key.pem ubuntu@<EC2_PUBLIC_IP> "mkdir -p ~/apps"

# Sync both repos (exclude local caches, .venv, node_modules)
rsync -avz --progress \
  --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
  --exclude '.venv' --exclude 'venv' --exclude 'data/eval' \
  -e "ssh -i ~/Downloads/stripe-rag-key.pem" \
  /Users/navein/stripe-rag-agent/ \
  ubuntu@<EC2_PUBLIC_IP>:~/apps/stripe-rag-agent/

rsync -avz --progress \
  --exclude '.git' --exclude 'node_modules' --exclude 'dist' \
  -e "ssh -i ~/Downloads/stripe-rag-key.pem" \
  /Users/navein/stripe-rag-frontend/ \
  ubuntu@<EC2_PUBLIC_IP>:~/apps/stripe-rag-frontend/
```

### Option B: Clone from GitHub (if repos are pushed to GitHub)

SSH into EC2, then:

```bash
cd ~/apps
git clone https://github.com/<your-user>/stripe-rag-agent.git
git clone https://github.com/<your-user>/stripe-rag-frontend.git
```

⚠️ If using GitHub option, make sure `data/chroma_db/` is **not** in `.gitignore`, otherwise the pre-built vector store won't be cloned. Add an exception in `.gitignore` if needed:

```
!data/chroma_db/
```

---

## Step 5 – Build & Start the Containers

SSH into EC2:

```bash
cd ~/apps/stripe-rag-agent
```

### 5.1 Build images (takes 5–15 min on first run, mostly for HuggingFace model download)

```bash
docker compose build
```

You will see:

- Backend: installing ~1 GB of Python packages + downloading `BAAI/bge-small-en-v1.5`
- Frontend: `npm ci` + `vite build` + copying into nginx image

### 5.2 Start services

```bash
docker compose up -d
```

### 5.3 Check status

```bash
docker compose ps
# Both services should show "running (healthy)" after ~60 s

docker compose logs -f
# Ctrl+C to stop watching logs
```

Look for these lines confirming successful startup:

```
[Embeddings] Loading huggingface model: BAAI/bge-small-en-v1.5
[Embeddings] Model loaded successfully
[VectorStore] Initializing database at: /app/data/chroma_db
[VectorStore] Connected successfully
INFO:     Application startup complete.
```

---

## Step 6 – Run Enriched Re-ingestion (one-time)

The Docker image ships with the **baseline** pre-built ChromaDB. Once the backend
is healthy, run the enriched re-ingestion script to populate the vector store with
fused summaries, keywords, and hypothetical questions for improved search accuracy.

This runs **inside the backend container** and writes to the named Docker volume
(`chroma_data`), so it **persists across restarts and image rebuilds**.

```bash
# Confirm the backend container is healthy first
docker compose ps

# Run the reingest script (takes 1–3 min depending on corpus size)
docker exec -it stripe-rag-backend python "src/test files/reingest_enriched.py"
```

Expected output:

```
Source file lookup: 16 entries
Clearing old ChromaDB collection...
  ✓ Old collection deleted
Creating new ChromaDB collection...
  ✓ Collection ready
Loading <N> supercharged chunks into ChromaDB...
✅ Enriched re-ingestion complete! Processed <N>/<N> chunks.
```

> **Important**: Do NOT run `docker compose down -v` after this — it deletes the
> named volume and you will need to re-run the reingest script.
> Use `docker compose down` (without `-v`) for normal stops/restarts.

---

## Step 7 – Access the App

Open your browser and go to:

```
http://<EC2_PUBLIC_IP>
```

The React UI loads from nginx. When you submit a query, the browser posts to `http://<EC2_PUBLIC_IP>/query`, nginx intercepts it and forwards it to the backend container — no CORS issues, no cross-port calls.

---

## Updating the Deployment

When you push code changes:

```bash
# On your local machine – re-sync changed files
rsync -avz --progress \
  --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
  --exclude 'data/eval' \
  -e "ssh -i ~/Downloads/stripe-rag-key.pem" \
  /Users/navein/stripe-rag-agent/ \
  ubuntu@<EC2_PUBLIC_IP>:~/apps/stripe-rag-agent/

# SSH in and rebuild
ssh -i ~/Downloads/stripe-rag-key.pem ubuntu@<EC2_PUBLIC_IP>
cd ~/apps/stripe-rag-agent
docker compose build && docker compose up -d
```

Docker's layer cache means only changed layers rebuild (e.g. if only `src/` changed, the Python install + model download layers are reused).

---

## Useful Commands on EC2

```bash
# View live logs
docker compose logs -f

# Restart a specific service
docker compose restart backend

# Stop everything (preserves the chroma_data volume)
docker compose down

# ⚠️  DANGER – deletes the chroma_data volume (enriched DB lost → must re-run reingest)
docker compose down -v

# Check resource usage
docker stats

# Shell into backend container (for debugging)
docker exec -it stripe-rag-backend bash

# Re-run enriched ingestion (if you ever need to redo it)
docker exec -it stripe-rag-backend python "src/test files/reingest_enriched.py"
```

---

## AWS Cost Estimate (t3.small)

| Resource          | Rate                   | Estimate                    |
| ----------------- | ---------------------- | --------------------------- |
| EC2 t3.small      | ~$0.023/hr             | ~$17/month (always-on)      |
| EBS 20 GB gp3     | ~$0.08/GB/month        | ~$1.60/month                |
| Data Transfer Out | $0.09/GB (after 100GB) | Negligible for personal use |
| Elastic IP        | Free when attached     | Recommended – see below     |
| **Total**         |                        | **~$18–19/month**           |

> To cut cost: stop the EC2 instance when not in use (AWS Console → Stop).
> The Elastic IP and EBS data are retained. Restart when needed.
> The `chroma_data` volume survives stop/start — no need to re-run reingest.

### Get a Static Public IP (optional but recommended)

By default, EC2 public IPs change on reboot. To keep a stable IP:

1. **EC2 → Elastic IPs → Allocate Elastic IP**
2. **Actions → Associate Elastic IP** → select your instance
3. Your IP is now permanent (free while instance is running)

---

## What's NOT included (runtime only)

- **LLM API keys** (Groq / Gemini / OpenAI / Grok) – entered in the UI per session
- No `.env` file needed on the server – the agent receives credentials per-request from the frontend

---

## Troubleshooting

| Symptom                                 | Cause                                      | Fix                                                                  |
| --------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------- |
| Frontend shows but queries hang/timeout | Backend still loading model on first boot  | Wait 60 s, check `docker compose logs backend`                       |
| `Cannot connect to backend` in logs     | Container name mismatch                    | Check `docker compose ps`, service must be named `backend`           |
| OOM killed / container exits            | Burst spike beyond 2 GB (rare on t3.small) | Verify swap via `free -h`; restart: `docker compose restart backend` |
| Port 80 refused                         | Security group missing HTTP rule           | AWS Console → SG → add inbound 0.0.0.0/0 port 80                     |
| ChromaDB empty / no results             | `data/chroma_db/` not synced               | Re-run rsync or ensure git includes the chroma_db directory          |
