from sentence_transformers import SentenceTransformer
import chromadb
model = SentenceTransformer("all-MiniLM-L6-v2")
with open("ai_sample.txt","r") as file:
    text = file.read()
#print(text)
chunks = []
chunk_size = 25
chunk_overlap = 20
step = chunk_size - chunk_overlap
for i in range(0,len(text),chunk_overlap):
    chunk = text[i:i+chunk_size]
    chunks.append(chunk)
# print("No.of chunks:",len(chunks))
# for i in range(len(chunks)):
#     print(f"Chunk {i} ->{chunks[i]}")
# Embeddings
embeddings = model.encode(chunks)
# print("Embedding created successfully")
# print(len(embeddings))
# print(embeddings[0])
# print(embeddings.shape)
# chromadb
client = chromadb.Client()
collection = client.create_collection(name= "My_documents")
# print("Collection created successfully")
ids = []
for i in range(len(chunks)):
    ids.append(str(i))
collection .add(
    ids = ids,
    documents = chunks,
    embeddings =embeddings.tolist() 
)
# print("No of collections:",collection.count())
# col = collection.get(ids=['0'])
# print(col)
print("No.of items in the collections:",collection.count())
results = collection.get()
for i in range(len(results["ids"])):
    print(f"ID:{results['ids'][i]} -> Chunk:{results['documents'][i]}")
chunk1 = collection.get(ids=['0'])
print("Chunk 1") 

    