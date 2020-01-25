import sys
import csv
import numpy as np
import pandas as pd


def exit_app(event):
    sys.exit(0)

def load_data_from_csv(filename, lead_placement):
    data = []
    column_name = "'{}'".format(lead_placement)
    if filename is not None:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader)
            if column_name in headers:
                index = headers.index(column_name)
                for row in csv_reader:
                    data.append(float(row[index]))
        csv_file.close()
    if len(data) > 0:
        return np.array(data)
    return None

def load_data_time_from_csv(filename, lead_placement):
    data = []
    column_data = "'{}'".format(lead_placement)
    if filename is not None:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader)
            if column_data in headers:
                data_index = headers.index(column_data)
                for row in csv_reader:
                    data.append(float(row[data_index]))        
        csv_file.close()
    
    time = np.arange(0,len(data),1)
    if len(data) > 0:
        return np.array(time), np.array(data)
    return None

def load_from_mitbh_csv(file):
    df = pd.read_csv(file)
    X = df.iloc[:, :-1].values
    Y = df.iloc[:, -1].values
    return X, Y

def load_data_from_txt(filename):
        peaks = []
        heartbeat_types = []
        if filename is not None:
            with open(filename) as txt_file:
                for i, line in enumerate(txt_file):
                    data = line.split(" ")
                    if i > 1:
                        peak = None
                        heartbeat_type = None
                        j = 0
                        for d in data:
                            if d != "":
                                j += 1
                                if j == 2:
                                    peak = int(d)
                                elif j == 3:
                                    heartbeat_type = d
                                    break
                        peaks.append(peak)
                        heartbeat_types.append(heartbeat_type)
            txt_file.close()
        
        if len(peaks) > 0:
            return peaks, heartbeat_types
        return None, None

def load_data(directory, lead_placement):
    data = []
    labels = []
    peaks = []
    heartbeat_types = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                label = filename[:-4]
                d = load_data_from_csv(os.path.join(directory, filename), lead_placement)
                if d is not None:
                    print("Label {}: {}".format(label, d.shape))
                    anno_file = os.path.join(directory, str(label) + "annotations.txt")
                    p, ht = load_data_from_txt(anno_file)
                    if p is not None:
                        data.append(d)
                        labels.append(label)
                        peaks.append(p)
                        heartbeat_types.append(ht)
                        continue
                print("Label {} does not contain \"{}\"".format(label, lead_placement))
    return labels, np.array(data), peaks, heartbeat_types