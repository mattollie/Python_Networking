from operator import xor


def encrypt(filename):
    # find the length of the data file
    with open(filename, "rb") as file:
        data = file.read()
        # divide the length by 2 since we are reading in two bytes at a time and round up division if it is odd
        if len(data) % 2 == 0:
            a = False
            half_of_characters = len(data)/2
        elif len(data) % 2 == 1:
            a = True
            half_of_characters = len(data)/2 + 0.5
    # counter for length of the text file
    l = 1
    # list for storing the encrypted bytes
    string_list = bytearray()
    # loop for the whole text file
    while l <= half_of_characters:
        plain_text = read_data(filename)
        # counter for the amount of times the encryption algorithm is processing
        i = 0
        # split the left byte and the right byte
        split_l, split_r = split_bits(plain_text, l, half_of_characters, a)
        # loop for amount of times algorithm is processing
        while i <= 7:
            # swap the bytes
            if i == 0:
                swapped_l, swapped_r = swapped_bits(split_l, split_r)
            else:
                swapped_l, swapped_r = swapped_bits(swapped_l, after_key)
            # get the key
            key_select = key_choice(i)
            # convert to binary and xor the key and the right byte
            bin_num = bin(swapped_r)
            # get binary value of key
            key_to_int = int(key_select)
            ascii_to_binkey = bin(key_to_int)
            after_key = sxor(bin_num, ascii_to_binkey)
            i = i + 1
        l += 1
        string_list.append(swapped_l)
        string_list.append(after_key)
    # write file
    write_encrypted(string_list)


def read_data(filename):
    f = open(filename, "rb")
    return f


def split_bits(f, e, index, a):
    if e == 1:
        ven = f.read()
        l = ven[e - 1]
        if e == index:
            r = 0
        else:
            r = ven[e]
    else:
        # move the pointer
        f.seek((2 * e - 2))
        ven = f.read()
        l = ven[0]
        if e == index:
            if a == True:
                r = 0
            else:
                r = ven[1]
        else:
            r = ven[1]
    return l, r


def swapped_bits(split_l, split_r):
    swapped_l = split_r
    swapped_r = split_l
    return swapped_l, swapped_r


def key_choice(i):
    with open("Keys") as fp:
        line = fp.readlines()
        try:
            line = line[i]
        except AttributeError:
            print("Please enter 8 keys and try again")
            exit()
        except IndexError:
            print("Please enter 8 keys and try again")
            exit()
        line = line.rstrip("\n")
        return line


def sxor(a, b):
    xor_result = xor(int(a, 2), int(b, 2))
    return xor_result


def write_encrypted(iteration1):
    write_data = open("Encrypted_data", "wb")
    write_data.write(iteration1)


def main():
    filename = 'datagram.bin'
    # handle if there is no data present to encrypt
    with open(filename, "rb") as file:
        data = file.read()
        if len(data) == 0:
            print("No data provided, please select a file with data")
        else:
            encrypt(filename)
            print("Encryption written to 'Encrypted_data' file")


if __name__ == '__main__':
    main()
    exit()