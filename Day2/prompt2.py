import ollama
response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {
            'role': 'user',
            'content': 'Define about AI in 2 lines and  only name of 3 types of AI and two real time example in bullet points'
            
        }
    ]
    
)

print(response['message']['content'])