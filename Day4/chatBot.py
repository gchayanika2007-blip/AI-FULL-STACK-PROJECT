import ollama
msgs=[
    {
        'role':'sysytem',
        'content':'you are talking with small child'
    }
]
while True:
    question=input("Ask the question: ")
    if question.lower() == "exit":
        break
    msgs.append({
        "role":"user",
        "content":question
    })
    response = ollama.chat(
        model='llama3.2:3b',
        messages=msgs)
    msgs.append(
        {
            "role":"assistent",
            "content": response['message']['content']
        }
    )
    print("AI:",response['message']['content'])

print("----Chat History----\n")
for msg in msgs:
    print(msg["role"],":",msg["content"])