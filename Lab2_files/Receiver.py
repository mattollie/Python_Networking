import struct
from Lab1_files import Lab1_Decrypt


def ip_to_byte_array(ip):
    words = ip.split('.')
    int_list = []
    for num in words:
        int_list.append(int(num))
    c = bytes(int_list)
    bigendian = struct.unpack('>I', c)
    return '{}'.format(bigendian[0])


def read_input_file():
    with open('Decrypted_data', 'rb') as filename:
        ven = filename.read()
        byte_list = []
        startFromLine = 5  # or whatever line I need to jump to
        linesCounter = 1
        for line in ven:
            if linesCounter < startFromLine:
                if line == 10:
                    linesCounter += 1
            else:
                byte_list.append(line)
        data_length = len(byte_list)
        total_length = data_length + 7
        print('Total length (Bytes): ' + str(total_length))
        return byte_list


def check_data_padding(data_length, data):
    if data_length % 2 == 1:
        data.append(0)
        g = len(data)
        return g, data
    else:
        return data_length, data


def calc_check_sum(source_port, dest_port, padded_data_length, data, source_ip, dest_ip, one_comp_check):
    init_check_sum = format(int(0), '016b')
    init_prot_num = format(int(17), '016b')
    total_length_bits = format(int(padded_data_length), '016b')
    data_sum = sum(i for i in data)
    source_ip_bits = format(int(source_ip), '032b')
    dest_ip_bits = format(int(dest_ip), '032b')
    sick = bin(int(total_length_bits, 2) + int(data_sum) + int(init_check_sum, 2) + int(init_prot_num, 2) + int(source_ip_bits,2) + int(dest_ip_bits,2) + int(source_port) + int(dest_port))
    while len(sick) > 18:
        right_sixteen = sick[len(sick) - 16:len(sick)]
        left_side = sick[2:len(sick) - 16]
        sick = bin(int(right_sixteen, 2) + int(left_side, 2))
    nw = int(sick, 2)
    let = nw + int(one_comp_check)
    sure = hex(let)
    print('Checksum: ' + str(hex(let)))
    if sure == '0xffff':
        print('Checksum is correct!')
    else:
        print('Checksum error!')
        exit()


def write_output(data):
    with open('Output_file', 'wb') as write_data:
        binary_format = bytearray(data)
        write_data.write(binary_format)
        print('File is successfully written to Output_file')


def main():
    arguments = input()
    source_ip, dest_ip, datagram_name = arguments.split(' ')
    big_en_source = ip_to_byte_array(source_ip)
    big_en_dest = ip_to_byte_array(dest_ip)
    print('Source IP: ' + big_en_source + '\n' + 'Destination IP: ' + big_en_dest)
    Lab1_Decrypt.main()
    with open('Decrypted_data', 'rb') as udp:
        udpdata = udp.readlines(16)
        source_port = udpdata[0]
        dest_port = udpdata[1]
        total_length = udpdata[2]
        check_sum = udpdata[3]
    source_port = int(source_port.rstrip(b'\n'))
    dest_port = int(dest_port.rstrip(b'\n'))
    total_length = int(total_length.rstrip(b'\n'))
    check_sum = int(check_sum.rstrip(b'\n'))
    data = read_input_file()
    calc_check_sum(source_port, dest_port, total_length, data, big_en_source, big_en_dest, check_sum)
    write_output(data)


if __name__ == '__main__':
    main()