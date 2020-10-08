an_int = 2148

a_bytes_big = an_int.to_bytes(2, 'big')
valor2 = int.from_bytes(a_bytes_big, byteorder='big') 
print(a_bytes_big)
print (valor2)