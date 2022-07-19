import socket

import datetime

import os


# Define the IP address and the Port Number

ip = "127.0.0.1"

port = 7071

listeningAddress = (ip, port)

# Create a datagram based server socket that uses IPv4 addressing scheme

datagramSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

datagramSocket.bind(listeningAddress)

# Initialize message, date/time, and client list

msg_list = []
sourceAddressList = []
date_time_list = []

while True:

    msg, sourceAddress = datagramSocket.recvfrom(250)

    with open("Encrypted.txt", "wb") as encrypted_input:
        encrypted_input.write(msg)

    os.system('python3.7 /Users/Lakefork15/PycharmProjects/ECE_456_Labs/Lab1_files/Lab1_Decrypt.py')

    with open("Decrypted.txt", "rb") as decrypt:
        msg_ready = decrypt.read()

    if msg_ready.decode() == 'exit':
        break

    msg_list.append(msg_ready.decode())
    sourceAddressList.append(sourceAddress)
    date_time_list.append(datetime.datetime.now())

    i = 0

    # Loop to display 5 most recent messages

    for i in range(len(msg_list)):
        if i == 5:
            i -= 1
            msg_list.remove(msg_list[0])
            sourceAddressList.remove(sourceAddressList[0])
            date_time_list.remove(date_time_list[0])
    response = "Received message from %s at %s: %s" % (sourceAddressList, date_time_list, msg_list)
    print(response)
    datagramSocket.sendto(response.encode(), sourceAddressList[i])
print('Closing connection')
datagramSocket.close()