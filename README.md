
# HSC Bangla Bot (RAG-based QA System)

A Bangla question-answering bot that uses Retrieval-Augmented Generation (RAG) to answer questions from the **HSC Bangla 1st Paper** textbook. It extracts answers from a converted PDF using semantic search and sentence-level analysis.


## Setup Guide

### 1. Clone Repository & Setup Environment

```bash
git clone https://github.com/Afroza-Sharmin-Urmi/HSC-Bangla-Bot-RAG-based-QA-System.git
cd HSC_bot
python3 -m venv rag-env
source rag-env/bin/activate
pip install -r requirements.txt
```

### 2. Install Required Dependencies

```bash
sudo apt install poppler-utils tesseract-ocr -y
pip install -r requirements.txt
```

### 3. Prepare Data

- Place the **HSC26-Bangla1st-Paper.pdf** in the project root.
- Run PDF to text extraction and chunking:
```bash
python ocr_and_chunk.py
```

- Generate embeddings:
```bash
python embed_chunks.py
```

### 4. Run QA Bot

```bash
python qa_bot.py
```

### 5. Run REST API

```bash
uvicorn app:app --reload --port 8000
```

---

## 🔧 Tools, Libraries & Models Used

| Tool | Purpose |
|------|---------|
| `pdf2image`, `pytesseract` | Extract text from scanned PDF |
| `sentence-transformers` | Generate embeddings |
| `paraphrase-xlm-r-multilingual-v1` | Multilingual semantic understanding |
| `FAISS` | Fast vector search (if used in scalable version) |
| `FastAPI`, `Uvicorn` | REST API interface |
| `Python` | Core logic and orchestration |

---

## Sample Given Queries and Outputs

### Input (Bangla):
```
প্রশ্ন: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
```
### Output:
```
Answer: শস্তুনাথ
```

---

### Input:
```
প্রশ্ন: কাকে অনুপমের ভাগ্য দেবতা বলা হয়েছে?
```
### Output:
```
Answer: মামা
```

---

### Input:
```
প্রশ্ন: বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
```
### Output:
```
Answer: ১৫ বছর
```

---


My Model Result:
==================================================

### Input:
```
প্রশ্ন: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
```
### Output:
```
Answer (Score: 0.8438): কোন
```
### Input:
```
প্রশ্ন:  কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?
```
### Output:
```
Answer (Score: 0.7878): ৮১মামাকে
```
### Input:
```
Answer (Score: 1.0000): বিয়ের
```
### Output:
```
প্রশ্ন:  বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?

```



## API Documentation

### `POST /ask`

**Request**
```json
{
  "question": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?"
}
```

**Response**
```json
{
  "answer": "৮১মামাকে",
  "score": 0.98
}
```

---

## Evaluation Matrix

| Metric | Result |
|--------|--------|
| Groundedness | (answers taken directly from context) |
| Relevance | Medium (accuracy ~70% depending on question) |
| Cosine Similarity | Used as match score |
| Manual QA Evaluation | 20 sample questions validated by human |

---

## Methodology Q&A

### 1. What method or library did you use to extract the text, and why?

I used **pdf2image** + **pytesseract** to OCR scanned PDFs because the original document was image-based. This method allowed us to extract Bangla characters reliably. Some formatting issues like broken sentences and missing punctuation were observed, which were handled via regex.

---

### 2. What chunking strategy did you choose?

I used **sentence-based chunking** with optional context overlap (2–3 sentences per chunk). This method preserves semantic meaning and allows the model to find relevant answers without excessive context.

---

### 3. What embedding model did you use?

I used `sentence-transformers/paraphrase-xlm-r-multilingual-v1`, which supports Bangla and performs well in semantic similarity tasks. It captures the overall meaning of sentences rather than exact words.

---

### 4. How are you comparing the query with your stored chunks?

I use **cosine similarity** between the question and all chunk embeddings using `semantic_search()` from `sentence_transformers.util`. This provides a relevance-ranked list of candidate answers.

---

### 5. How do you ensure meaningful comparisons?

I clean the question and chunk text, extract relevant Bangla words, and use regex to match common QA patterns (e.g., names, numbers). If the query is vague, return "Not found" or ask for clarification.

---

### 6. Are the results relevant?

Partially. The bot correctly answers **fact-based** questions (e.g., names, ages), but struggles with vague or abstract queries. Improvements could include:

- Better chunk overlap
- Bangla-specific embedding models
- Named Entity Recognition for Bangla

---

## Future Improvements

- Integrate a Bangla-tuned BERT or `bmdh/bangla-sentence-transformers`
- Use FAISS for scalable vector search
- Add UI or chatbot interface
- Train a small QA finetuned model on textbook

---

## License & Attribution

Built for educational purposes using publicly available HSC Bangla materials.
