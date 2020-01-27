import serial
import time
from sys import platform

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
#rx_state = 0 # To check state of the packet
pkt_pos_counter = 0 # Packet counter
pkt_len = 0 # To store the packet length 
data_counter = 0 # Data counter
pkt_pktType = 0 # Store the packet type

pkt_data_counter = [None] * 1000 # Buffer to store the data from the packet
pkt_ecg_bytes = [None] * 4 # Buffer to hold ECG data
pkt_resp_bytes = [None] * 4 # Buffer to hold respiration data although its currently not used

def process_serial( rxch, rx_state ):
    global pkt_pos_counter
    global pkt_len
    print("This is the state: ", rx_state)
    if rx_state == None: # Added for error conditions
        rx_state = STATE_INIT
        return rx_state

    if rx_state == STATE_INIT:
        if rxch == PKT_START1: 
            print("10")
            rx_state = STATE_SOF1_FOUND
            return rx_state

    elif rx_state == STATE_SOF1_FOUND:
        if rxch == PKT_START2:
            rx_state = STATE_SOF2_FOUND
            print("2")
        else:
            rx_state = STATE_INIT
        return rx_state

    elif rx_state == STATE_SOF2_FOUND:
            rx_state = STATE_PKTLEN_FOUND
            print("3")
            pkt_len = ord(rxch) # might be wrong
            pkt_pos_counter = CMDIF_IND_LEN
            data_counter = 0
            return rx_state

    elif rx_state == STATE_PKTLEN_FOUND:
        pkt_pos_counter += 1
        print("4")
        if pkt_pos_counter < CMDIF_PKT_OVERHEAD:
            if pkt_pos_counter == CMDIF_IND_LEN_MSB:
                pkt_len = ord(rxch) << 8 | pkt_len
                print(pkt_len)
            elif pkt_pos_counter == CMDIF_IND_PKTTYPE:
                print("WTF")
                pkt_pktType = int(rxch)
        elif (pkt_pos_counter >= CMDIF_PKT_OVERHEAD) and (pkt_pos_counter < CMDIF_PKT_OVERHEAD + pkt_len + 1): # Read data
            print("noooob")
            if pkt_pktType == 2:
                pkt_data_counter[data_counter] = chr(rxch) # Buffer that assigns the data separated from the packet
                data_counter += 1
        else:
            print("aaaahhhh") 
            if rxch == PKT_STOP:
                print("5")
                pkt_ecg_bytes[0] = pkt_data_counter[0]
                pkt_ecg_bytes[1] = pkt_data_counter[1]
                pkt_ecg_bytes[2] = pkt_data_counter[2]
                pkt_ecg_bytes[3] = pkt_data_counter[3]

                pkt_resp_bytes[0] = pkt_data_counter[4]
                pkt_resp_bytes[1] = pkt_data_counter[5]
                pkt_resp_bytes[2] = pkt_data_counter[6]
                pkt_resp_bytes[3] = pkt_data_counter[7]

                data1 = ecsParsePacket(pkt_ecg_bytes, len(pkt_ecg_bytes) - 1)
                ecg = float( data1 / pow(10, 3) ) # originally was a double
                print(ecg)

                data2 = ecsParsePacket(pkt_resp_bytes, len(pkt_resp_bytes) - 1)
                resp = float( data2 ); #(Math.pow(10, 3));

                print(data1)

    def ecsParsePacket(DataRcvPacket, num):
        if num == 0:
            return int(DataRcvPacket[num] << (num * 8))
        else:
            return ( DataRcvPacket[num] << (num * 8)) | ecsParsePacket(DataRcvPacket, num - 1) 
                
def main():

    if platform == "linux" or platform == "linux2":
        ser = serial.Serial('/dev/ttyACM0', 115200) # Serial port for the raspberry pi
    else:
        ser = serial.Serial('COM3', 115200) # Serial port for windows
    
    rx_state = 0
    while 1:
        if( ser.in_waiting > 0 ):
            byte = ser.read()
            print(byte)
            rx_state = process_serial( byte, rx_state )
            time.sleep(1)


if __name__ == '__main__':
    main()

        