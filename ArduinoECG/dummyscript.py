import csv

data = []

with open('Datasets/ECGData.csv') as load_file:
    csv_reader = csv.reader(load_file, delimiter=',')
    for row in csv_reader:
        for item in row:
            data.append(item)

with open('Datasets/ECGDataStream.csv', mode='w', newline='') as save_file:
    csv_writer = csv.writer(save_file)
    for item in data:
        csv_writer.writerow([item])
