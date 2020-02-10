import csv

data = []
print("Loading section data...")
with open("../Datasets/SectionData.csv") as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter=',')
    for row in csv_reader1:
        data.append(row)
csv_file1.close()

print("Loading ECG section data...")
with open("../Datasets/ECGSectionData.csv") as csv_file2:
    csv_reader2 = csv.reader(csv_file2, delimiter=',')
    for row in csv_reader2:
        if row[-1] == 'Y':
            item = row[:-1] + ['ecg', 'N']
            data.append(item)
csv_file2.close()

print("Saving combined data...")
with open("../Datasets/CombineData.csv", mode='w', newline='') as save_file:
    csv_writer = csv.writer(save_file)
    for item in data:
        csv_writer.writerow(item)