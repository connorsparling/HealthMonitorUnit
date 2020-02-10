''' This file is the segmentation library from the arduino to the neural network'''
import numpy as np
import time
from log import print_log
from scipy import signal
from scipy.signal import find_peaks

SAMPLE_SIZE = 200 # number of points we are putting through the neural network

def get_peaks(data):
    data = list(data)
    # hard coded value that has shown to get the best peak accuracy (lower is more peaks, higher is less peaks)
    peaks, _ = find_peaks(data, prominence=0.6) 
    return peaks

# Split take the peaks and split the segments based on the half way point between peaks
def segment_data(data):
    peaks = get_peaks(data)
    segments = []
    start = 0
    end = 0
    for j in range(len(peaks)):
        if(j == (len(peaks) - 1)):
            break
        start = j
        end = j + 1
        segments.append(int(((peaks[end] - peaks[start]) / 2) + peaks[start]))
    return segments

# Min-Max normalizing ( normalizes data between 0 and 1)
def normalize_data(data): # doesnt need to be a numpy array
    minValue = min(data)
    maxValue = max(data)
    for i in range(len(data)):
        a = data[i] - minValue
        b = maxValue - minValue
        if b == 0: # cant divide by zero
            b = 1
        data[i] = round(np.divide(a, b),6) # rounding to 6 decimal places
    return data

# resizes a sample
def resize_section(section, desired):
    newData = signal.resample(section, desired)
    return newData

def format_data(transfer_buffer, item):    
    data = normalize_data(item)
    buf = transfer_buffer + data
    segments = segment_data(buf)
    segments_buffer = []
    seg_count = len(segments)
    print_log("Retrieved {} segments".format(seg_count))

    transfer_buffer = []
    i = 0
    current_segment = []
    for index in range(len(buf)):
        if i >= seg_count:
            transfer_buffer.append(buf[index])
        else:
            current_segment.append(buf[index])
            if index == segments[i]:
                normalized_segment = resize_section(current_segment, SAMPLE_SIZE)
                segments_buffer.append(normalized_segment)
                current_segment = []
                i += 1

    # j = 0
    # for i in range(len(segments)):
    #     if i > 50:
    #         break # break if it has to many segments means theres an error
    #     segment = []
    #     while True:
    #         segment.append(data[j])
    #         j += 1
    #         if j == segments[i]:
    #             break
    #     newData = []
    #     newData = resize_section(segment, SAMPLE_SIZE)
    #     segments_buffer.append(newData)
    return transfer_buffer, segments_buffer