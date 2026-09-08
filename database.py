import time
import pypdf
import chromadb
from chromadb.utils import embedding_functions

def get_vector_db_collection(api_key):
  chroma_client = chromadb.PersistentClient(path="./my_vector_db")
  # gemini_embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
  #   api_key=api_key,
  #   model_name="models/gemini-embedding-001" #why this model?
  # )

  # NEW LOCAL EMBEDDING ENGINE (Bypasses Google Quota Restrictions)
  local_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="all-MiniLM-L6-v2"
  )

  return chroma_client.get_or_create_collection(
    name="pdf_knowledge_base_v4",
    embedding_function=local_embedding_fn
  )

def process_and_store_pdf(collection, uploaded_file, chunk_size=1000):
  """
  Reads the byte stream of an uploaded PDF file page-by-page, partitions
  the text chunks deterministically, logs page numbers as isolated metadata,
  and inserts them securely into the vector store.
  """
  reader = pypdf.PdfReader(uploaded_file)
  chunks = []
  metadata_list = []

  for idx, page in enumerate(reader.pages):
    page_num = idx + 1
    text = page.extract_text()
    if not text:
      continue

    for i in range(0, len(text), chunk_size):
      chunks.append(text[i:i+chunk_size])
      metadata_list.append({"page": page_num})

  batch_size = 3
  for i in range(0, len(chunks), batch_size):
    batch_chunks = chunks[i:i+batch_size]
    batch_meta = metadata_list[i:i+batch_size]
    batch_ids = [f"chunk_{j}_{uploaded_file.name}" for j in range(i, min(i + batch_size, len(chunks)))]

    collection.add(documents=batch_chunks, metadatas=batch_meta, ids=batch_ids)

    time.sleep(0.5)
