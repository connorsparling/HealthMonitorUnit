import sys, getopt
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from sklearn.preprocessing import normalize
import scipy.signal as sig

DEFAULT_LEAD = "MLII"

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
        for filename in os.listdir(directory)[:6]:
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

class SectionPlot():
    def next(self, event):
        plt.close(self.fig)
        self.index = min(self.sections.shape[0], self.index+1)
        self.display_plot()

    def prev(self, event):
        plt.close(self.fig)
        self.index = max(0, self.index-1)
        self.display_plot()

    def exit(self, event):
        plt.close(self.fig)

    def display_plot(self):
        self.fig, self.plot = plt.subplots(figsize=(5, 4))
        detail_name = str(self.index)
        if self.types is not None:
            detail_name = self.types[self.index]
        self.fig.canvas.set_window_title("{}: {}".format(self.name, detail_name))
        plt.subplots_adjust(bottom=0.2)

        plt.plot(self.sections[self.index])
        plt.minorticks_on()
        plt.grid(True, alpha=0.5)

        axprev = plt.axes([0.29, 0.05, 0.2, 0.075])
        axnext = plt.axes([0.5, 0.05, 0.2, 0.075])
        axexit = plt.axes([0.71, 0.05, 0.2, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.next)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(self.prev)
        bexit = Button(axexit, 'Exit')
        bexit.on_clicked(self.exit)

        plt.show()

    def __init__(self, name, sections, types=None):
        self.name = name
        self.sections = sections
        self.types = types
        self.index = 0
        self.display_plot()

class RangePlot():
    def next(self, event):
        self.index = min(self.dataX.shape[0]-self.length, self.index+self.length)
        self.update()

    def prev(self, event):
        self.index = max(0, self.index-self.length)
        self.update()

    def update(self):
        self.plot.set_xlim(self.index, self.index+self.length)
        self.data_plot.set_ydata(self.dataY[self.index:self.index+self.length])
        self.data_plot.set_xdata(self.dataX[self.index:self.index+self.length])
        plt.draw()

    def exit(self, event):
        plt.close(self.fig)

    def __init__(self, name, data, peaks, length=1000, start=0):
        self.fig, self.plot = plt.subplots(figsize=(15, 4))
        self.fig.canvas.set_window_title(name)
        plt.subplots_adjust(bottom=0.2)

        self.index = start
        self.length = length

        self.plot.set_xlim(self.index, self.index+self.length)
        self.plot.set_ylim(-1, 1)

        self.dataY = data
        self.dataX = np.arange(0.0, float(data.shape[0]))

        plotPY = []
        for p in peaks:
            plotPY.append(data[p])
        self.peaksY = np.array(plotPY)
        self.peaksX = peaks

        self.data_plot, = plt.plot(self.dataX[self.index:self.index+self.length], self.dataY[self.index:self.index+self.length])
        self.peak_plot, = self.plot.plot(self.peaksX, self.peaksY, c="orange", marker="o", ls="")

        axprev = plt.axes([0.59, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.7, 0.05, 0.1, 0.075])
        axexit = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.next)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(self.prev)
        bexit = Button(axexit, 'Exit')
        bexit.on_clicked(self.exit)

        plt.show()

def main(argv):
    filename = None
    lead_placement = "MLII"
    plot_type = None
    downsample_amount = None
    split_location = None
    function_format = "MITBIH_preprocess.py [-f <input_file>] [-l <lead_placement>] [-d <downsample_amount>] [-p <plot_type>] [-s <split_location>]"
    try:
        opts, args = getopt.getopt(argv,"hd:f:l:p:s:",["file=", "lead=", "plot=", "downsample=", "split="])
    except getopt.GetoptError:
        print("INCORRECT FORMAT: \"" + function_format + "\"")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(function_format)
            sys.exit()
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-l", "--lead"):
            lead_placement = arg
        elif opt in ("-d", "--downsample"):
            downsample_amount = int(arg)
        elif opt in ("-p", "--plot"):
            plot_type = arg
        elif opt in ("-s", "--split"):
            split_location = arg

    if lead_placement is None:
        print("Please input a lead placement position")
        sys.exit()

    if split_location is not None and downsample_amount is not None:
        print("Cannot downsample and split graph into sections")
        sys.exit()

    labels, data, peaks, heartbeat_types = load_data(filename, lead_placement)
    data = normalize_data(data)

    #peaks = get_peaks(data) # OLD METHOD

    sections = None
    if split_location == "peak":
        sections = split_peak_to_peak(data, peaks, 200)
        heartbeat_types = None #******** CAREFULL
    elif split_location == "center":
        sections, heartbeat_types = split_center_peak(data, peaks, heartbeat_types, 200)

    if downsample_amount is not None:
        data, peaks = downsample(data, peaks, downsample_amount)

    if plot_type == "range":
        for i in range(data.shape[0]):
            RangePlot("Label {}".format(labels[i]), data[i], peaks[i], length=2000)
    if plot_type == "section":
        if sections is None:
            print("Please select a split location ('peak' or 'center')")
        for i in range(sections.shape[0]):
            SectionPlot("Label {}".format(labels[i]), sections[i], types=heartbeat_types[i])

# Example Command:
#   python3 preprocessData/MIT-BIH_preprocess.py -f Datasets/mitbih-database -l MLII -p section -s center
#   python3 preprocessData/MIT-BIH_preprocess.py -f Datasets/mitbih-database -l MLII -p range -d 2
            
        
if __name__ == '__main__':
	main(sys.argv[1:])