import csv
import matplotlib.pyplot as plt
import numpy as np

def plot_ecg(filename, delay=5, start=0):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #headers = next(csv_reader)
        x = range(200)
        index = 0
        for row in csv_reader:
            if index > start:
                vals = [np.float(val) for val in row]
                plt.figure(index, figsize=(15, 3))
                plt.plot(vals)
                #plt.minorticks_on()
                plt.grid(True, alpha=0.5)
                plt.ylim(0,1)
                plt.show(block=False)
                plt.pause(delay)
                plt.close(index)
            index += 1
    csv_file.close()

if __name__ == "__main__":
    #filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGSectionData.csv'
    #filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGTestSectionData.csv'
    #filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ARD.csv'
    #filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGSegmentDataConnorStanding.csv'
    filename = '/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGSegmentDataAlexSitting.csv'
    plot_ecg(filename, 1)