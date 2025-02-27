import csv

csvfile = open("nu.csv")
reader = csv.reader(csvfile, delimiter=',')
rows = []
pays = {}
for i,row in enumerate(reader):
    if i==0: continue
    rows.append(row)
    pays[row[1]] = 0.0

for row in rows:
    pays[row[1]] += float(row[2])

for k,v in sorted(pays.items(), key=lambda item: item[1], reverse=True):
    print(f"{k}:   {v:.2f}")

