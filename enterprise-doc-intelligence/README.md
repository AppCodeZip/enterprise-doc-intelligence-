mkdir my_first_python_project
cd my_first_python_project


# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# Create your first Python file
touch main.py

# 3. Upgrade pip (optional but recommended)
pip install --upgrade pip


enterprise-doc-intelligence/
│
├── ingestion/
│   ├── loaders.py
│   ├── chunker.py
│
├── embeddings/
│   ├── embedder.py
│   ├── cache.py
│
├── vectorstore/
│   ├── faiss_store.py
│
├── rag/
│   ├── retriever.py
│   ├── prompt.py
│   ├── qa_chain.py
│
├── api/
│   ├── main.py
│
├── data/
│   ├── uploads/
│
├── README.md


# Code format
black your_file.py

# update library 
pip install -r requirements.txt

<!-- PDF → chunks → embeddings → FAISS → top-K relevant chunks -->




<!-- 🎯 Target Architecture (Simple & Industry-Standard)
User
 ↓
Internet
 ↓
EC2 (Ubuntu)
 ├── FastAPI (uvicorn)
 ├── FAISS (in-memory)
 ├── Ollama / LLM
 └── Persistent disk (embeddings, index)
1️⃣ Create EC2 Instance (AWS)
Step 1: Launch Instance
AMI: Ubuntu 22.04
Instance Type:
CPU only: t3.large
GPU (optional): g4dn.xlarge
Storage: 50 GB
Security Group:
Allow 22 (SSH)
Allow 8000 (FastAPI)
2️⃣ SSH Into EC2
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
3️⃣ Install System Dependencies
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl
4️⃣ Clone Your Project
git clone https://github.com/your-username/enterprise-doc-intelligence.git
cd enterprise-doc-intelligence
5️⃣ Python Virtual Environment
python3 -m venv venv
source venv/bin/activate
6️⃣ Install Python Dependencies
requirements.txt
(IMPORTANT – create this)
fastapi
uvicorn
faiss-cpu
sentence-transformers
pypdf
python-docx
python-multipart
tqdm
Then install:
pip install -r requirements.txt
7️⃣ Install Ollama (LLM Runtime)
curl -fsSL https://ollama.com/install.sh | sh
Pull model:
ollama pull llama3
Test:
ollama run llama3
8️⃣ Update FastAPI for Production
Change Uvicorn Command
Instead of --reload (dev only):
uvicorn api.main:app --host 0.0.0.0 --port 8000
9️⃣ Run the Server
uvicorn api.main:app --host 0.0.0.0 --port 8000
Open in browser:
http://<EC2_PUBLIC_IP>:8000/docs
🎉 Your GenAI RAG backend is LIVE on cloud
🔥 MAKE IT PRODUCTION-GRADE (VERY IMPORTANT)
10️⃣ Run as Background Service (systemd)
Create service file:
sudo nano /etc/systemd/system/rag-api.service
Paste:
[Unit]
Description=Enterprise RAG FastAPI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/enterprise-doc-intelligence
ExecStart=/home/ubuntu/enterprise-doc-intelligence/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
Enable & start:
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable rag-api
sudo systemctl start rag-api
Check status:
sudo systemctl status rag-api
1️⃣1️⃣ Persistence (VERY IMPORTANT)
Ensure these files stay on disk:
embeddings_cache.pkl
faiss.index
docs.pkl
They survive restart → no re-indexing
1️⃣2️⃣ Production Security (Basic)
Put EC2 behind Nginx (optional)
Add API key / JWT
Close port 8000 → expose via Nginx 80/443
(You can add later)
🧠 INTERVIEW: HOW TO EXPLAIN THIS DEPLOYMENT
Say this 👇 (memorize):
“I deployed the system on AWS EC2 using a VM-based approach because GenAI workloads require long-running processes, streaming responses, and in-memory vector stores. The FastAPI app runs as a systemd service, FAISS indexes are persisted to disk, and the LLM runs locally via Ollama. This setup avoids cold starts and supports real-time streaming.”
🔥 This is senior-level explanation.
🌍 SAME DEPLOYMENT ON OTHER CLOUDS
Azure
AWS	Azure
EC2	Virtual Machine
S3	Blob Storage
IAM	Azure AD
systemd	same
👉 Same steps, same commands.
GCP
AWS	GCP
EC2	Compute Engine
S3	Cloud Storage
ALB	Cloud Load Balancer
👉 Again, same architecture.
🏆 FINAL VERDICT
✅ Your project is cloud-ready
✅ EC2 deployment is industry-correct
✅ Interviewers will accept this confidently
✅ This is real GenAI backend engineering 





1️⃣ Docker + ECS Deployment
❓ What it is
You package your FastAPI + RAG system into a Docker image and deploy it on AWS ECS (managed containers).
✅ What problem it solves
Without Docker	With Docker
“Works on my machine”	Same everywhere
Manual setup	Automated
Hard to scale	Easy scaling
OS dependency	Portable
💎 Why Interviewers LOVE this
When you say Docker + ECS, interviewer hears:
CI/CD readiness
Microservices mindset
Cloud-native engineering
Team-scale deployment
🗣️ Interview signal:
“Candidate understands modern backend deployment.”
🔥 Real-world usage
Almost every production backend
Required for ECS / EKS / Kubernetes
Standard in startups & enterprises
2️⃣ Nginx + HTTPS (TLS)
❓ What it is
Nginx acts as:
Reverse proxy
Load balancer
HTTPS terminator
✅ What problem it solves
Problem	Solution
Exposing port 8000	Use 80/443
No SSL	HTTPS via TLS
Security risk	Industry standard
💎 Why Interviewers LOVE this
This shows:
You understand networking
You understand security basics
You know how real APIs are exposed
🗣️ Interview line:
“I don’t expose application ports directly; I put them behind Nginx with HTTPS.”
That’s production thinking.
🔥 Real-world usage
Every serious API
Mandatory in finance, healthcare, enterprise SaaS
3️⃣ S3 Auto-Ingestion (Event-Driven RAG)
❓ What it is
Documents are:
Uploaded to S3
Automatically indexed via events (no manual upload API)
✅ What problem it solves
Manual Upload	Auto-Ingestion
Human dependent	Fully automatic
Error-prone	Reliable
Not scalable	Scales infinitely
💎 Why Interviewers LOVE this
This is true automation.
🗣️ Interview signal:
“System reacts to data, not humans.”
This shows:
Event-driven architecture
Asynchronous thinking
Real enterprise workflows
🔥 Real-world usage
Knowledge bases
Compliance docs
Internal enterprise search
Legal / HR / Policy systems

☁️ S3 Auto-Ingestion — How It Works (Enterprise Way)
🎯 Goal (One Line)
Jaise hi koi document S3 me upload hota hai, system automatically usko read, chunk, embed aur index kar deta hai — bina kisi manual API call ke.
This is called event-driven ingestion.
🧠 High-Level Flow (Concept)
User / System
   ↓
Upload file to S3 bucket
   ↓
S3 Event Notification (ObjectCreated)
   ↓
Trigger (Lambda OR ECS task)
   ↓
Ingestion Pipeline
   ↓
FAISS / Vector DB Updated
No UI.
No /upload API.
Fully automatic.
🔹 Step 1: Document Upload to S3
Who uploads?
Human (HR uploads policy)
System (cron job, CI pipeline)
Another app
Example:
s3://enterprise-docs-bucket/hr/leave_policy.pdf
That’s it.
User ka kaam yahin khatam.
🔹 Step 2: S3 Event Notification
AWS S3 can emit events like:
ObjectCreated
ObjectRemoved
You configure S3:
“Whenever a new file is uploaded → notify something”
That “something” can be:
AWS Lambda ✅ (most common)
SQS
SNS
EventBridge
🔹 Step 3: Lambda Triggered Automatically
What Lambda Receives
Lambda gets metadata only (not full file):
{
  "bucket": "enterprise-docs-bucket",
  "key": "hr/leave_policy.pdf"
}
Lambda now knows:
Which file
Where it is
🔹 Step 4: Lambda Downloads File from S3
Inside Lambda:
import boto3

s3 = boto3.client("s3")
s3.download_file(bucket, key, "/tmp/leave_policy.pdf")
Now Lambda has the document.
🔹 Step 5: Lambda Calls Your RAG Ingestion Logic
Two options (both industry-used):
✅ Option A: Lambda calls your FastAPI ingestion endpoint
requests.post(
    "http://rag-backend/internal/ingest",
    files={"file": open("/tmp/leave_policy.pdf", "rb")}
)
Your existing logic runs:
load_document
chunk_documents
embed
FAISS add
✔ Reuse your current code
✔ Simple
✅ Option B: Lambda runs ingestion code directly (Better)
Lambda directly imports:
loaders.py
chunker.py
embedder.py
faiss_store.py
This is true automation.
🔹 Step 6: FAISS Index Updated
New embeddings added
Metadata stored
Index persisted to disk / S3
Now system is query-ready.
🔹 Step 7: User Asks Question (Later)
“What is the leave policy?”
System already knows the document —
no upload step required.
🏗️ COMPLETE ARCHITECTURE (Mental Picture)
[ S3 Bucket ]
     ↓ (ObjectCreated event)
[ Lambda Function ]
     ↓
[ Ingestion Logic ]
     ↓
[ FAISS Index ]
     ↓
[ FastAPI /query ]
     ↓
[ LLM Answer ]

-->

