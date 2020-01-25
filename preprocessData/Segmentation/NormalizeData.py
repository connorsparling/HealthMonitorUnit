import numpy as np
import scipy.signal as sig
from sklearn.preprocessing import normalize

def normalize_data(data):
    for i in range(data.shape[0]):
        data[i] = np.subtract(data[i], np.median(data[i]))
        data[i] = np.divide(data[i], data[i].max())#np.max(data[i].max(), np.abs(data[i].min())))
    return data

def downsample(data, peaks, amount):
    new_data = data[:,range(0, data.shape[1], amount)]
    new_peaks = [[int(p / amount) for p in local_peaks] for local_peaks in peaks]
    print("From {} to {}".format(data.shape, new_data.shape))
    return new_data, new_peaks

def get_peaks(data):
    peaks = []
    for d in data:
        p = sig.find_peaks(d, prominence=0.35, wlen=10)
        peaks.append(p[0])
    return peaks

def normalize_X(section, desired):
    return sig.resample(section, desired)

def split_peak_to_peak(data, peaks, length):
    sections = []
    for i in range(data.shape[0]):
        last_peak = peaks[i][0]
        local_sections = []
        for p in peaks[i][1:]:
            section = data[i][last_peak:p]
            local_sections.append(normalize_X(section, length))
            last_peak = p
        sections.append(np.array(local_sections))
    return np.array(sections)

def split_center_peak(data, peaks, heartbeat_types, length):
    sections = []
    types = []
    for i in range(data.shape[0]):
        last_middle = int(peaks[i][0] + (peaks[i][1] - peaks[i][0])/2)
        last_peak = peaks[i][1]
        local_sections = []
        local_types = []
        index = 1
        for p in peaks[i][2:]:
            middle = int(last_peak + (p - last_peak)/2)
            section = data[i][last_middle:middle]
            local_sections.append(normalize_X(section, length))
            local_types.append(heartbeat_types[i][index])
            index += 1
            last_peak = p
            last_middle = middle
        sections.append(np.array(local_sections))
        types.append(local_types)
    return np.array(sections), types
