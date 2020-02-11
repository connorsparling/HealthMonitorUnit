#== GLOBAL ==========================================================================================================================
import threading
import time
import queue
from log import print_log
import serialRecieve
import serialSegmentation
import socketio
import torch
import torch.nn as nn
import numpy as np
import os
import sys, getopt
import csv

LOCAL = 'http://localhost:8080'
CLOUD = 'https://backend.healthmonitor.dev'

def add_to_emit_queue(queue, function, data=None):
    return add_to_queue(queue, {'function': function, 'data': data})

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
def serial(threadname, emit_queue, segment_queue, emit_buf_size=100, segment_buf_size=200):
    print_log("SERIAL THREAD WORKING")
    emit_buffer = []
    segment_buffer = []
    index = 0
    if serialRecieve.LoadECGData() == 0:
        print_log("Something went wrong with the serial connection")

    for value in serialRecieve.LoadECGData():
        # add to emit buffer
        emit_buffer.append({'sampleNum': index, 'value': value})
        # if emit buffer is 100 then add to emit queue and clear
        if len(emit_buffer) >= emit_buf_size: # 100:
            while True:
                result = add_to_emit_queue(emit_queue, 'new-ecg-point', {'data': emit_buffer})
                if result:
                    break
                print_log("EMIT QUEUE ADD = FALSE")
            emit_buffer = []

        # add to segment buffer
        segment_buffer.append(value)
        # if segment buffer is 1000 then add to segment queue and clear
        if len(segment_buffer) >= segment_buf_size: # 1000:
            while True:
                result = add_to_queue(segment_queue, segment_buffer)
                if result:
                    break
                print_log("SEGMENT QUEUE ADD = FALSE")
            segment_buffer = []
        # break if closing
        if not runThreads:
            break

#== MOCK SERIAL ==========================================================================================================================
# used to test without the arduino
def mock_serial(threadname, emit_queue, segment_queue):
    print_log("MOCK SERIAL THREAD WORKING")
    emit_buffer = []
    segment_buffer = []
    index = 0
    for value in serialRecieve.Mock_LoadECGData_File():
        time.sleep(0.008)
        # add to emit buffer
        emit_buffer.append({'sampleNum': index, 'value': value})
        # if emit buffer is 100 then add to emit queue and clear
        # currently dont send data to web app for mock out
        if len(emit_buffer) >= 100:
            while True:
                result = add_to_emit_queue(emit_queue, 'new-ecg-point', {'data': emit_buffer})
                if result:
                    break
                print_log("EMIT QUEUE ADD = FALSE")
            emit_buffer = []

        # add to segment buffer
        segment_buffer.append(value)
        # if segment buffer is 1000 then add to segment queue and clear
        if len(segment_buffer) >= 1000:
            while True:
                result = add_to_queue(segment_queue, segment_buffer)
                if result:
                    break
                print_log("SEGMENT QUEUE ADD = FALSE")
            segment_buffer = []
        # break if closing
        if not runThreads:
            break

#== SOCKET IO CLIENT ================================================================================================================
global sio
sio = socketio.Client()

# CREATE EVENT HANDLERS
@sio.on('test-ecg')
def test_ecg(data):
    print_log("test-ecg")
    print_log(data)

@sio.on('pingmebaby')
def ping_me_baby():
    print_log("ping!")

# DEFAULT EVENTS AND SETUP
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

def connect_to_server(server):
    sio.connect(server)
    sio.wait()

def socketIOClient(threadname, local):
    print_log("SOCKETIO THREAD WORKING")
    if local:
        print_log("CONNECTING TO LOCAL SERVER")
        connect_to_server(LOCAL)
    else:
        print_log("CONNECTING TO CLOUD SERVER")
        connect_to_server(CLOUD)

#== SOCKET IO EMIT QUEUE ============================================================================================================
def socketIOEmitQueue(threadname, emit_queue):
    print_log("SOCKETIO SENDING THREAD WORKING")
    while not sio.sid:
        # Wait to connect before continuing
        pass
    while runThreads:
        try:
            item = emit_queue.get()
            if item is not None:
                if item['function'] is not None:
                    if item['data'] is not None:
                        sio.emit(item['function'], item['data'])
                    else:
                        sio.emit(item['function'])
                else:
                    print_log("EMIT ITEM FUNCTION IS NONE")
                emit_queue.task_done()
            else:
                print_log("EMIT QUEUE ITEM IS NONE")
        except:
            pass

#== NEURAL NET ======================================================================================================================
TEST_NET_N = [-0.016383942295442013,-0.01687776263644462,-0.015412401210439262,-0.01247257674385413,-0.013097879462362207,-0.014480624312233159,-0.01156092127014047,-0.01706964319530293,-0.017506945437496143,-0.019497787765882353,-0.01959466999275929,-0.015942493807869683,-0.01370656776184439,-0.014781420033246222,-0.015921598857438875,-0.016799975754168583,-0.020157028436821652,-0.02278421371011281,-0.024494573376816074,-0.02327685303906001,-0.02133621179728132,-0.020348127636290684,-0.0166634646829319,-0.017612016250831822,-0.018509762860342657,-0.020700247128560532,-0.025486039794150008,-0.024662818288634716,-0.017602128834857383,-0.018680695402812544,-0.015121876887143278,-0.012188580736589134,-0.017326549126337285,-0.015409446495301847,-0.012426835440409945,-0.014722066999129386,-0.013777337459434994,-0.00864270479529799,-0.003999069619249176,-0.0028655782335729385,0.006116462393160105,0.004730479440538616,0.0075423095307507355,0.005681855650154366,0.005575295488951732,0.0063554599782269065,0.011695749297069237,0.01482568931122418,0.019525204874882345,0.020586426520206726,0.025565975721402637,0.03047089491252023,0.02774798347681111,0.03285260069424937,0.03546054114989146,0.037879832068518894,0.039770265985727075,0.044923415094578936,0.04156662216915644,0.03895760898861792,0.03834603292587075,0.03486772865141524,0.02899714219745517,0.0229971167499273,0.017738163318392675,0.013225386553348406,0.014032860824062205,0.010986481461051174,0.007338968798552067,-0.0013615593493921815,-0.008782290992913193,-0.01797942476893307,-0.018652473619248135,-0.017579324767947928,-0.012083703080120885,-0.011380105797326567,-0.0059105905503420274,-0.008984926173976322,-0.013222287483886196,-0.012578064808406583,-0.013666294687527914,-0.008001973566243456,-0.004505318629041866,-0.0017076247719550748,0.00599616961376108,0.008178521392614595,0.016320594790295396,0.02187162525721035,0.032324818087719615,0.05687132777844217,0.09099654802993075,0.13410517201104394,0.18283377799858727,0.24118800885907393,0.3085762074374782,0.3791270079018457,0.4494883393048387,0.5029009042628628,0.5410029745439383,0.5750813232472116,0.6120403223859004,0.6202055420312373,0.5712554001172183,0.44846855559876425,0.2831108733700651,0.1212327798285856,0.004429114721329768,-0.05678620562312044,-0.07272640317997567,-0.06555981954707177,-0.05722258252594388,-0.048644013503016385,-0.04316129227432186,-0.03965702849467063,-0.03835928406759137,-0.038815866923400257,-0.04278535685654058,-0.04897793080434141,-0.050432008637659,-0.04888888519983001,-0.047313520195768746,-0.044860043333483625,-0.04942871204038842,-0.0539923973902136,-0.053472981441581656,-0.055198191021230344,-0.055134145055498206,-0.05596013759146726,-0.05650070404053236,-0.055437031847026384,-0.0507261036723962,-0.058942756493278216,-0.06034177490622987,-0.061224435449436114,-0.06113832644565591,-0.06305597709792977,-0.0669761805091336,-0.0635565115353476,-0.06465751372109897,-0.06356789625915618,-0.06401257751076639,-0.06694570110585267,-0.07107294094857546,-0.07420213156361441,-0.07574341752194703,-0.07770099339582659,-0.0792561213974751,-0.07836680813353351,-0.07806218129231354,-0.07823856537599803,-0.08193681937174799,-0.08205478784377132,-0.08789893477500496,-0.09389470029708392,-0.09415640583379951,-0.09376995939963507,-0.09522668391694464,-0.09585486862855365,-0.09447527208639078,-0.09869230326668592,-0.10240360306823218,-0.10457858807781344,-0.1071855908672375,-0.1112651322082796,-0.10327208444812178,-0.10232774350151756,-0.09789952707597588,-0.10249325308121332,-0.10124779172764138,-0.10387116766019842,-0.10337985451782661,-0.10016092137900996,-0.09699066157791122,-0.09378854339858803,-0.08498307443439185,-0.07535039112686427,-0.06999741461992175,-0.061304718629205716,-0.06320468570510157,-0.06250591684799955,-0.04999192761072486,-0.041038906829509295,-0.03417414833049697,-0.02606207001504494,-0.022564439066591092,-0.018189980146107346,-0.01546386637807768,-0.019904659005406115,-0.016797180880241666,-0.01795502190986927,-0.015066388925268197,-0.009834817040541306,-0.006976136048044332,-0.006320921076503068,-0.0062947977814100985,-0.008877052934839199,-0.013285265317389099,-0.01573918903010108,-0.018405870927988722,-0.02096906214716193]
TEST_NET_BAD = [0.024263345,0.026776548,0.025201933,0.024234353,0.02714004,0.033756834,0.04508582,0.05114189,0.057001077,0.055271156,0.053238757,0.053193387,0.056980506,0.06114802,0.058115263,0.042903017,0.036293086,0.034985088,0.035428856,0.029032426,0.022787878,0.017531572,0.014043688,0.014220221,0.018191049,0.0132027855,0.0049159685,-0.0005572446,0.0060438123,0.0062233587,0.008765211,0.0034063063,0.00083209324,0.00086067576,0.005186104,0.004660823,0.0077076815,0.0064385375,0.003949239,0.00041055752,-0.00040073507,0.00023715617,0.0040487493,0.0048471154,0.008337374,0.0070848684,0.006416145,0.0024471134,0.0073726703,0.011934662,0.02020606,0.02573783,0.020377941,0.014333374,0.012571127,0.01855733,0.018624093,0.016235163,0.0097459415,0.009088432,0.033083912,0.10185889,0.18723299,0.25410175,0.27194926,0.279287,0.32457694,0.40793788,0.46318814,0.39202848,0.17574939,-0.069293275,-0.22629023,-0.2786503,-0.3017148,-0.32372868,-0.34565008,-0.35314593,-0.3430338,-0.32906562,-0.3269467,-0.32614174,-0.31433573,-0.27861017,-0.21104576,-0.12603167,-0.055573758,-0.0145381745,-0.009292502,-0.013405192,-0.011080308,0.0024615848,0.016324429,0.023283381,0.018991882,0.005180741,-0.0015506683,-0.013857022,-0.024137227,-0.031476617,-0.034751236,-0.033048954,-0.03192753,-0.040728457,-0.0511804,-0.06450106,-0.06937672,-0.07103205,-0.0738994,-0.073092036,-0.082219824,-0.092652425,-0.100616336,-0.10501871,-0.0997455,-0.10181644,-0.10042535,-0.1010729,-0.10154027,-0.10626111,-0.101060145,-0.09573499,-0.082096435,-0.07203722,-0.06144514,-0.051976338,-0.04731422,-0.03864801,-0.028042903,-0.012726852,-0.0026202034,0.003175891,0.0020656148,-0.0015883209,0.003769595,0.012342563,0.015679626,0.019080462,0.024508443,0.023466518,0.017911697,0.01927525,0.014964077,0.017088005,0.019683475,0.01871875,0.01744315,0.014863522,0.012029031,0.0084457,0.010077648,0.014523539,0.014793013,0.01734873,0.015544332,0.013673581,0.010274174,0.005341674,0.009727441,0.014639133,0.013074222,0.008799938,-0.0005025415,0.0026763577,0.0093884785,0.013703231,0.018107586,0.019639764,0.014634261,0.010361894,0.007971511,0.005597775,0.016580671,0.01921152,0.01943013,0.017074376,0.019135414,0.017625734,0.016455993,0.014969028,0.018592417,0.016640762,0.018958453,0.016705653,0.019627959,0.013501395,0.019664515,0.022363033,0.025609765,0.027611807,0.025279181,0.01506331,0.012138402,0.015695764,0.019182457,0.025731081,0.024306055,0.023128677,0.022580449,0.01755021]
BEAT_TYPES = {
    'N': 'Normal beat',
    'L': 'Left bundle branch block beat',
    'R': 'Right bundle branch block beat',
    'A': 'Atrial premature beat',
    'V': 'Premature ventricular contraction',
    'F': 'Fusion of ventricular and normal beat',
}

ARRYTHMIA_TYPES_INDEX = ['L','R','A','V','F']

class BinaryNeuralNetwork(nn.Module):
    def __init__(self):
        super(BinaryNeuralNetwork, self).__init__()
        layer_size = [200, 128, 64, 32, 16, 1]
        self.model = nn.Sequential()

        in_size = layer_size[0]
        index = 1
        for out_size in layer_size[1:]:
            self.model.add_module('fc' + str(index), nn.Linear(in_size, out_size))
            self.model.add_module('sigmoid' + str(index), nn.Sigmoid())
            in_size = out_size
            index += 1
        
    def forward(self, x):
        return self.model(x)

class ArrythmiaNeuralNetwork(nn.Module):
    def __init__(self, input_size, kernel_size, hidden_size, drop_prob):
        super(ArrythmiaNeuralNetwork, self).__init__()
        self.model = nn.Sequential()
        
        in_size = input_size
        index = 1
        for out_size in hidden_size:
            self.model.add_module('fc' + str(index), nn.Linear(in_size, out_size))
            if out_size != 5:
                self.model.add_module('sigmoid' + str(index), nn.Sigmoid())
            in_size = out_size
            index += 1
        self.model.add_module('softmax', nn.Softmax(dim=1))
        
    def forward(self, x):
        return self.model(x)

def get_output(x):
    beat_type = torch.tensor(np.array([-1]))
    out = binary_model(x)
    if out > 0.5:
        out = arrythmia_model(x)
        resValues, resIndices = torch.max(out, 1)
        beat_type = resIndices
    return beat_type

def evaluateNNData(emit_queue, binary_model, arrythmia_model, data):
    x = torch.tensor(data).type(torch.FloatTensor)
    x = x.view(1, x.size(0))

    out = binary_model(x)
    if out > 0.5:
        out = arrythmia_model(x)
        resValues, resIndices = torch.max(out, 1)
        result = resIndices[0]
        print_log("FUCK YOU'RE GONNA DIE => " + BEAT_TYPES[ARRYTHMIA_TYPES_INDEX[result]])
        #add_to_emit_queue(emit_queue, 'alert', BEAT_TYPES[ARRYTHMIA_TYPES_INDEX[result]])
    else:
        print_log("YEAH WE GOOD BABY")        

def neuralNet(threadname, neural_net_queue, emit_queue, model_path):
    time.sleep(2)
    MODEL_FOLDER = "../Models"
    binary_path = os.path.join(MODEL_FOLDER, 'BinaryNN.pt')
    arrythmia_path = os.path.join(MODEL_FOLDER, 'ArrithmiaNN.pt')

    print_log("NEURAL NET THREAD WORKING")
    if not os.path.exists(binary_path):
        print_log("BINARY MODEL DOES NOT EXIST")
        return
    if not os.path.exists(arrythmia_path):
        print_log("ARRYTHMIA MODEL DOES NOT EXIST")
        return
    print_log("LOADING BINARY MODEL FROM " + binary_path)
    binary_model = torch.load(binary_path)
    binary_model.eval()
    print_log("LOADING ARRYTHMIA MODEL FROM " + arrythmia_path)
    arrythmia_model = torch.load(arrythmia_path)
    arrythmia_model.eval()
    # REMOVE LATER ==> TEMPORARY TESTING v
    # evaluateNNData(emit_queue, binary_model, arrythmia_model, TEST_NET_N)
    # time.sleep(5)
    # evaluateNNData(emit_queue, binary_model, arrythmia_model, TEST_NET_BAD)
    # REMOVE LATER ==> TEMPORARY TESTING ^
    while runThreads:
        try:
            item = neural_net_queue.get()
            if item is not None:
                evaluateNNData(emit_queue, binary_model, arrythmia_model, item)
                neural_net_queue.task_done()
            else:
                print_log("NN QUEUE ITEM IS NONE")
        except:
            pass

#== SEGMENTATION ====================================================================================================================
def segmentation(threadname, segment_queue, neural_net_queue):
    print_log("SEGMENTATION THREAD WORKING")
    transfer_buffer = []
    #with open('../Datasets/ARD.csv', mode='w', newline='') as save_file:
        #csv_writer = csv.writer(save_file)
    while runThreads:
        try:
            item = segment_queue.get()
            if item is not None:
                # Segment piece of 1000 and spit out an array of 10 segments
                transfer_buffer, segments_buffer = serialSegmentation.format_data(transfer_buffer, item)
                # add to neural network queue
                for segment in segments_buffer:
                    # csv_writer.writerow(segment) # Write live collection data to file
                    add_to_queue(neural_net_queue, segment)
                segment_queue.task_done()
            else:
                print_log("SEGMENT QUEUE ITEM IS NONE")
        except:
            pass
    #save_file.close()

#== MAIN ============================================================================================================================
def main(argv):
    global runThreads
    runThreads = True
    local = False
    mockMode = False
    model_path = "../Models/CurrentBest.pt"
    emit_buf_size = 100
    segment_buf_size = 200
    try:
        opts, args = getopt.getopt(argv,"hlmq:",["help", "local", "model=", "mockMode"])
    except getopt.GetoptError:
        print("INCORRECT FORMAT: \"arduinoECG.py [--local | -l] [--model <PATH> | -m <PATH>] [--mockMode]\"")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("arduinoECG.py [--local | -l] [--model <PATH> | -m <PATH>] [--mockMode]")
            sys.exit()
        elif opt in ("-l", "--local"):
            local = True
            emit_buf_size = 50
        elif opt in ("-m", "--model"):
            model_path = arg
        elif opt in ("--mockMode"):
            mockMode = True

    emit_queue = queue.Queue()
    segment_queue = queue.Queue() # Pull off segment queue for processing
    neural_net_queue = queue.Queue()

    if mockMode == False:
        serial_t = threading.Thread(name="Serial", target=serial, args=("Serial", emit_queue, segment_queue, emit_buf_size, segment_buf_size))
    elif mockMode == True:
        serial_t = threading.Thread(name="MockSerial", target=mock_serial, args=("Serial", emit_queue, segment_queue))
    
    socketIOClient_t = threading.Thread(name="SocketIOClient", target=socketIOClient, args=("SocketIOClient", local))
    socketIOEmitQueue_t = threading.Thread(name="SocketIOQueue", target=socketIOEmitQueue, args=("SocketIOQueue", emit_queue))
    neuralNet_t = threading.Thread(name="NeuralNet", target=neuralNet, args=("NeuralNet", neural_net_queue, emit_queue, model_path))
    segmentation_t = threading.Thread(name="Segmentation", target=segmentation, args=("Segmentation", segment_queue, neural_net_queue))

    try:
        serial_t.start()
        socketIOClient_t.start()
        socketIOEmitQueue_t.start()
        neuralNet_t.start()
        segmentation_t.start()
    except KeyboardInterrupt:
        print_log("Keyboard Interrupt: Shutting down program...")
        sys.exit()
        runThreads = False
        sio.disconnect()
        serial_t.join()
        socketIOClient_t.join()
        socketIOEmitQueue_t.join()
        neuralNet_t.join()
        segmentation_t.join()
        print_log("Programm shutdown successfully")

if __name__ == "__main__":
    main(sys.argv[1:])