import socket
from openai import OpenAI
from dotenv import load_dotenv
import os

# Initialize open ai key
load_dotenv()
openai = OpenAI(
    api_key= os.getenv('kurtim_api_key'), # Refer to Create a secret key section
    base_url="https://cloud.olakrutrim.com/v1",
)

# Initialize chat history, language
chatHistory = ["","","","","",""]
firstClientLanguage = "Hindi"
secondClientLanguage = "English"


# Initialize the translation function
def chat(fromLanguage, sentence, toLanguage): 
    
    global chatHistory
    query = f"Translate this {fromLanguage} sentence '{sentence}' to {toLanguage}"
    chat_completion = openai.chat.completions.create(
    model="Meta-Llama-3-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful translator assistant. You are given conversation history and the latest question from the user. Only respond with the translation nothing else"},
        {"role": "user", "content": chatHistory[-6]},
        {"role": "assistant", "content": chatHistory[-5]},
        {"role": "user", "content": chatHistory[-4]},
        {"role": "assistant", "content": chatHistory[-3]},
        {"role": "user", "content": chatHistory[-2]},
        {"role": "assistant", "content": chatHistory[-1]},
        {"role": "user", "content": query}
    ],
    logit_bias= {2435: -100, 640: -100},
    max_tokens= 5000,
    temperature= 0, # Optional, Defaults to 1. Range: 0 to 2
    top_p= 1 # Optional, Defaults to 1. It is generally recommended to alter this or temperature but not both.
    )

    response = chat_completion.choices[0].message.content

    chatHistory.append(query)
    chatHistory.append(response)

    return response

s = socket.socket()
s.bind(("localhost", 50000))
print('\nWaiting for connection\n')
s.listen(2)
conn1, addr1 = s.accept()
print(addr1, ' has connected to the server\n')
conn2, addr2 = s.accept()
print(addr2, ' has connected to the server\n')

while 1:
    
    # Recieving from Client 1 and Sending to Client 2 after translation
    incoming_message = conn1.recv(2048)
    incoming_message = incoming_message.decode()
    translated_message = chat(firstClientLanguage, incoming_message, secondClientLanguage)
    translated_message = translated_message.encode()
    conn2.send(translated_message)

    # Recieving from Client 2 and Sending to Client 1 after translation
    incoming_message = conn2.recv(2048)
    incoming_message = incoming_message.decode()
    translated_message = chat(secondClientLanguage, incoming_message, firstClientLanguage)
    translated_message = translated_message.encode()
    conn1.send(translated_message)


