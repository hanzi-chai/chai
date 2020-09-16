import math

B = [1, 1]

for n in range(2, 31):
    B_n = 0
    for k, B_k in enumerate(B):
        B_n = B_n + math.factorial(n-1) // math.factorial(k) // math.factorial(n - 1 - k) * B_k
    B.append(B_n)

with open('Bell.txt', 'w') as f:
    for n, B_n in enumerate(B):
        f.write('%d\t%d\n' % (n, B_n))