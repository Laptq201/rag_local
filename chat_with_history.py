from ollama import chat

message = [
    {
    'role': 'user',
    'content': 'Why is the sky blue?',
    },
    {
    'role': 'assistant',
    'content': "The sky is blue because of the way the  Earth's atmosphere scatters sunlight.""",
    },
    {
    'role': 'user',
    'content': 'What is the weather in Tokyo?',
    },
    {
    'role': 'assistant',
    'content': '''The weather in Tokyo is typically 
                warm and humid during the summer months,
                with temperatures often exceeding 30°C (86°F). 
                The city experiences a rainy season from June to September, 
                with heavy rainfall and occasional typhoons.
                Winter is mild, with temperatures rarely dropping 
                below freezing. The city is known for its high-tech 
                and vibrant culture, with many popular tourist attractions 
                such as the Tokyo Tower, Senso-ji Temple, and 
                the bustling Shibuya district.''',
    },
]

while True:
    user_input = input('Chat with LLM (type "exit" to quit): ')
    if user_input.lower() == 'exit':
        break
    response = chat(model='llama3.2',
                    messages=message + [{'role': 'user', 'content': user_input}])
    message.append({'role': 'user', 'content': user_input})
    message.append({'role': 'assistant', 'content': response['message']['content']})
    print(response['message']['content'])
    #print(response.message.content + '\n')
    # 2 đoạn ở dòng 39 - 40 là tương đương nhau
    print('---\n')
