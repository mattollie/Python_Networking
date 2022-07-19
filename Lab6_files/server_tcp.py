import socket
import subprocess as sp
from threading import Thread
import datetime
from time import sleep


# Define the class for handling multiple threads (clients)
class ClientThread(Thread):

    def __init__(self, addr, clientsocket):
        Thread.__init__(self)
        self.csocket = clientsocket
        self.address = addr
        print('New socket started for ' + str(self.address) + '\n')

    def run(self):
        while True:
            # Receive the command
            message = self.csocket.recv(50)
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
            print('Command received from %s at time %s: "%s"' % (str(self.address), rc, command))
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
            with open('contents_tcp', 'wb') as cont:
                cont.write(bytes(time_string, 'UTF-8'))
                cont.write(bytes(contents_string, 'UTF-8'))

            # Open the file that has just been created
            new = open('contents_tcp', 'rb')
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
            self.csocket.send(a)
            # Send the contents of the file
            self.csocket.send(first)
            print('Contents have been sent')
            print('Socket closed for ' + str(self.address) + '\n')
            # Close the file
            new.close()
            break


def start_socket():
    # Socket setup: AF_INET for internet and SOCK_STREAM for TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Get the name of the local host
    host = input(str('Enter the host IP address: '))
    # Define the port number
    port = input('Enter the port number: ')
    # Bind the host and port numbers
    s.bind((host, int(port)))
    print('Waiting for connections...' + '\n')

    while True:
        # Listen for incoming connections
        s.listen(1)
        # Accept an incoming connection
        conn, addr = s.accept()
        # Send the accepted connection to the thread class
        newthread = ClientThread(addr, conn)
        newthread.start()


def main():
    start_socket()


if __name__ == '__main__':
    main()
