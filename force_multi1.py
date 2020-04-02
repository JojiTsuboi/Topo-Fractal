import csv
b = list()

with open('force.csv') as f:
    # a = f.read()
    a = csv.reader(f)
    for row in a:
        b.append(row)
# print(a[2])
print(b)