import json
import csv


with open('category.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    data = {'category': []}
    for row in reader:
        data['category'].append(
            {
                'id': row[0],
                'name': row[1],
                'slug': row[2]
            }
        )
    print(data)

with open('category.json', 'w') as f:
    json.dump(data, f, indent=4)
