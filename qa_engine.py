from sentence_transformers import SentenceTransformer, util
import pickle
import re

CHUNKS_FILE = "HSC26_Bangla_chunks.txt"
EMBEDDINGS_FILE = "bangla_chunks_embeddings.pkl"

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def load_data():
    with open(EMBEDDINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data["chunks"], data["embeddings"]

chunks, embeddings = load_data()

def extract_answer(chunk, query):
    chunk = re.sub(r'[–—\-:]', ' ', chunk)
    chunk = re.sub(r'[^\u0980-\u09FF\d\s]', '', chunk)
    sentences = re.split(r'[।!?]', chunk)

    query_words = set(re.findall(r'[\u0980-\u09FF]{2,}|\d+', query))
    best_sentence = ""
    max_overlap = 0

    for sentence in sentences:
        sentence_words = set(re.findall(r'[\u0980-\u09FF]{2,}|\d+', sentence))
        overlap = len(query_words & sentence_words)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sentence = sentence.strip()

    if not best_sentence:
        return "Not found"

    return best_sentence.strip()

def get_answer(query, top_k=3):
    q_embed = model.encode(query)
    hits = util.semantic_search(q_embed, embeddings, top_k=top_k)[0]
    best = hits[0]
    best_chunk = chunks[best["corpus_id"]]
    extracted = extract_answer(best_chunk, query)
    
    return {
        "question": query,
        "answer": extracted,
        "score": round(best["score"], 4),
        "context": best_chunk
    }
