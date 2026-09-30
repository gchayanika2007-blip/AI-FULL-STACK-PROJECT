from sentence_transformers import SentenceTransformer
import chromadb,ollama
model = SentenceTransformer("all-MiniLM-L6-v2")
file_name="sample.txt"
with open(file_name,"r") as file:
    text = file.read()
chunks = []
chunk_size = 100
chunk_overlap = 20
step = chunk_size - chunk_overlap
for i in range(0,len(text),chunk_overlap):
    chunk = text[i:i+chunk_size]
    chunks.append(chunk)
embeddings = model.encode(chunks)
client = chromadb.PersistentClient(path = "./chroma_db")
collection = client.get_or_create_collection(name= "My_documents")
ids = []
for i in range(len(chunks)):
    ids.append(f"{file_name}_{i}")
collection .add(
    ids = ids,
    documents = chunks,
    embeddings =embeddings.tolist() 
)
# Query phase
question = input("Ask a question....")
question_embedding = model.encode(question)
results = collection.query(
    query_embeddings = [question_embedding.tolist()],
    n_results=3
)
# print(results)
retrived_results = results['documents'][0]
retrived_ids = results['ids'][0]
# print(retrived_results)
# for i in range(len(results['documents'][0])):
#     print(f"Chunk_{i}\n")
#     print(results['documents'][0][i])
# prompting
context = '\n'.join(retrived_results)
# print(retrived_results)
# print(context)
prompt = f'''
Answer the question using the context provided below.
Queestion : {question}
Context : {context}
Answer : '''
# print(prompt)
# connecting to local model
response = ollama.chat(
    model="llama3.2:3b",
    messages=[{
        "role" : "user",
        "content" : prompt
    }]
)
print(response['message']['content'])