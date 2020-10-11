an_int = 0
a_bytes_big = an_int.to_bytes(1, 'big')
print (bytes([7])*10)
crc_fake = 10
h8_h9 = crc_fake.to_bytes(2,'big')
print (h8_h9)
print (bytes([7])*10)
bla=[1]
print (bla[1])
