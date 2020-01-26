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

ser = serial.Serial('/dev/ttyACM0', 9600)
while 1:
    if(ser.in_waiting >0):
        byte = ser.read()
        print(byte)

def processing_packet (rxch):
    switcher = {
        1: ""
    }


def pkt_init()

def pkt_sof1_found():

def pkt_sof2_found():

def pkt_len_found():

def analysize_state( rx_state ):
    switcher = {
        CESState_Init: init
            if (rxch == pkt_start1):
                                 ,
        CESState_SOF1_Found: ,
        CESState_SOF2_Found: , 
        CESState_PktLen_Found: , 

    }

  switch(ecs_rx_state)
  {
  case CESState_Init:
    if (rxch==CES_CMDIF_PKT_START_1)
      ecs_rx_state=CESState_SOF1_Found;
    break;

  case CESState_SOF1_Found:
    if (rxch==CES_CMDIF_PKT_START_2)
      ecs_rx_state=CESState_SOF2_Found;
    else
      ecs_rx_state=CESState_Init;                    //Invalid Packet, reset state to init
    break;

  case CESState_SOF2_Found:
    ecs_rx_state = CESState_PktLen_Found;
    CES_Pkt_Len = (int) rxch;
    CES_Pkt_Pos_Counter = CES_CMDIF_IND_LEN;
    CES_Data_Counter = 0;
    break;

  case CESState_PktLen_Found:
    CES_Pkt_Pos_Counter++;
    if (CES_Pkt_Pos_Counter < CES_CMDIF_PKT_OVERHEAD)  //Read Header
    {
      if (CES_Pkt_Pos_Counter==CES_CMDIF_IND_LEN_MSB)
        CES_Pkt_Len = (int) ((rxch<<8)|CES_Pkt_Len);
      else if (CES_Pkt_Pos_Counter==CES_CMDIF_IND_PKTTYPE)
        CES_Pkt_PktType = (int) rxch;
    } else if ( (CES_Pkt_Pos_Counter >= CES_CMDIF_PKT_OVERHEAD) && (CES_Pkt_Pos_Counter < CES_CMDIF_PKT_OVERHEAD+CES_Pkt_Len+1) )  //Read Data
    {
      if (CES_Pkt_PktType == 2)
      {
        CES_Pkt_Data_Counter[CES_Data_Counter++] = (char) (rxch);          // Buffer that assigns the data separated from the packet
      }
    } else  //All  and data received
    {
      if (rxch==CES_CMDIF_PKT_STOP)
      { 
        ces_pkt_ecg_bytes[0] = CES_Pkt_Data_Counter[0];
        ces_pkt_ecg_bytes[1] = CES_Pkt_Data_Counter[1];


    
        ces_pkt_resp_bytes[0] = CES_Pkt_Data_Counter[2];
        ces_pkt_resp_bytes[1] = CES_Pkt_Data_Counter[3];
        ces_pkt_resp_bytes[2] = CES_Pkt_Data_Counter[4];
        ces_pkt_resp_bytes[3] = CES_Pkt_Data_Counter[5];  
        
        hr = (int)CES_Pkt_Data_Counter[6];

        int data1 = ces_pkt_ecg_bytes[0] | ces_pkt_ecg_bytes[1] <<8 ; //ecsParsePacket(ces_pkt_ecg_bytes, ces_pkt_ecg_bytes.length-1);
        data1 = data1<<16;
        data1 = data1>>16;
        /*int data1  = ecsParsePacket(ces_pkt_ecg_bytes, ces_pkt_ecg_tes.length-1);*/
        ecg = (double) data1/(Math.pow(10, 3));

               
                
        int data2 = ecsParsePacket(ces_pkt_resp_bytes, ces_pkt_resp_bytes.length-1);
       /* int data2 = ces_pkt_resp_bytes[2] | ces_pkt_resp_bytes[3] <<8 ; 
        data2 = data2<<16;
        data2 = data2>>16 ;*/
        resp = (double) data2;       // hr = (int) ces_pkt_resp_bytes[0];, 3));
        


        // Assigning the values for the graph buffers

        time = time+1;
        xdata[arrayIndex] = time;

        ecgdata[arrayIndex] = (float)ecg;
        respdata[arrayIndex] = (float) resp;
        bpmArray[arrayIndex] = (float)ecg;
        
        arrayIndex++;
        
        if(hr != 0)
        {
                    lbl_hr.setText(""+ hr);
          if(leaderror_detected == true)
          {
             leaderror_detected =  false;
             lbl_hr.setTextBold();
             lbl_hr.setFont(new Font("Monospaced", Font.PLAIN, 40));
             lbl_hr.setLocalColorScheme(GCScheme.GREEN_SCHEME);
          }
         }
        else if(hr == 0 && leaderror_detected== false)
        {
          
          lbl_hr.setTextBold();
          lbl_hr.setFont(new Font("Monospaced", Font.PLAIN,25));
          lbl_hr.setLocalColorScheme(GCScheme.RED_SCHEME);
          lbl_hr.setText("ECG lead error!!");
          leaderror_detected =  true;
        }
        
        if (arrayIndex == pSize)
        {  
          arrayIndex = 0;
          time = 0; 

        }       

        // If record button is clicked, then logging is done

        if (logging == true)
        {
          try {
            date = new Date();
            dateFormat = new SimpleDateFormat("HH:mm:ss");
            bufferedWriter.write(dateFormat.format(date)+","+ecg+","+rtor_value+","+hr);
            bufferedWriter.newLine();
          }
          catch(IOException e) {
            println("It broke!!!");
            e.printStackTrace();
          }
        }
        ecs_rx_state=CESState_Init;
      } else
      {
        ecs_rx_state=CESState_Init;
      }
    }
    break;

  default:
    break;
  }
}