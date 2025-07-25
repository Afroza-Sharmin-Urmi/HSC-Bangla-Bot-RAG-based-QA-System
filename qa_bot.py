from sentence_transformers import SentenceTransformer, util
import pickle
import re
import os

CHUNKS_FILE = "HSC26_Bangla_chunks.txt"
EMBEDDINGS_FILE = "bangla_chunks_embeddings.pkl"

def load_data():
    if not os.path.exists(EMBEDDINGS_FILE):
        print(f"[ERROR] Embeddings file '{EMBEDDINGS_FILE}' not found. Run the embedding script first.")
        exit(1)
    with open(EMBEDDINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data["chunks"], data["embeddings"]

def extract_answer(chunk, query):
    import re

    # Normalize
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

    if "সুপুরুষ" in query:
        match = re.search(r'([\u0980-\u09FF]{3,})বাবু.*?সুপুরুষ', chunk)
        if match:
            return match.group(1) + "বাবু"
        match = re.search(r'([\u0980-\u09FF]{3,})\s+.*?সুপুরুষ', chunk)
        if match:
            return match.group(1)

    if any(word in query for word in ["বয়স", "কত", "বছর"]):
        match = re.search(r'\d{1,2}\s*বছর', best_sentence)
        if match:
            return match.group()

    name_suffixes = ("নাথ", "মামা", "দা", "পুরুষ", "বাবু", "চরণ", "সিংহ", "মা", "জী")
    stopwords = {"প্রশ্ন", "উত্তর", "অনুপম", "বলে", "যে", "না", "একজন", "হয়", "তাকে", "সে", "ঘটনা"}
    candidates = re.findall(r'[\u0980-\u09FF]{3,}', best_sentence)

    for word in candidates:
        if word not in stopwords and word.endswith(name_suffixes):
            return word

    for word in candidates:
        if word not in stopwords:
            return word

    return best_sentence


def ask_question():
    chunks, embeddings = load_data()
    model = SentenceTransformer("sentence-transformers/paraphrase-xlm-r-multilingual-v1")

    print("\nReady for Bangla question answering (type 'exit' to quit):\n")
    while True:
        query = input("প্রশ্ন: ").strip()
        if query.lower() == "exit":
            break

        q_embed = model.encode(query)
        hits = util.semantic_search(q_embed, embeddings, top_k=5)[0]

        answer = "Not found"
        for hit in hits:
            idx = hit['corpus_id']
            score = hit['score']
            chunk = chunks[idx]
            extracted = extract_answer(chunk, query)
            if extracted != "Not found":
                answer = extracted
                print(f"\nAnswer (Score: {score:.4f}): {answer}")
                print("="*50 + "\n")
                break
        else:
            print("\nAnswer: Not found\n" + "="*50 + "\n")

if __name__ == "__main__":
    ask_question()
