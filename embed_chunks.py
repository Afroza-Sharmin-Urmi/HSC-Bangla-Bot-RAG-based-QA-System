from sentence_transformers import SentenceTransformer
import pickle

CHUNKS_FILE = "HSC26_Bangla_chunks.txt"
EMBEDDINGS_FILE = "bangla_chunks_embeddings.pkl"

def load_chunks(path):
    with open(path, "r", encoding="utf-8") as f:
        return [x.strip() for x in f.read().split("\n\n") if x.strip()]

def main():
    chunks = load_chunks(CHUNKS_FILE)
    from sentence_transformers import SentenceTransformer
     model = SentenceTransformer("sentence-transformers/paraphrase-xlm-r-multilingual-v1") # Better for Bangla
    embeddings = model.encode(chunks, show_progress_bar=True)

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump({"chunks": chunks, "embeddings": embeddings}, f)
    print(f"Embeddings saved for {len(chunks)} chunks.")

if __name__ == "__main__":
    main()
