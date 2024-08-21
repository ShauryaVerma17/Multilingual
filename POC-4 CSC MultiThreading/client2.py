import socket
import streamlit as st
import threading
import tkinter as tk
from tkinter import scrolledtext

def sendMessage():
    message = message_entry.get()
    if message:
        message = message.encode()
        c.send(message)
        chatHistory.config(state = 'normal')
        chatHistory.insert(tk.END, f"You : {message.decode()}\n")
        chatHistory.config(state = 'disabled')
        chatHistory.yview(tk.END)
        message_entry.delete(0,tk.END)

def recieveMessages():    
    while True: 
        try:
            incoming_message = c.recv(2048)
            incoming_message = incoming_message.decode()
            chatHistory.config(state = 'normal')
            chatHistory.insert(tk.END, f"Friend : {incoming_message}\n")
            chatHistory.config(state = 'disabled')
            chatHistory.yview(tk.END)
        except:
            c.close()
            break

def showMessages():
    chat = ""
    for message in chatHistory:
        chat = chat + f"\n{message}"
    return chat

root = tk.Tk()
root.title("Multilingual Client 2")

chatHistory = scrolledtext.ScrolledText(root)
chatHistory.pack(pady = 10)
chatHistory.config(state = 'disabled')

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady = 5, padx=10, side=tk.LEFT)

send_button = tk.Button(root, text="Send", command=sendMessage)
send_button.pack(pady = 5, padx=10, side=tk.LEFT)

c = socket.socket()
c.connect(("localhost", 50000))
language = "English"
c.send(language.encode())

threading.Thread(target=recieveMessages, daemon=True).start()

root.mainloop()

