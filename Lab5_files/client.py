import socket

# Socket setup: AF_INET for internet and SOCK_STREAM for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get the IP address of the server from the user
host = input(str('Enter the host IP address: '))
# Define the port number
port = 12346
# Connect to the server
s.connect((host, port))
print('Connected')

# Get the name of the file to send from the user
filename = input(str('Enter the name of the file: '))
# Open the file
file = open(filename, 'rb')
# Need a loop to send more than 1024 bytes
while True:
    # Gather the data from the file 1024 bytes at a time
    file_data = file.read(1024)
    # Send the 1024 bytes of data
    s.send(file_data)
    # Check if there is more data to send
    if not file_data:
        break
print('Data has been successfully transmitted')
file.close()
s.close()
