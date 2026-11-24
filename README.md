# AI Resume Analyzer / JD Matcher

Upload a resume and paste a job description. The app returns a match score,
per-criterion scores with quoted evidence from the resume, and missing keywords.

## How it works

1. Parse the resume (PDF or DOCX) and clean the text.
2. Split it into chunks and store embeddings in FAISS (RAG).
3. An LLM extracts 5-6 hiring criteria from the job description.
4. For each criterion, retrieve the top-3 resume chunks and ask the LLM
   for a 0-10 score plus an exact quote.
5. Verify every quote exists in the resume. Unverified quotes cap the score.
6. Combine three signals into a final score.

## Scoring

| Signal | Weight | What it measures |
|---|---|---|
| Semantic similarity | 40% | Embedding match between criteria and resume chunks |
| Skill overlap | 30% | Skills in the JD that appear in the resume |
| LLM rubric | 30% | Scored evidence per criterion, quotes verified |

Weights live in `backend/app/config.py`.

## Tech stack

Python, LangChain, FAISS, sentence-transformers (all-MiniLM-L6-v2),
Groq (openai/gpt-oss-20b), Pydantic, PyMuPDF, pdfplumber, python-docx, Streamlit.

## Project structure

    backend/app/parsing/    PDF/DOCX parsing and text cleaning
    backend/app/rag/        chunking, embeddings, FAISS, retriever
    backend/app/llm/        Groq client, prompts, schemas, chains
    backend/app/scoring/    semantic, skills, rubric, hybrid scores
    backend/app/services/   analyzer.py (full pipeline)
    backend/checks/         runnable checks for each module
    frontend/streamlit_app/ UI

The UI contains no scoring logic. It only calls `analyze()`, so it can be
replaced by FastAPI + React without touching the backend.

## Setup

    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r backend/requirements.txt
    copy .env.example .env      # then add your GROQ_API_KEY

## Run

    streamlit run frontend/streamlit_app/app.py

Try it with `samples/demo_resume.pdf` and `samples/demo_jd.txt`.

## Known limitations

- Skill matching is dictionary-based (no aliases or plural handling).
- Semantic score normalization limits were tuned on a single resume.
- LLM calls run sequentially, so analysis takes 15-40 seconds.
- Resume text is sent to the Groq API. PII masking is not implemented yet.
- No knockout rule: a missing must-have skill lowers the score but does not cap it.

## Future work

Evaluation set with recall@k and MRR, parallel LLM calls, PII masking,
knockout rules, FastAPI + React frontend.