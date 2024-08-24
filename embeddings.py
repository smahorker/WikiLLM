import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Load the preprocessed data
df = pd.read_csv('preprocessed_warframe_data.csv')

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(df['sentences'].tolist(), show_progress_bar=True)

# Convert embeddings to numpy array and normalize
embeddings_np = np.array(embeddings).astype('float32')
faiss.normalize_L2(embeddings_np)

# Create FAISS index
print("Creating FAISS index...")
dimension = embeddings_np.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings_np)

# Save the index
print("Saving FAISS index...")
faiss.write_index(index, 'warframe_faiss_index')

# Save the mapping of index to sentence and title
print("Saving mapping data...")
df['faiss_id'] = range(len(df))
df[['faiss_id', 'title', 'sentences']].to_csv('warframe_faiss_mapping.csv', index=False)

print("Process completed!")