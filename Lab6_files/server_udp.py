import socket
import subprocess as sp
from threading import Thread
import datetime
from time import sleep


# Define the class for handling multiple threads (clients)
class ClientThread(Thread):

    def __init__(self, host, port):
        # Initialize the address and port number
        Thread.__init__(self)
        self.port = port
        self.host = host
        self.socket = None

    def configure_server(self):
        # Create the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('\nSocket created')
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the server to the address
        self.socket.bind((self.host, self.port))
        print(f'Server binded to {self.host}:{self.port}\n')

    def run(self):
        while True:
            # Receive the command
            message, client = self.socket.recvfrom(50)
            # Convert the received bytes to a string
            message = message.decode()
            message = message.split(',')
            # Separate the execution times, time delay, and command
            execution_times = int(message[0])
            time_delay = int(message[1])
            command = message[2]
            # Get the time at which the contents were received
            received_time = datetime.datetime.now()
            # Format the received time
            rc = str(received_time.strftime("%H:%M:%S"))
            print('Command received from %s at time %s: "%s"' % (str(client), rc, command))
            print('Executing command...')
            # Initialize the final strings that will be sent to the client
            contents_string = ''
            time_string = ''
            # Execute the command execution_times with time between executions time_delay
            for m in range(execution_times):
                contents = sp.getoutput(command)
                # Get the time at which the command is executed
                now = datetime.datetime.now()
                # Format the time
                timing = str(now.strftime("%H:%M:%S"))
                # Separate each command and time at which it is executed in order for the client to decode the contents
                contents_string += contents + '{fin}'
                time_string += timing + '{fin}'
                # Delay the command execution by the client specified time delay
                sleep(time_delay)
            # Write the contents of the command and the execution times to a file
            with open('contents_udp', 'wb') as cont:
                cont.write(bytes(time_string, 'UTF-8'))
                cont.write(bytes(contents_string, 'UTF-8'))

            # Open the file that has just been created
            new = open('contents_udp', 'rb')
            first = new.read()
            # Create a list for the length of the file
            len_list = []
            # Create a byte array to send to the client
            a = bytearray()
            # Get the length of the file
            length = str(len(first))
            # Append each number in the length to the list
            for char in length:
                len_list.append(char)
            # Make the list 10 bytes long
            for x in range(10 - len(len_list)):
                len_list.insert(0, '0')
            # Convert the contents in the length list to bytes
            for num in len_list:
                num = bytes(num, 'UTF-8')
                a.append(int(num))
            print('Sending contents to client...')
            # Send the length of the file
            self.socket.sendto(a, client)
            # Send the contents of the file
            self.socket.sendto(first, client)
            print('Contents have been sent')
            print('Socket closed for ' + str(client) + '\n')
            # Close the file
            new.close()
            break


def get_sock_info():
    # Get the name of the local host
    host = input(str('Enter the host IP address: '))
    # Define the port number
    port = input('Enter the port number: ')
    # Create the server with the given address and port number
    newthread = ClientThread(host, int(port))
    # Configure the server
    newthread.configure_server()

    while True:
        # Execute the command
        newthread.run()
        # Start a new thread
        newthread.start()


def main():
    get_sock_info()


if __name__ == '__main__':
    main()
