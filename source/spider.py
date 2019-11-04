with open('GB.txt', 'r') as f:
    l = [str(hex(ord(line.strip('\r\n'))))[2:] for line in f]

print(l)