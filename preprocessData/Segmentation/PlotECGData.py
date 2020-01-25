# Libraries
import pandas as pd # used for handling the dataset
import matplotlib.pyplot as plt
import time
import numpy as np
import FileHandler as filer
from scipy.signal import find_peaks
import NormalizeData as normdata

def split_data(data, percent):
    if percent >= 0 and percent <= 1:
        point = int(len(data) * percent)
        return data[:point], data[point:]

def display_plots(X, Y, count, length=10, start=0, delay=0.2):
    plt.interactive(False)
    i = start
    while i < len(Y):
        x = np.trim_zeros(X[i])
        x = X[i]
        y = Y[i]
        plt.figure(i, figsize=(15, 3))
        plt.title("Type: {}".format(int(y)))
        for j in range(length-1):
           x = np.concatenate((x, np.trim_zeros(X[i+j+1])))
        plt.plot(x)
        plt.minorticks_on()
        plt.grid(True, alpha=0.5)
        #plt.plot(x,x*2, color='purple', marker='o')
        plt.show(block=False)
        plt.pause(delay)
        plt.close(i)
        i += count

def static_data_plot(X,Y):
    data = []
    data = list(Y)
    plt.figure(figsize=(15,3))
    plt.plot(data)
    # Find peaks
    peaks, _ = find_peaks(data, 1100)
    print(peaks)
    plt.plot(peaks, Y[peaks], "x") 
    #plt.plot(np.zeros_like(Y), "--", color="gray") 
    plt.show(block=False)
    plt.xlim(0,1500)
    plt.ylim(850,1250)
    plt.show()

def get_peaks(data):
    data = list(data)
    peaks, _ = find_peaks(data, 1100)
    return peaks

def segment_data(data):
    peaks = get_peaks(data)
    segments = []
    start = 0
    end = 0
    print(peaks)
    first = False
    for j in range(len(peaks)):
        #print(peaks[j])
        if(j == (len(peaks) - 1)):
            break
        start = j
        end = j + 1

        if first == False:
            segments.append(peaks[end] - peaks[start])
            first = True
        else:
            segments.append((peaks[end] - peaks[start]))
    print(peaks[1] - peaks[0])
    return segments

def display_segments(data, segments):
    plt.interactive(False)
    count = 10
    delay = 3
    i = 0
    j = 0
    while(i < count):
        display_data = []
        for j in range(len(data)):
            display_data.append(data[j])
            if j == segments[i]:
                break
        plt.figure(i, figsize=(10,3))
        plt.show(block=False)
        plt.plot(display_data)
        plt.xlim(0,300)
        plt.ylim(850,1250)
        plt.minorticks_on()
        plt.grid(True, alpha=0.5)
        plt.pause(delay)
        plt.close(i)
        i += 1
        j = segments[i]

def static_segments(data, segments):
    plt.interactive(False)
    delay = 3
    j = 0
    display_data = []
    segment = 370 - 77
    print(segments[0])
    for j in range(len(data)):
        if j == segment:
            break
        display_data.append(data[j])
        
    plt.figure(1, figsize=(10,3))
    plt.plot(display_data)
    plt.xlim(0,300)
    plt.ylim(850,1250)
    plt.minorticks_on()
    plt.grid(True, alpha=0.5)
    plt.show()
    
def display_plots(X, Y, count, length=10, start=0, delay=0.2):
    plt.interactive(False)
    i = start
    while i < len(Y):
        x = np.trim_zeros(X[i])
        x = X[i]
        y = Y[i]
        plt.figure(i, figsize=(15, 3))
        plt.title("Type: {}".format(int(y)))
        for j in range(length-1):
           x = np.concatenate((x, np.trim_zeros(X[i+j+1])))
        plt.plot(x)
        plt.minorticks_on()
        plt.grid(True, alpha=0.5)
        plt.show(block=False)
        plt.pause(delay)
        plt.close(i)
        i += count
    
def main():
    #import data
    '''train_X, train_Y = filer.load_from_mitbh_csv('data/mitbih_train.csv')
    test_X, test_Y = filer.load_from_mitbh_csv('data/mitbih_test.csv')
    sample_data = filer.load_data_from_csv('data/100.csv')
'''
    time, data = filer.load_data_time_from_csv('data/100.csv','MLII')
    #data = normdata.normalize_data(data)
    #print(time)
    #print(data)
    #display_plots(time, data, 100, length=10, delay=2, start=15000)
    
    #static_data_plot(time, data)
    segments = segment_data(data)
    #print(segments)
    display_segments(data,segments)


if __name__ == '__main__':
    main()