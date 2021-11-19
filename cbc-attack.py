from Crypto.Util.number import *
from Crypto.Cipher import AES
from oracle import Oracle_Connect, Mac, Vrfy

import binascii

AES_key = "a9c3ffe462a9948c3e36b08d83a83e45"

def hex_to_str(input):
    str_value = input.decode("hex")

    print("key: %s"%(input))
    print("------------------------------------")
    
    return str_value

AES_key = hex_to_str(AES_key)

iv = "\x00" * 16
BLOCKSIZE = 16

def CBC_MAC(plaintext, length):
    msg_tag = Mac(plaintext, length)
    
  
    return msg_tag

def using_format(msg):
    return "".join(format(x, "02x") for x in msg)

def print_result(output):
    if(output == 1):
        print("Output: Verified")
    else:
        print("Output: Failed!!!")

def xor_strings(s1, s2):
	assert len(s1) == len(s2)
	ct = "".join([chr(ord(s1[i]) ^ ord(s2[i])) for i in range(len(s1))])
	return ct

def exploit(msg1, msg2, tag1, tag2):
    
    print("Exploit")
    print("------------------------------------")

    msg2_1 = msg2[:16]
    msg2_2 = msg2[16:32]
    msg2_3 = msg2[32:48]
    msg2_4 = msg2[48:64]

    #CBC_MAC(msg1|| (msg2_1 \xor tag1 \xor IV) || msg2_2 || ... || msg2_n)
    iv = "\x00" * 16

    hex_tag = tag1.decode("hex")

    out = xor_strings(msg2_1, hex_tag)
    
    out = xor_strings(out, iv)
    
    fmsg = msg1 + out + msg2_2 + msg2_3 + msg2_4

    print("fmsg: %s"%(fmsg))

    # message2 tag2 == forge message tag
    ftag = tag2
    hex_ftag = binascii.hexlify(ftag)
    print("ftag: %s"%(hex_ftag))

    output = Vrfy(fmsg, len(fmsg), tag2)
    print_result(output)    

    return ftag


if __name__ == '__main__':
    
    Oracle_Connect()

    msg1 = "I, the server, hereby agree that"
    msg2 = " I will pay $100 to this student"
    
    tag1 = CBC_MAC(msg1, len(msg1))
    hex_tag1 = binascii.hexlify(tag1)
    print("tag: %s"%(hex_tag1))

    output = Vrfy(msg1, len(msg1), tag1)
    print_result(output)    
    print("-------------------------------------")
    
    tag2 = CBC_MAC(msg2, len(msg2))
    print("msg: %s"%(msg2))
    hex_tag2 = binascii.hexlify(tag2)
    print("tag: %s"%(hex_tag2))

    output = Vrfy(msg2, len(msg2), tag2)
    print_result(output)    

    print("-------------------------------------")

    fmsg = "I, the server, hereby agree that I will pay $100 to this student"
    
    ftag = CBC_MAC(fmsg, len(fmsg))
    print("msg: %s"%(fmsg))
    hex_ftag = binascii.hexlify(ftag)
    print("tag: %s"%(hex_ftag))
    print("CBC-MAC server refused to provide a tag for the forge message.")
    print("====================================")
    print("Launching length extension attack...")
    #Exploit
    print("------------------------------------")
    
    ftag = exploit(msg1, msg2, hex_tag1, tag2)

    
    