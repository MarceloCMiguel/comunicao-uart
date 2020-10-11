import crcmod
an_int = 0
payload= bytes([7]*10)
a_bytes_big = an_int.to_bytes(1, 'big')
crc16_func = crcmod.mkCrcFun(0x11021, initCrc=0, xorOut=0xFFFFFFFF)
crc = crc_out = crc16_func(payload).to_bytes(2, "big")
print(crc)
