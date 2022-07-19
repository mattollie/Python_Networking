from operator import xor


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


def decrypt(filename):
    # get the length of the encrypted data file
    with open(filename, "rb") as file:
        data = file.read()
        # divide by 2 since we are reading in 2 bytes at a time
        half_of_characters = len(data)/2
    l = 1
    a = False
    string_list = bytearray()
    # loop for whole data file
    while l <= half_of_characters:
        encrypted = read_encrypted(filename)
        # split the bytes
        seperated_L, seperated_R = split_bits(encrypted, l, half_of_characters, a)
        # decryption counter
        j = 0
        # key counter
        k = 7
        while j <= 7:
            # get the key
            get_key = key_choice(k)
            if j == 0:
                ascii_to_bin = bin(seperated_R)
            else:
                ascii_to_bin = bin(swapped_R)
            # get binary value of key
            key_to_int = int(get_key)
            ascii_to_binkey = bin(key_to_int)
            # xor key and right byte and then swap
            reverse_key = sxor(ascii_to_bin, ascii_to_binkey)
            if j == 0:
                swapped_L, swapped_R = swap(seperated_L, reverse_key)
            else:
                swapped_L, swapped_R = swap(swapped_L, reverse_key)
            j = j + 1
            k -= 1
        l += 1
        string_list.append(swapped_L)
        string_list.append(swapped_R)
    string_list_length = len(string_list)
    # take out extra byte at the end if data length = 0
    if string_list[string_list_length-1] == 0:
        string_list = string_list[:string_list_length-1]
    # write file
    write_decrypted(string_list)


def read_encrypted(filename):
    f = open(filename, "rb")
    return f


def swap(seperated_L, reverse_key):
    L = reverse_key
    R = seperated_L
    return L, R


def write_decrypted(iteration1):
    write_data = open("Decrypted.txt", "wb")
    write_data.write(iteration1)


def main():
    # handle if there is no data present to encrypt
    with open('Encrypted.txt', "rb") as file:
        data = file.read()
        if len(data) == 0:
            print("No data provided, please select a file with data")
        else:
            decrypt('Encrypted.txt')


if __name__ == '__main__':
    main()
    exit()