import socket

# Socket setup: AF_INET for internet and SOCK_DGRAM for UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Get the IP address of the server from the user
host = input(str('Enter the host IP address: '))
# Define the port number
port = input('Enter the port number: ')

# Get the number of times the command will be executed
execution_count = input(str('Enter the number of times the command will be executed: '))
# Get the time delay
time_delay = input(str('Enter the time delay between command executions in seconds: '))
# Get the command
command = input(str('Enter the command for the server: '))
# Combine the execution count, time delay and command into a single message
message = execution_count + ',' + time_delay + ',' + command
s.sendto(bytes(message, 'UTF-8'), (host, int(port)))
print('Command sent!' + '\n')
# Receive the data length
length_of_data, source_address = s.recvfrom(10)
# Make a list to append the length with zeros
data_list = []
# Make a list to append the length without zeros
new_list = []
# Append the length with zeros
for x in range(10):
    data_list.append(length_of_data[x])
# Find the index of the first nonzero number
k = data_list.index(next(filter(lambda i: i != 0, data_list)))
# Append the data length without zeros
for j in range(10-k):
    new_list.append(data_list[k])
    k += 1
# Convert each element to a string in order to join the full data length
y = [str(i) for i in new_list]
# Join the elements and convert to an integer
res = int(''.join(y))

# Receive the result of the command
contents, source_address = s.recvfrom(res)
# Convert the received bytes to a string
printable_contents = contents.decode()
# Create the variable for the index that separates the execution times from the results
time_length = ((8 * int(execution_count)) + (5 * int(execution_count)))
# Separate the execution times from the results and store the times
execute_times = printable_contents[:time_length]
# Split each individual execution time
execute_times = execute_times.split('{fin}')
# Separate the execution times from the results and store the results
result_of_command = printable_contents[time_length:]
# Split each individual result
result_of_command = result_of_command.split('{fin}')
print('Length of data from server is %d bytes' % res)
print('Result of "%s" on the server:' % command)
# Print the execution times and the results
for n in range(int(execution_count)):
    if n == 0:
        print('\n1st iteration executed at %s' % execute_times[n])
        print(result_of_command[n])
    elif n == 1:
        print('\n2nd iteration executed at %s' % execute_times[n])
        print(result_of_command[n])
    elif n == 2:
        print('\n3rd iteration executed at %s' % execute_times[n])
        print(result_of_command[n])
    else:
        print('\n%sth iteration executed at %s' % (n+1, execute_times[n]))
        print(result_of_command[n])
print('\n' + 'Closing connection to server' + '\n')
# Close the socket
s.close()
