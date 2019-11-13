# Libraries
import pandas as pd # used for handling the dataset
import matplotlib.pyplot as plt
import time
import numpy as np

def mitbh_process(in_file):
    df = pd.read_csv(in_file)
    X = df.iloc[:, :-1].values
    Y = df.iloc[:, -1].values
    return X, Y

def split_data(data, percent):
    if percent >= 0 and percent <= 1:
        point = int(len(data)*percent)
        return data[:point], data[point:]

def ptbdb_process(normal, abnormal):
    train_percent = 0.9
    ptbdb_normal_train, ptbdb_normal_test = split_data(pd.read_csv(normal).iloc[:, :-1].values, train_percent)
    ptbdb_abnormal_train, ptbdb_abnormal_test = split_data(pd.read_csv(abnormal).iloc[:, :-1].values, train_percent)

    ptbdp_train_X = np.concatenate((ptbdb_normal_train, ptbdb_abnormal_train))
    ptbdp_test_X = np.concatenate((ptbdb_normal_test, ptbdb_abnormal_test))

    ptbdp_train_Y = np.concatenate((np.zeros(len(ptbdb_normal_train)), np.ones(len(ptbdb_abnormal_train))))
    ptbdp_test_Y = np.concatenate((np.zeros(len(ptbdb_normal_test)), np.ones(len(ptbdb_abnormal_test))))

    return ptbdp_train_X, ptbdp_train_Y, ptbdp_test_X, ptbdp_test_Y

def display_plots(X, Y, count, length=10, start=0, delay=0.2):
    plt.interactive(False)
    i = start
    while i < len(Y):
        x = np.trim_zeros(X[i])
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
    mitbih_train_X, mitbih_train_Y = mitbh_process('mitbih_train.csv')
    mitbih_test_X, mitbih_test_Y = mitbh_process('mitbih_test.csv')
    ptbdp_train_X, ptbdp_train_Y, ptbdp_test_X, ptbdp_test_Y = ptbdb_process('ptbdb_normal.csv', 'ptbdb_abnormal.csv')

    display_plots(ptbdp_test_X, ptbdp_test_Y, 100, length=5, delay=3)

if __name__ == '__main__':
	main()