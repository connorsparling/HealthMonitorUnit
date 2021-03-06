import serial
import time
import csv
from sys import platform
from log import print_log
import socketio
import asyncio
import time
import numpy as np
import ctypes
import random

# filename
FILENAME = "../Datasets/ECGDataStream.csv"

#Packet Constants
PKT_START1 = b'\x0A'
PKT_START2 = b'\xFA'
PKT_STOP = b'\x0B'

# Packet Validation
STATE_INIT = 0
STATE_SOF1_FOUND = 1
STATE_SOF2_FOUND = 2
STATE_PKTLEN_FOUND = 3 

# CMD IF Packet Indices
CMDIF_IND_LEN = 2
CMDIF_IND_LEN_MSB = 3
CMDIF_IND_PKTTYPE = 4
CMDIF_PKT_OVERHEAD = 5

# Packet Related variables
rx_state = 0 # To check state of the packet
pkt_pos_counter = 0 # Packet counter
pkt_len = 0 # To store the packet length 
data_counter = 0 # Data counter
pkt_pktType = 0 # Store the packet type

#pkt_data_counter = [0] * 1000 # Buffer to store the data from the packet
#pkt_data_counter = np.array([0] * 1000, dtype=np.int8)
#pkt_data_counter = np.empty(1000, dtype = np.int8)
pkt_data_counter = bytearray()
#print(pkt_data_counter)
#pkt_ecg_bytes = np.empty(4, dtype=np.int8)
#pkt_resp_bytes = np.empty(4, dtype=np.int8)
pkt_ecg_bytes = bytearray() # Buffer to hold ECG data
pkt_resp_bytes = bytearray() # Buffer to hold respiration data although its currently not used

ecg_data_buffer = []
    
def ecsParsePacket(DataRcvPacket, num):
    if num == 0:
        return int(DataRcvPacket[num] << (num * 8))
    else:
        return ( DataRcvPacket[num] << (num * 8)) | ecsParsePacket(DataRcvPacket, num - 1) 

def process_serial( rxch ):
    global rx_state
    global pkt_pos_counter
    global pkt_len
    global pkt_pktType
    global data_counter
    global pkt_data_counter
    global pkt_ecg_bytes
    global pkt_resp_bytes

    if (rx_state == STATE_INIT):
        if (rxch == PKT_START1): 
            rx_state = STATE_SOF1_FOUND
            return

    elif rx_state == STATE_SOF1_FOUND:
        if rxch == PKT_START2:
            rx_state = STATE_SOF2_FOUND
        else:
            rx_state = STATE_INIT
        return

    elif rx_state == STATE_SOF2_FOUND:
            rx_state = STATE_PKTLEN_FOUND
            pkt_len = ord(rxch) 
            pkt_pos_counter = CMDIF_IND_LEN
            data_counter = 0
            return

    elif rx_state == STATE_PKTLEN_FOUND:
        pkt_pos_counter += 1
        if pkt_pos_counter < CMDIF_PKT_OVERHEAD:
            if pkt_pos_counter == CMDIF_IND_LEN_MSB:
                pkt_len = ord(rxch) << 8 | pkt_len
                return
            elif pkt_pos_counter == CMDIF_IND_PKTTYPE:
                pkt_pktType = ord(rxch)
                return
        elif (pkt_pos_counter >= CMDIF_PKT_OVERHEAD) and (pkt_pos_counter < CMDIF_PKT_OVERHEAD + pkt_len + 1): # Read data
            if pkt_pktType == 2:
                #np.append(pkt_data_counter, rxch) # Buffer that assigns the data separated from the packet
                pkt_data_counter += rxch
                data_counter += 1
                return
        else: 
            if rxch == PKT_STOP:
                pkt_ecg_bytes.append(pkt_data_counter[1])
                pkt_ecg_bytes.append(pkt_data_counter[0])

                pkt_resp_bytes.append(pkt_data_counter[2])
                pkt_resp_bytes.append(pkt_data_counter[3])
                pkt_resp_bytes.append(pkt_data_counter[4])
                pkt_resp_bytes.append(pkt_data_counter[5])

                data1 = pkt_ecg_bytes[0] | pkt_ecg_bytes[1] << 8
                data1 = data1 << 16
                data1 = data1 >> 16

                val = data1
                bits = 16
                # 2's complement
                if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
                    val = val - (1 << bits) 

                #if ecg > 30000:
                #    ecg = 65335 - ecg

                ecg = float(val / pow(10, 3))

                data2 = ecsParsePacket(pkt_resp_bytes, len(pkt_resp_bytes) - 1)
                resp = float( data2 ); #(Math.pow(10, 3));

                # Clear buffers
                pkt_data_counter.clear()
                pkt_ecg_bytes.clear() # Buffer to hold ECG data
                pkt_resp_bytes.clear() # Buffer to hold respiration data although its currently not used
                
                rx_state = STATE_INIT
                return ecg

def LoadECGData():
    try:
        if platform == "linux" or platform == "linux2":
            ser = serial.Serial('/dev/ttyACM0', 115200) # Serial port for the raspberry pi
        elif platform == "darwin":
            ser = serial.Serial('/dev/cu.usbmodem14401', 115200) # Serial port for windows
        else:
            ser = serial.Serial('COM3', 115200) # Serial port for windows
    except (OSError, serial.SerialException):
        print_log("ECG Not Connected")
        return None
        
    try:
        while True:
            if ser.in_waiting > 0:
                byte = ser.read()
                ecg = process_serial(byte)
                if ecg is not None:
                    yield ecg
    except:
        print_log("SERIAL DISCONNECTED")
        return None

# Create mock processing
def Mock_Process(byte1, byte2):
    ecg_sample =  bytearray()
    ecg_sample += byte2
    ecg_sample += byte1 
    data1 = ecg_sample[0] | ecg_sample[1] << 8
    data1 = data1 << 16
    data1 = data1 >> 16
    val = data1
    bits = 16
    # 2's complement
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits) 
    ecg = float(val / pow(10, 3))
    return ecg    

# Mocking out the arduino
def Mock_LoadECGData_File():
    if FILENAME is not None:
        with open(FILENAME) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for data in csv_reader:
                yield float(data[0])
    return 0


# Mocking out the arduino
def Mock_LoadECGData():
    BYTE1 = b'\x0A'
    BYTE2 = b'\xFF'
    BYTE3 = b'\x00'
    BYTE4 = b'\x11'
    while True:     
        num = random.uniform(0,1)
        if num < 0.25:
            ecg = Mock_Process(BYTE1, BYTE2)
        elif 0.25 < num < 0.5:
            ecg = Mock_Process(BYTE2, BYTE1)
        elif 0.5 < num < 0.75:
            ecg = Mock_Process(BYTE3, BYTE4)
        else:
            ecg = Mock_Process(BYTE4, BYTE3)
        yield abs(ecg)