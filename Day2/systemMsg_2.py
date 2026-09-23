import ollama
response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {
            'role':'system',
            'content':'You are teaching a 5 years baby should understand the concept.'
        },
        {
            'role': 'user',
            'content': 'Explain AI'
            
        }
    ]
    
)

print(response['message']['content'])