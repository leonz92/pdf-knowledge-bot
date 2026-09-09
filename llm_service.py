import google.generativeai as genai
import pypdf

def ask_gemini_with_memory(collection, question, chat_history, api_key):
  """
  Executes a vector serach based on user prompt, pieces together conversational history context window and exectes a targeted RAG pipeline query
  """
  genai.configure(api_key=api_key)

  #query chromadb for top 3 matching text nodes based on vector proximity
  results = collection.query(query_texts=[question], n_results=3)
  retrieved_metadata = results['metadatas'] if results['metadatas'] else []
  flattened_chunks = []
  if results['documents']:
      for chunk_list in results['documents']:
          if chunk_list:
              for chunk in chunk_list:
                  if chunk:
                      flattened_chunks.append(str(chunk))

  pages_found = []
  if retrieved_metadata:
      for metadata_list in retrieved_metadata:
          if metadata_list:
              for meta in metadata_list:
                  if meta and 'page' in meta:
                      pages_found.append(meta['page'])

  # Deduplicate page entries and arrange them in ascending order
  pages_found = sorted(list(set(pages_found)))
  context = "\n---\n".join(flattened_chunks)

  formatted_history = "".join([f"{msg['role'].capitalize()}: {msg['content']}\n" for msg in chat_history])

  prompt = f"""
  You are a helpful assistant. Use the provided context below to help answer the user's latest question.
  Rely heavily on the conext, but also remember conversation history to understand the follow-up terms.
  If the answer cannot be found in the conext or history, say "I cannot find the answer in the provided documents."

  [CONVERSATION HISTORY]
  {formatted_history if formatted_history else "No history yet."}

  [new retrieves context from pdf]
  {context}

  Latest User Question: {question}
  Assistant Answer:
  """

  model = genai.GenerativeModel("gemini-3.5-flash")
  response = model.generate_content(prompt)
  return response.text, pages_found

def ask_gemini_with_raw_text(question, raw_text, chat_history, api_key):
  """
  Passes loose text inputs directly to the LLM's primary memory window,
  bypassing vector segmentation db's
  """
  genai.configure(api_key=api_key)
  formatted_history = "".join([f"{msg['role'].capitlaize()}: {msg['content']}\n" for msg in chat_history])

  prompt = f"""
  You are a helpful assistant. Use the provided text block below to help answer the user's latest question.
  Rely heavily on the text context, but also remember conversational history to understand follow-up terms.
  If the answer cannot be found in the text or history, say "I cannot find the answer in the provides text."

  [CONVERSATIONAL HISTORY]
  {formatted_history if formatted_history else "No history yet."}

  [PROVIDED TEXT CONTENT]
  {raw_text}

  Latest User Question: {question}
  Assistant Answer:
  """

  model = genai.GenerativeModel("gemini-3.5-flash")
  response = model.generate_content(prompt)
  return response.text

def summarize_entire_pdf(uploaded_file, api_key):
  genai.configure(api_key=api_key)
  reader = pypdf.PdfReader(uploaded_file)
  full_text = "".join([page.extract_text() or "" for page in reader.pages])

  prompt = f"""
  You are an expert analyst. Provide a comprehensive summary of the entire document proivded below.
  Break it down into:
  1. Executive summary (Overall concept)
  2. Key Takeaways & Core Themes (Bullet points)
  3. Conclusion

  Document Content:
  {full_text}
  """

  model = genai.GenerativeModel("gemini-3.5-flash")
  response = model.generate_content(prompt)
  return response.text
