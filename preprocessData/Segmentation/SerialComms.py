import serial
from sys import platform

#Packet Constants
PKT_START1 = 0x0A
PKT_START2 = 0xFA
PKT_STOP = 0x0B

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

pkt_data_counter = [None]*1000 # Buffer to store the data from the packet
pkt_ecg_bytes = [None]*4 # Buffer to hold ECG data
pkt_resp_bytes = [None]*4 # Buffer to hold respiration data although its currently not used
'''
if platform == "linux" or platform == "linux2":
    ser = serial.Serial('/dev/ttyACM0', 115200) # Serial port for the raspberry pi
else:
    ser = serial.Serial('COM4', 115200) # Serial port for windows

while 1:
    if(ser.in_waiting > 0):
        byte = ser.read()
        print(byte)
'''
def process_serial(rxch):
    analyze_state(rxch)

def analyze_state( rxch ):
    switcher = {
        CESState_Init: init,
        CESState_SOF1_Found: pkt_sof1_found,
        CESState_SOF2_Found: pkt_sof2_found, 
        CESState_PktLen_Found: pkt_len_found, 
    }

def pkt_init():
    if rxch == pkt_start1: 
        rx_state = STATE_SOF1_FOUND

def pkt_sof1_found():
    if rxch == pkt_start2:
        rx_state = STATE_SOF2_FOUND
    else:
        rx_state = STATE_INIT

def pkt_sof2_found():
    rx_state = STATE_PKTLEN_FOUND
    pkt_len = int(rxch) # might be wrong
    pkt_pos_counter = CMDIF_IND_LEN
    data_counter = 0

def pkt_len_found():
    pkt_pos_counter += 1
    if pkt_pos_counter < CMDIF_PKT_OVERHEAD:
        if pkt_pos_counter == ind_len_msb:
            pkt_len = int( rxch << 8 | pkt_len ) 
        elif pkt_pos_counter == ind_pktType:
            pkt_pktType = int(rxch)
    elif (pkt_pos_counter >= CMDIF_PKT_OVERHEAD) and (pkt_pos_counter < CMDIF_PKT_OVERHEAD + pkt_len + 1): # Read data
        if pkt_pktType == 2:
            pkt_data_counter[data_counter] = chr(rxch) # Buffer that assigns the data separated from the packet
            data_counter += 1
    else:
        if rxch == PKT_STOP:
            pkt_ecg_bytes[0] = pkt_data_counter[0]
            pkt_ecg_bytes[1] = pkt_data_counter[1]
            pkt_ecg_bytes[2] = pkt_data_counter[2]
            pkt_ecg_bytes[3] = pkt_data_counter[3]

            pkt_resp_bytes[0] = CES_Pkt_Data_Counter[4]
            pkt_resp_bytes[1] = CES_Pkt_Data_Counter[5]
            pkt_resp_bytes[2] = CES_Pkt_Data_Counter[6]
            pkt_resp_bytes[3] = CES_Pkt_Data_Counter[7]

            data1 = ecsParsePacket(pkt_ecg_bytes, len(pkt_ecg_bytes) - 1)
            ecg = float( data1 / pow(10, 3) ) # originally was a double
        
            data2 = ecsParsePacket(pkt_resp_bytes, len(pkt_resp_bytes) - 1)
            resp = float( data2 ); #(Math.pow(10, 3));


def ecsParsePacket(DataRcvPacket, num):
    if num == 0:
        return int(DataRcvPacket[num] << (num * 8))
    else:
        return ( DataRcvPacket[num] << (num * 8)) | ecsParsePacket(DataRcvPacket, num - 1) 

                
