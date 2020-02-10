import csv
import serialSegmentation
import numpy as np
import matplotlib.pyplot as plt

def plot(index, vals):
    plt.figure(index, figsize=(15, 3))
    plt.plot(vals)
    #plt.minorticks_on()
    plt.grid(True, alpha=0.5)
    plt.show(block=False)
    plt.pause(5)
    plt.close(index)

load_filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGSectionData.csv'
save_filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGTestSectionData.csv'
out_segments = []
transfer_buffer = []
index = 0
with open(load_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        item = [np.float(a) for a in row]
        transfer_buffer, segments_buffer = serialSegmentation.format_data(transfer_buffer, item)
        for segment in segments_buffer:
            #plot(index, segment)
            out_segments.append(segment)
            index += 1
csv_file.close()


with open(save_filename, mode='w', newline='') as save_file:
    csv_writer = csv.writer(save_file)
    for segment in out_segments:
        csv_writer.writerow(segment)
save_file.close()
#plotECGData.plot_ecg(save_filename)