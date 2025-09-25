# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import socket
import threading
import queue
import json
import time
from enum import IntEnum

################################################################# CONSTANTS ################################################################

lock = threading.Lock() 

process_id = 0
server_port = 0

PROCESSES_AMOUNT = 5
processes_ports = []
BASE_PORT = 5050

GENERAL_ADDRESS = "127.0.0.1"
SERVER_IP = "127.0.0.1"

TIMEOUT_LIMIT = 2
timeouts = []

################################################################# CLASSSES #################################################################

class Message(IntEnum):
    ELECTION = 1
    OK = 2
    COORDINATOR = 3
    HEARTBEAT = 4

######################################################### FUNCTIONS AND PROCEDURES ##########################################################
###################################### GENERAL PROCEDURES AND FUNCTIONS
def environment_start(program_process_id, program_server_port):
    process_id = program_process_id
    server_port = program_server_port
    for i in range(PROCESSES_AMOUNT):
        timeouts.append(0)
        processes_ports.append(BASE_PORT+i)
    call_election() # When starting, a process automatically calls for an election

def send_payload(payload, destiny_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((GENERAL_ADDRESS, destiny_port))
    s.sendall(payload)

###################################### SERVER
def server():
    print("")

###################################### HEARTBEAT
def check_heartbeats():
    for i in range(PROCESSES_AMOUNT):
        if timeouts[i] > TIMEOUT_LIMIT:
            thread = threading.Thread(target=call_election, daemon=True)
            thread.start()
            return

def send_heartbeats():
    heartbeat = {
        'type': Message.HEARTBEAT,
        'process_id': process_id
    }
    payload = json.dumps(heartbeat).encode("utf-8")
    for i in range(PROCESSES_AMOUNT):
        if i != process_id:
            destiny_port =  processes_ports[i]
            send_payload(payload, destiny_port)
            timeouts[i] += 1

def heartbeat():
    while True:
        send_heartbeats()
        time.sleep(0.4)
        check_heartbeats()

###################################### CALL ELECTION
def call_election():
    print("Calling for an election!")

