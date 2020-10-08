an_int = 2148
en_int = 100
a_bytes_big = an_int.to_bytes(3, 'big')
a = ""
a +=a_bytes_big
print (a)
print (a_bytes_big)