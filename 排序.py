with open('字.yaml', 'r') as f:
    l = sorted([line.strip('\n') for line in f], key = lambda x: len(x.split(':')[0]) * 1000000 + ord(x[0]))

with open('字.yaml', 'w') as f:
    f.write('\n'.join(l))