# Interview Helper — Backend

A **FastAPI** backend that helps candidates prepare for job interviews using AI. Users upload their resume and job description, and the system uses LLM-powered features to simulate interviews, answer questions, and suggest resume improvements — all grounded in their own documents.

## How It Works

1. **Sign up / Log in** to get a JWT access token.
2. **Upload** your resume and job description (`.txt` or `.md` files).
3. The files are chunked, embedded, and stored in **ChromaDB**.
4. Use the AI features:
   - **Ask** — ask any question; the LLM automatically figures out whether to look in your resume or job description and answers accordingly.
   - **Interview** — simulate a mock interview; the LLM answers as the candidate, strictly based on the resume and JD.
   - **Improvements** — get a detailed resume analysis against the job description: match score, missing keywords, weak sections, suggested rewrites, and overall advice.

---

## Quick Start

### Prerequisites

- PostgreSQL
- OpenAI API key
- LangSmith API key (optional, for tracing)

### Installation

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and fill in all required values

# Run migrations
alembic upgrade head

# Start server
uv run uvicorn app.main:app --reload
```