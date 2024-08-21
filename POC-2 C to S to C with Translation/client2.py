import socket

c = socket.socket()

c.connect(("localhost", 50000))
print('Connected to chat server')

while 1:
    incoming_message = c.recv(2048)
    incoming_message = incoming_message.decode()
    print('Client 1 >> ', incoming_message)
    print()
    message = input(str('Client 2 >> '))
    message = message.encode()
    c.send(message)
    #print('Message has been Sent')
    print()
    