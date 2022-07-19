import socket

# Socket setup: AF_INET for internet and SOCK_STREAM for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get the name of the local host
host = input(str('Enter the host IP address: '))
# Define the port number
port = 12346
# Bind the host and port numbers
s.bind((host, port))
# Listen for incoming connections
s.listen(5)
print(host)
print('Waiting for incoming connections...')

while True:
    # Accept an incoming connection
    conn, addr = s.accept()
    print(addr, 'Has connected')

    # Accept the name of the file that is being received
    filename = input(str('Enter the name of the incoming file: '))
    # Open a new file to write the incoming data
    file = open(filename, 'wb')
    while True:
        # Receive the data
        file_data = conn.recv(1024)
        # Write the received data to the opened file
        file.write(file_data)
        # Check if there is any data left to receive
        if not file_data:
            break
    file.close()
    print('File has been successfully received')
    print('Waiting for incoming connections...')
