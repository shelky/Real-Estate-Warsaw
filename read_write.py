import csv

f = csv.reader(open('apartments.csv'))
print(f)
for row in f:
    print(row)
    title = row[0]
    price = int(row[1])
    print('title: ', title)
    print('price: ', price)
    print('__________')