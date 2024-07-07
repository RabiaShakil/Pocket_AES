def shift_row(text):
    
    d0 = text[0:4]
    d1 = text[4:8]
    d2 = text[8:12]
    d3 = text[12:16]

    shifted_row = d2 + d1 + d0 + d3
    return shifted_row




def sub_nibbles(block):
    
    s_box = {
        '0000': '1010', '0001': '0000', '0010': '1001', '0011': '1110',
        '0100': '0110', '0101': '0011', '0110': '1111', '0111': '0101',
        '1000': '0001', '1001': '1101', '1010': '1100', '1011': '0111',
        '1100': '1011', '1101': '0100', '1110': '0010', '1111': '1000'
    }
    result = ''
    for i in range(0, len(block), 4):
        # Extract each 4-bit nibble from the block
        nibble = block[i:i + 4]
        result += s_box[nibble]
    return result


def add_round_key(block, round_key):
    result = ''
    for i in range(len(block)):
        # XOR each bit of the block and round key
        result += '1' if block[i] != round_key[i] else '0'
    return result


def generate_round_keys(key):
    
    Rcon1 = '1110'
    Rcon2 = '1010'

    w0 = key[0:4]
    w1 = key[4:8]
    w2 = key[8:12]
    w3 = key[12:16]

    w4 = format(int(w0, 2) ^ int(sub_nibbles(w3), 2) ^ int(Rcon1, 2), '04b')
    w5 = format(int(w1, 2) ^ int(w4, 2), '04b')
    w6 = format(int(w2, 2) ^ int(w5, 2), '04b')
    w7 = format(int(w3, 2) ^ int(w6, 2), '04b')

    w8 = format(int(w4, 2) ^ int(sub_nibbles(w7), 2) ^ int(Rcon2, 2), '04b')
    w9 = format(int(w5, 2) ^ int(w8, 2), '04b')
    w10 = format(int(w6, 2) ^ int(w9, 2), '04b')
    w11 = format(int(w7, 2) ^ int(w10, 2), '04b')

    Key1 = w4 + w5 + w6 + w7
    Key2 = w8 + w9 + w10 + w11

    return Key1, Key2


def inverse_sub_nibbles(block):
    
    inverse_s_box = {
        '1010': '0000', '0000': '0001', '1001': '0010', '1110': '0011',
        '0110': '0100', '0011': '0101', '1111': '0110', '0101': '0111',
        '0001': '1000', '1101': '1001', '1100': '1010', '0111': '1011',
        '1011': '1100', '0100': '1101', '0010': '1110', '1000': '1111'
    }
    result = ''
    for i in range(0, len(block), 4):
        nibble = block[i:i + 4]
        result += inverse_s_box[nibble]
    return result


def multiply_in_gf(a, b):
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x10:
            a ^= 0x13  
        b >>= 1
    return result & 0x0F  
 

def inverse_mix_columns(block):
    
    inverse_mix_columns_matrix = [
        [9, 2],
        [2, 9]
    ]   
  
    c0 = int(block[0:4], 2)
    c1 = int(block[4:8], 2)
    c2 = int(block[8:12], 2)
    c3 = int(block[12:16], 2)

    d0 = multiply_in_gf(c0, 9) ^ multiply_in_gf(c1, 2)
    d1 = multiply_in_gf(c1, 9) ^ multiply_in_gf(c0, 2)
    d2 = multiply_in_gf(c2, 9) ^ multiply_in_gf(c3, 2)
    d3 = multiply_in_gf(c3, 9) ^ multiply_in_gf(c2, 2)

    result = (
            bin(d0)[2:].zfill(4) +
            bin(d1)[2:].zfill(4) +
            bin(d2)[2:].zfill(4) +
            bin(d3)[2:].zfill(4)
    )
    
    return result


# Function to perform decryption
def decrypt_block(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()

    ciphertext_binary = bin(int(ciphertext, 16))[2:].zfill(16)

    key_binary = bin(int(key, 16))[2:].zfill(16)

    Key1, Key2 = generate_round_keys(key_binary)

    text_block = ciphertext_binary

    # Shift Row 1st time
    text_block = shift_row(text_block)

    # Add round key 2
    text_block = add_round_key(text_block, Key2)

    # Inverse of the SubNibbles 1st time
    text_block = inverse_sub_nibbles(text_block)

    # Shift Row 2nd time
    text_block = shift_row(text_block)

    # Inverse of the last MixColumns operation
    text_block = inverse_mix_columns(text_block)

    # Add round key 1
    text_block = add_round_key(text_block, Key1)

    # Inverse of the SubNibbles 2nd time
    text_block = inverse_sub_nibbles(text_block)
    decrypted_text_hex = hex(int(text_block, 2))[2:].upper().zfill(4)
   
    return decrypted_text_hex


if __name__ == '__main__':
    
    ciphertext = input("Enter the ciphertext block: ")
    if not all(c in '0123456789abcdef' for c in ciphertext):
        print("Invalid input. Please enter a valid 16-bit hexadecimal number.")
        
        
    key = input("Enter the key: ")
    if not all(c in '0123456789abcdef' for c in key):
        print("Invalid key. Please enter a valid 16-bit hexadecimal number.")

    decrypted_block = decrypt_block(ciphertext, key)
    
    print("Decrypted block:", decrypted_block)