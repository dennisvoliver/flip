import csv

csv_file = open('pets.csv', 'r')
csv_reader = csv.reader(csv_file)
for i in csv_reader:
    print(i)

