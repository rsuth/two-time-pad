ciphers = []
with open('twotimepad.txt') as f:
  c = f.readline()
  while c:
    # first trim the extra stuff
    c = c[7:-1]
    # b holds the bytes
    b = []
    for i in range(0,len(c),8):
      # byte = chunk of 8 bits
      byte = c[i:i+8]
      b.append(int(byte, base=2))
    ciphers.append(b)
    c = f.readline()

def xor_byte_arrays(ba1, ba2):
  return [a ^ b for a, b in zip(ba1, ba2)]

def bit_str(ba):
  byte_string = ''
  for byte in ba:
    byte_string += "{:08b}".format(byte)
  return byte_string

def check_leading_bits(bit_string):
  for i in range(0, len(bit_string), 8):
    if bit_string[i] != '0':
      return False
  return True

pairs = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]

for p in pairs:
  xord = bit_str(xor_byte_arrays(ciphers[p[0]],ciphers[p[1]]))
  print(f'pair: {p} leading bits match? {check_leading_bits(xord)}')

def guess(guess, pair):
  m_x_m = xor_byte_arrays(ciphers[pair[0]], ciphers[pair[1]])
  guess = [ord(g) for g in guess]
  ret = []
  for i in range(len(m_x_m)-len(guess)):
    s = []
    for j in range(len(guess)):
      x = guess[j] ^ m_x_m[j+i]
      s.append(x)

    # check for out of range ascii chars.
    good = True
    for c in s:
      if c < 32 or c > 127:
        good = False
        break
    if good:
      ret.append((i, ''.join(chr(c) for c in s)))
  return ret

print(f"message length:{len(xor_byte_arrays(ciphers[1], ciphers[3]))}")

while True:
  results = guess(input("Enter Guess:"), (1,3))
  for r in results:
    print(f"{r[0]}: {r[1]}")
