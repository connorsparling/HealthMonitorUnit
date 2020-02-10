import csv
import matplotlib.pyplot as plt
import numpy as np

delay = 5

with open('/Users/connorsparling/Documents/GitHub/HealthMonitorUnit/Datasets/ECGSectionData.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #headers = next(csv_reader)
    x = range(200)
    index = 0
    for row in csv_reader:
        vals = [np.float(val) for val in row]
        plt.figure(index, figsize=(15, 3))
        plt.plot(vals)
        #plt.minorticks_on()
        plt.grid(True, alpha=0.5)
        plt.show(block=False)
        plt.pause(delay)
        plt.close(index)
        index += 1
csv_file.close()