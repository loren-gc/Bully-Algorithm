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
TIMEOUT_TIME_LIMIT = 0.5 # (in seconds)
timeouts = []

COORDINATOR_ID = 0
IN_ELECTION = False
alive_processes = [] # List that keeps track of the current running process on the distributed system

######################################################## CLASSSES AND DICTIONARIES ###########################################################

class Message(IntEnum):
    ELECTION = 1
    OK = 2
    COORDINATOR = 3
    HEARTBEAT = 4

def json_dumps(payload):
    return json.dumps(payload).encode("utf-8")

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

######################################################### FUNCTIONS AND PROCEDURES ##########################################################

############################ GENERAL PROCEDURES AND FUNCTIONS
def environment_start(program_process_id, program_server_port):
    global process_id, server_port
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
def handle_election(election):
    print("")

def handle_ok(ok):
    print("")

def handle_coordinator(coordinator):
    print("")
    
def handle_heartbeat(heartbeat):
    global timeouts
    print("heartbeat process id = ", heartbeat["process_id"])
    with lock:
        timeouts[heartbeat["process_id"]] = 0

def handle_message(message):
    t = message["type"]
    if t == Message.ELECTION:
        handle_election(message)
    elif t == Message.OK:
        handle_ok(message)
    elif t == Message.COORDINATOR:
        handle_coordinator(message)
    elif t == Message.HEARTBEAT:
        handle_heartbeat(message)

def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        message = json.loads(data.decode("utf-8"))
        handle_message(message)
    except json.JSONDecodeError:
        print(f"[{addr}] Error: Invalid JSON!")

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, server_port))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread to handle the client:
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

################################################# HEARTBEAT
def check_heartbeats():
    for i in range(PROCESSES_AMOUNT):
        if timeouts[i] > TIMEOUT_AMOUNT_LIMIT:
            print(f"Process with process_id {i} has crashed!")
            print(timeouts)
            thread = threading.Thread(target=call_election, daemon=True)
            thread.start()
            return

def send_heartbeats():
    global timeouts
    heartbeat = {
        'type': Message.HEARTBEAT,
        'process_id': process_id
    }
    payload = json.dumps(heartbeat).encode("utf-8")
    print(f"process id = {process_id}")
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

