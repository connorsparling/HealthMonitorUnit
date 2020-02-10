#== GLOBAL ==========================================================================================================================
import threading
import time
import queue
from log import print_log
import serialRecieve
import serialSegmentation
import numpy as np
import os
import sys, getopt
import csv

def add_to_queue(queue, item):
    if queue is not None:
        try:
            queue.put(item)
        except:
            print_log("ADD TO QUEUE ERROR")
            return False
        return True
    print_log("QUEUE IS NONE")
    return False

#== SERIAL ==========================================================================================================================
def serial(threadname, segment_queue, file_path, save_to_file):
    print_log("SERIAL THREAD WORKING")
    segment_buffer = []
    index = 0
    # if serialRecieve.LoadECGData() == 0:
    #     print_log("Something went wrong with the serial connection")

    
    with open(file_path, mode='w', newline='') as save_file:
        csv_writer = csv.writer(save_file)        
        for value in serialRecieve.LoadECGData():
            # add to segment buffer
            segment_buffer.append(value)
            # if segment buffer is 1000 then add to segment queue and clear
            if len(segment_buffer) >= 1000:
                if save_to_file:
                    csv_writer.writerow(segment_buffer)
                while True:
                    result = add_to_queue(segment_queue, segment_buffer)
                    if result:
                        break
                    print_log("SEGMENT QUEUE ADD = FALSE")
                segment_buffer = []
            # break if closing
            if not runThreads:
                break
    save_file.close()

#== CSV SAVE ========================================================================================================================
def csvSave(threadname, save_data_queue, file_path):
    print_log("CSV SAVE THREAD WORKING")
    with open(file_path, mode='w', newline='') as save_file:
        csv_writer = csv.writer(save_file)        
        while runThreads:
            try:
                item = save_data_queue.get()
                if item is not None:
                    csv_writer.writerow(item)
                    save_data_queue.task_done()
                else:
                    print_log("SAVE QUEUE ITEM IS NONE")
            except:
                pass
    save_file.close()

#== SEGMENTATION ====================================================================================================================
def segmentation(threadname, segment_queue, save_data_queue):
    print_log("SEGMENTATION THREAD WORKING")
    transfer_buffer = []
    while runThreads:
        try:
            item = segment_queue.get()
            if item is not None:
                # Segment piece of 1000 and spit out an array of 10 segments
                transfer_buffer, segments_buffer = serialSegmentation.format_data(transfer_buffer, item)
                # add to neural network queue
                for segment in segments_buffer:
                    add_to_queue(save_data_queue, segment)
                segment_queue.task_done()
            else:
                print_log("SEGMENT QUEUE ITEM IS NONE")
        except:
            pass

#== MAIN ============================================================================================================================
def main(argv):
    global runThreads
    runThreads = True
    segment_csv_file = '../Datasets/ECGSectionData.csv'
    section_csv_file = '../Datasets/ECGData.csv'

    segment_queue = queue.Queue() # Pull off segment queue for processing
    save_data_queue = queue.Queue()

    serial_t = threading.Thread(name="Serial", target=serial, args=("Serial", segment_queue, section_csv_file, True))
    saveData_t = threading.Thread(name="SaveData", target=csvSave, args=("SaveData", save_data_queue, segment_csv_file))
    segmentation_t = threading.Thread(name="Segmentation", target=segmentation, args=("Segmentation", segment_queue, save_data_queue))

    try:
        serial_t.start()
        saveData_t.start()
        segmentation_t.start()
    except KeyboardInterrupt:
        print_log("Keyboard Interrupt: Shutting down program...")
        sys.exit()
        runThreads = False
        serial_t.join()
        saveData_t.join()
        segmentation_t.join()
        print_log("Programm shutdown successfully")

if __name__ == "__main__":
    main(sys.argv[1:])