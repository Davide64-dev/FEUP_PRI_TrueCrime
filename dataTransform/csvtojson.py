import csv
import json

csvFilePath = '../dataset/true_crime_channel_stats.csv'
jsonFilePath = '../dataset/true_crime.json'

data = {}

with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for i, rows in enumerate(csvReader):
        # Convert rows to a dictionary but skip the first column
        rows = {key: value for key, value in rows.items() if key != ''}  # Skip the first (useless) column
        data[i] = rows

with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))
