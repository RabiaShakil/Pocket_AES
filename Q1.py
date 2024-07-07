
def shift_row(text_block):

    d0 = text_block[0:4]
    d1 = text_block[4:8]
    d2 = text_block[8:12]
    d3 = text_block[12:16]

    shifted_row = d2 + d1 + d0 + d3
    shifted_row_hex = hex(int(shifted_row, 2))[2:].upper().zfill(4)

    return shifted_row_hex


def sub_nibbles(text_block):
    
    s_box =  {
        '0000': '1010', '0001': '0000', '0010': '1001', '0011': '1110',
        '0100': '0110', '0101': '0011', '0110': '1111', '0111': '0101',
        '1000': '0001', '1001': '1101', '1010': '1100', '1011': '0111',
        '1100': '1011', '1101': '0100', '1110': '0010', '1111': '1000'
    }

    result = ''
    for i in range(0, len(text_block), 4):
        nibble = text_block[i:i + 4]
        result += s_box[nibble]
    return result



def add_round_key(text_block, round_key):
    result = ''
    for i in range(len(text_block)):
        result += '1' if text_block[i] != round_key[i] else '0'
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


def mix_columns(text_block):
   
    c0 = int(text_block[0:4], 2)
    c1 = int(text_block[4:8], 2)
    c2 = int(text_block[8:12], 2)
    c3 = int(text_block[12:16], 2)

    d0 = multiply_in_gf(c0, 1) ^ multiply_in_gf(c1, 4)
    d1 = multiply_in_gf(c0, 4) ^ multiply_in_gf(c1, 1)
    d2 = multiply_in_gf(c2, 1) ^ multiply_in_gf(c3, 4)
    d3 = multiply_in_gf(c2, 4) ^ multiply_in_gf(c3, 1)

    result = "" + bin(d0)[2:].zfill(4) + bin(d1)[2:].zfill(4) + bin(d2)[2:].zfill(4) + bin(d3)[2:].zfill(4)
    result_hex = hex(int(result, 2))[2:].upper().zfill(4)

    return result_hex


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


if __name__ == '__main__':
    
    
    plaintext=input("Enter the  16-bit text block (hexadecimal): ")
    plaintext_binary = bin(int(plaintext, 16))[2:].zfill(16)
    
    # shift row
    row_result = shift_row(plaintext_binary)
    print("Shift Rows(" + plaintext + ") =", row_result)

    # mix columns
    mixCol_result = mix_columns(plaintext_binary)
    print("Mix Cols(" + plaintext + ") =", mixCol_result)
    
    # sub_nibbles
    sub_nibbles_result = sub_nibbles(plaintext_binary)
    print("SubNibbles(" + plaintext + ") =", hex(int(sub_nibbles_result, 2))[2:].upper().zfill(4))

    key = input("Enter the 16-bit key (hexadecimal): ")
    if len(key) != 4 or not all(c in '0123456789abcdef' for c in key):
        print("Invalid key format. Please enter a 4-digit hexadecimal key.")
        exit(1)
        
    print("GenerateRoundKeys(" + key + ") =", end=" ")

    # Generate round keys K1 and K2
    K1, K2 = generate_round_keys(bin(int(key, 16))[2:].zfill(16))
    print("(" + hex(int(K1, 2))[2:].upper().zfill(4) + ", " + hex(int(K2, 2))[2:].upper().zfill(4) + ")")

    
    


