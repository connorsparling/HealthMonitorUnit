import serial
import time
from sys import platform
import socketio
import asyncio
import time
import numpy as np
#import os
#import csv
#import sys

sio = socketio.AsyncClient()

WEBSOCKET = 'https://backend.healthmonitor.dev'

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

    #print("This is the state: ", rx_state)

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
            #print("aaaahhhh") 
            if rxch == PKT_STOP:
                #print("5")
                #print(pkt_data_counter[0])
                #print(pkt_data_counter[1])
                #print(np.int8(pkt_data_counter[0]))
                #np.append(pkt_ecg_bytes, pkt_data_counter[0])
                #np.append(pkt_ecg_bytes, pkt_data_counter[1])
                #np.append(pkt_ecg_bytes, pkt_data_counter[2])
                #np.append(pkt_ecg_bytes, pkt_data_counter[3])
                pkt_ecg_bytes.append(pkt_data_counter[0])
                pkt_ecg_bytes.append(pkt_data_counter[1])
                #pkt_ecg_bytes.append(pkt_data_counter[2])
                #pkt_ecg_bytes.append(pkt_data_counter[3])

                #np.append(pkt_resp_bytes, pkt_data_counter[4])
                #np.append(pkt_resp_bytes, pkt_data_counter[5])
                #np.append(pkt_resp_bytes, pkt_data_counter[6])
                pkt_resp_bytes.append(pkt_data_counter[2])
                pkt_resp_bytes.append(pkt_data_counter[3])
                pkt_resp_bytes.append(pkt_data_counter[4])
                pkt_resp_bytes.append(pkt_data_counter[5])

                #print(pkt_ecg_bytes.size)
                #print(pkt_resp_bytes[1])
                #print(pkt_resp_bytes[2])
                #print(pkt_data_counter[0])
                #print(pkt_data_counter[1])
                #print(pkt_data_counter[2])
                data1 = ecsParsePacket(pkt_ecg_bytes, len(pkt_ecg_bytes) - 1)
                ecg = float( data1 / pow(10, 3) ) # originally was a double
                print("ECG VALUE: ", ecg)

                data2 = ecsParsePacket(pkt_resp_bytes, len(pkt_resp_bytes) - 1)
                resp = float( data2 ); #(Math.pow(10, 3));
                print("RESPIRATION VALUE: ", resp)

                # Clear buffers
                pkt_data_counter.clear()
                pkt_ecg_bytes.clear() # Buffer to hold ECG data
                pkt_resp_bytes.clear() # Buffer to hold respiration data although its currently not used
                
                rx_state = STATE_INIT
                return ecg

def UpdateBuffer( ecg, buffer ):
    if ecg != None:
        buffer.append(ecg)

def LoadECGData( buffer, packet_size ):
    if platform == "linux" or platform == "linux2":
        ser = serial.Serial('/dev/ttyACM0', 115200) # Serial port for the raspberry pi
    else:
        ser = serial.Serial('COM3', 115200) # Serial port for windows

    while 1:
        if( ser.in_waiting > 0 ):
            byte = ser.read()
            ecg = process_serial( byte )
            UpdateBuffer(ecg, buffer)
            #time.sleep(0.1)
            if len(buffer) == packet_size:
                break
        