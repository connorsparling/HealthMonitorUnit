import serial

#Packet Constants
pkt_start1 = 0x0A
pkt_start2 = 0xFA
pkt_end = 0x0B

#State Constants
rx_state = 0
state_Init = 0
state_SOF1_Found = 1
state_SOF2_Found = 2
state_PktLen_Found = 3

#CES CMD IF Packet Indicies
ind_len = 2
ind_len_msb = 3
ind_pkttype = 4
pkt_overhead = 5


ser = serial.Serial('/dev/ttyACM0', 9600)
while 1:
    if(ser.in_waiting >0):
        byte = ser.read()
        print(byte)


def pkt_init():
    if rxch == pkt_start1: 
        rx_state = state_SOF1_Found

def pkt_sof1_found():
    if rxch == pkt_start2:
        rx_state = state_SOF2_Found
    else:
        rx_state = state_Init

def pkt_sof2_found():
    rx_state = state_PktLen_Found
    pkt_len = ord(rxch)
    pkt_pos_counter = ind_len
    data_counter = 0


def pkt_len_found():
    pkt_pos_counter += 1
    if pkt_pos_counter < pkt_overhead:
        if pkt_pos_counter == ind_len_msb:
            pkt_len = ord(rxch<<8|pkt_len) 
        elif pkt_pos_counter == ind_pkttype:
            pkt_pkttype = ord(rxch)
    elif ((pkt_pos_counter >= pkt_overhead) && (pkt_pos_counter < pkt_overhead + pkt_len + 1)):
        if pkt_pkttype == 2:
            pkt_data_counter


def analysize_state(rx_state):
    switcher = {
        CESState_Init: pkt_init ,
        CESState_SOF1_Found: pkt_sof1_found ,
        CESState_SOF2_Found: pkt_sof2_found, 
        CESState_PktLen_Found: pkt_len_found 
    }
