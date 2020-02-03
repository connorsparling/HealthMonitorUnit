''' This file is the segmentation library from the arduino to the neural network'''

import numpy as np
from scipy.signal import find_peaks

def get_peaks(data):
    data = list(data)
    peaks, _ = find_peaks(data, prominence=150)
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

# Min-Max normalizing
def normalize_data(data): # doesnt need to be a numpy array
    minValue = min(data)
    maxValue = max(data)
    for i in range(len(data)):
        a = data[i] - minValue
        b = maxValue - minValue
        data[i] = a / b 
    return data

def normalize_X(section, desired):
    return sig.resample(section, desired)

