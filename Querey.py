import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load the FAISS index and mapping
index = faiss.read_index('warframe_faiss_index')
mapping_df = pd.read_csv('warframe_faiss_mapping.csv')

# Initialize the sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the FLAN-T5 model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def process_query(query, k=5):
    # Generate embedding for the query
    query_embedding = sentence_model.encode([query])[0]

    # Normalize the query embedding
    faiss.normalize_L2(query_embedding.reshape(1, -1))

    # Perform the search
    D, I = index.search(query_embedding.reshape(1, -1), k)

    # Get the corresponding sentences and titles
    results = mapping_df.iloc[I[0]]

    return results


def generate_response(query, context):
    # Prepare the prompt
    prompt = f"Answer the following question based on the given context about Warframe:\n\nQuestion: {query}\n\nContext:\n"
    for _, row in context.iterrows():
        prompt += f"- {row['sentences']} (from {row['title']})\n"
    prompt += "\nAnswer:"

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generate response
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=150, num_return_sequences=1)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def warframe_qa(query):
    # Process the query
    relevant_info = process_query(query)

    # Generate response
    response = generate_response(query, relevant_info)

    return response


# Example usage
while True:
    user_query = input("Ask a question about Warframe (or type 'quit' to exit): ")
    if user_query.lower() == 'quit':
        break
    answer = warframe_qa(user_query)
    print(f"\nAnswer: {answer}\n")