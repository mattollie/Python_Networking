import struct
import math
from Lab1_files import Lab1_Encrypt


def ip_to_byte_array(ip):
    words = ip.split('.')
    int_list = []
    for num in words:
        int_list.append(int(num))
    c = bytes(int_list)
    bigendian = struct.unpack('>I', c)
    return '{}'.format(bigendian[0])


def get_source_ip_bytes(source_ip):
    words = source_ip.split('.')
    int_list = []
    for num in words:
        int_list.append(int(num))
    print('Source IP byte1: ' + str(int_list[0]) + '\n' + 'Source IP byte2: ' + str(int_list[1]) + '\n' + 'Source IP byte3: ' + str(int_list[2]) + '\n' + 'Source IP byte4: ' + str(int_list[3]))


def get_dest_ip_bytes(dest_ip):
    words = dest_ip.split('.')
    int_list = []
    for num in words:
        int_list.append(int(num))
    print('Destination IP byte1: ' + str(int_list[0]) + '\n' + 'Destination IP byte2: ' + str(int_list[1]) + '\n' + 'Destination IP byte3: ' + str(int_list[2]) + '\n' + 'Destination IP byte4: ' + str(int_list[3]))


def read_input_file(input_name):
    with open(input_name, 'rb') as filename:
        ven = filename.read()
        ven_len = len(ven)
        byte_list = []
        f = 0
        while f < ven_len:
            L = ven[f]
            byte_list.append(L)
            f += 1
        data_length = len(byte_list)
        print('File size (Bytes, without zero padding): ' + str(data_length))
        total_length = data_length + 8
        print('Total length (Bytes): ' + str(total_length))
        new_length, new_data = check_data_padding(data_length, byte_list)
        return total_length, new_data


def check_data_padding(data_length, data):
    if data_length % 2 == 1:
        data.append(0)
        g = len(data)
        return g, data
    else:
        return data_length, data


def calc_check_sum(source_port, dest_port, padded_data_length, data, source_ip, dest_ip):
    init_check_sum = format(int(0), '016b')
    init_prot_num = format(int(17), '016b')
    total_length_bits = format(int(padded_data_length), '016b')
    data_sum = sum(i for i in data)
    source_ip_bits = format(int(source_ip), '032b')
    dest_ip_bits = format(int(dest_ip), '032b')
    sick = bin(int(total_length_bits, 2) + int(data_sum) + int(init_check_sum, 2) + int(init_prot_num, 2) + int(source_ip_bits, 2) + int(dest_ip_bits, 2) + int(source_port, 2) + int(dest_port, 2))
    while len(sick) > 18:
        right_sixteen = sick[len(sick)-16:len(sick)]
        left_side = sick[2:len(sick)-16]
        sick = bin(int(right_sixteen, 2) + int(left_side, 2))
    sick = sick[2:]
    while len(sick) < 16:
        sick = sick.rjust(1+len(sick), '0')
    sick1 = ''
    for num in sick:
        if num == '0':
            sick1 = sick1 + '1'
        else:
            sick1 = sick1 + '0'
    nw = int(sick1, 2)
    print('Checksum: ' + str(hex(nw)))
    return nw


def ones_complement(n):
    # Find number of bits in
    # the given integer
    number_of_bits = (int)(math.floor(math.log(n) /
                                      math.log(2))) + 1

    # XOR the given integer with poe(2,
    # number_of_bits-
    # 1 and print the result
    return ((1 << number_of_bits) - 1) ^ n


def write_output(source_port, dest_port, new_length, check_sum, new_data, datagram_name):
    with open(datagram_name, 'wb') as write_data:
        write_data.write(bytes(source_port, 'UTF-8'))
        write_data.write(bytes('\n', 'UTF-8'))
        write_data.write(bytes(dest_port, 'UTF-8'))
        write_data.write(bytes('\n', 'UTF-8'))
        write_data.write(bytes(str(new_length), 'UTF-8'))
        write_data.write(bytes('\n', 'UTF-8'))
        write_data.write(bytes(str(check_sum), 'UTF-8'))
        write_data.write(bytes('\n', 'UTF-8'))
        binary_format = bytearray(new_data)
        write_data.write(binary_format)
        print('File is successfully written to datagram.bin')


def main():
    arguments = input()
    input_name, source_ip, dest_ip, source_port, dest_port, datagram_name = arguments.split(' ')
    print('Source port: ' + source_port)
    print('Destination port: ' + dest_port + '\n')
    big_en_source = ip_to_byte_array(source_ip)
    big_en_dest = ip_to_byte_array(dest_ip)
    print(' Big-endian IP:' + '\n' + 'Source IP: ' + big_en_source + '\n' + 'Destination IP: ' + big_en_dest)
    get_source_ip_bytes(source_ip)
    get_dest_ip_bytes(dest_ip)
    source_port_bits = format(int(source_port), '016b')
    dest_port_bits = format(int(dest_port), '016b')
    new_length, new_data = read_input_file(input_name)
    check_sum = calc_check_sum(source_port_bits, dest_port_bits, new_length, new_data, big_en_source, big_en_dest)
    write_output(source_port, dest_port, new_length, check_sum, new_data, datagram_name)
    Lab1_Encrypt.main()


if __name__ == '__main__':
    main()