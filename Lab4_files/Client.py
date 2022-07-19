import socket

import os

# Get the port number from the user

port = input("Enter the port number: ")

# Get the IP address of the server

ip_address = input("Enter the server IP address: ")

# A tuple with server ip and port

serverAddress = (ip_address, int(port))

# Create a datagram socket

Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

fromserv = []

while True:
    i = 0
    # Socket is not in connected state yet...sendto() can be used

    # Get the message from the user to send to the server

    msg = input("Enter a message: ")

    if msg == 'exit':
        Socket.sendto(msg.encode(), (ip_address, int(port)))
        Socket.close()
        print('Closing connection')
        exit()
    # Encrypt message and send message to the server

    with open('file.txt', 'wb') as message_file:
        message_file.write(bytes(msg, 'UTF-8'))

    os.system('python3.7 /Users/Lakefork15/PycharmProjects/ECE_456_Labs/Lab1_files/Lab1_Encrypt.py')

    with open('Encrypted_data', 'rb') as encrypted:
        encrypt_send = encrypted.read()

    Socket.sendto(encrypt_send, (ip_address, int(port)))
    response = Socket.recvfrom(1000)
    # fromserv.append(response)
    # for i in range(len(fromserv)):
    #     if i == 5:
    #         i -= 1
    #         fromserv.remove(fromserv[0])
    print(response)
Socket.close()