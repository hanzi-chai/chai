import yaml

WEN = yaml.load(open('文.yaml'), Loader=yaml.BaseLoader)

# l = []
# for char, strokeList in WEN.items():
#     l.append((len(strokeList), char))

# print(sorted(l, reverse=True)[:50])

l = []
for char, strokeList in WEN.items():
    for stroke in strokeList:
        l.append(stroke[0])

for i in set(l):
    print(i)