from langchain_community.embeddings import ollama
from langchain.evaluation import load_evaluator


def get_embedding_function():
    ollama_emb = ollama.OllamaEmbeddings(model='nomic-embed-text')

    return ollama_emb


def main():
    # Get embedding for a word.
    embedding_function = get_embedding_function()
    vector = embedding_function.embed_query("apple")
    print(f"Vector for 'apple': {vector}")
    print(f"Vector length: {len(vector)}")

    # Compare vector of two words
    evaluator = load_evaluator("pairwise_embedding_distance")
    words = ("apple", "iphone")
    x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
    print(f"Comparing ({words[0]}, {words[1]}): {x}")


if __name__ == "__main__":
    main()