# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import socket
import threading
import queue
import json
import time
from enum import IntEnum

############################################################### CONSTANTS ####################################################################

lock = threading.Lock() 

process_id = 0
server_port = 0

PROCESSES_AMOUNT = 5
processes_ports = []
BASE_PORT = 5050

GENERAL_ADDRESS = "127.0.0.1"
SERVER_IP = "127.0.0.1"

TIMEOUT_AMOUNT_LIMIT = 2
TIMEOUT_TIME_LIMIT = 0.4 # (in seconds)
timeouts = []

IN_ELECTION = False
alive_processes = [] # List that keeps track of the current running process on the distributed system

######################################################## CLASSSES AND DICTIONARIES ###########################################################

class Message(IntEnum):
    ELECTION = 1
    OK = 2
    COORDINATOR = 3
    HEARTBEAT = 4

def json_dumps(payload):
    json.dumps(payload).encode("utf-8")

ELECTION = {
    'type': Message.ELECTION
}
ELECTION_PAYLOAD = json_dumps(ELECTION)

OK = {
    'type': Message.OK
}
OK_PAYLOAD = json_dumps(OK)

COORDINATOR = {
    'type': Message.COORDINATOR
}
COORDINATOR_PAYLOAD = json_dumps(COORDINATOR)

HEARTBEAT = {
    'type': Message.HEARTBEAT,
    'process_id': process_id
}
HEARTBEAT_PAYLOAD = json_dumps(HEARTBEAT)

######################################################### FUNCTIONS AND PROCEDURES ##########################################################

############################ GENERAL PROCEDURES AND FUNCTIONS
def environment_start(program_process_id, program_server_port):
    process_id = program_process_id
    server_port = program_server_port
    for i in range(PROCESSES_AMOUNT):
        timeouts.append(0)
        processes_ports.append(BASE_PORT+i)
        alive_processes.append(True)
    call_election() # When starting, a process automatically calls for an election

def send_payload(payload, destiny_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((GENERAL_ADDRESS, destiny_port))
        s.sendall(payload)
    except socket.error:
        pass

#################################################### SERVER
def server():
    print("")

################################################# HEARTBEAT
def check_heartbeats():
    for i in range(PROCESSES_AMOUNT):
        if timeouts[i] > TIMEOUT_AMOUNT_LIMIT:
            print(f"Process with process_id {i} has crashed!")
            thread = threading.Thread(target=call_election, daemon=True)
            thread.start()
            return

def send_heartbeats():
    global timeouts
    payload = HEARTBEAT_PAYLOAD
    for i in range(PROCESSES_AMOUNT):
        if i != process_id:
            destiny_port =  processes_ports[i]
            send_payload(payload, destiny_port)
            with lock:
                timeouts[i] += 1

def heartbeat():
    while True:
        send_heartbeats()
        time.sleep(TIMEOUT_TIME_LIMIT)
        check_heartbeats()

############################################ CALL ELECTION
def call_election():
    print("Calling for an election!")

