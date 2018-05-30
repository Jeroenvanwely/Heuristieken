import CSV

alles = int(0)

for i in range(7):
    with open(‘h_results’ +int(i) + ‘.csv’) as f:
        reader = csv.reader(f)
        for row in reader:
            alles += row

print(alles)