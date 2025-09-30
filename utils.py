# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import socket
import threading
import queue
import json
import time
from enum import IntEnum
import signal
import sys

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
ELECTION_TIMEOUT = TIMEOUT_AMOUNT_LIMIT*TIMEOUT_TIME_LIMIT
timeouts = []

coordinator_id = 0
in_election = False
alive_processes = [] # List that keeps track of the current running process on the distributed system

############################################################## MESSAGE CLASS ################################################################

class Message(IntEnum):
    ELECTION = 1
    OK = 2
    COORDINATOR = 3
    HEARTBEAT = 4

######################################################### FUNCTIONS AND PROCEDURES ##########################################################

############################ GENERAL PROCEDURES AND FUNCTIONS
def environment_setup(program_process_id, program_server_port):
    global process_id, server_port, alive_processes, timeouts
    process_id = program_process_id
    server_port = program_server_port
    for i in range(PROCESSES_AMOUNT):
        timeouts.append(0)
        processes_ports.append(BASE_PORT+i)
        alive_processes.append(True)

def send_payload(payload, destiny_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((GENERAL_ADDRESS, destiny_port))
        s.sendall(payload)
        s.close()
    except:
        pass

############################################ CALL ELECTION
def send_coordinator_messages():
    global process_id, alive_processes
    coordinator = {
        'type': Message.COORDINATOR,
        'process_id': process_id
    }
    payload = json.dumps(coordinator).encode("utf-8")
    # Informing all the other process that this process won the election:
    for i in range(PROCESSES_AMOUNT):
        if alive_processes[i] == True and i != process_id:
            destiny_port = processes_ports[i]
            send_payload(payload, destiny_port)

def send_election_messages():
    global process_id, alive_processes, processes_ports
    election = {
        'type': Message.ELECTION,
        'process_id': process_id
    }
    payload = json.dumps(election).encode("utf-8")
    # sending only to the processes with smaller process_id:
    for i in range(process_id):
        if alive_processes[i] == True:
            destiny_port = processes_ports[i]
            send_payload(payload, destiny_port)

def call_election():
    global process_id, in_election, coordinator_id
    with lock:
        in_election = True
    print("Calling for an election!")
    send_election_messages()
    time.sleep(ELECTION_TIMEOUT)
    if in_election == True: # If the in_election variable is still True, this process won the election
        print("\nThis process is the new COORDINATOR!!!")
        with lock:
            coordinator_id = process_id
            in_election = False
        send_coordinator_messages()

################################################# HEARTBEAT
def check_heartbeats():
    global timeouts, alive_processes, coordinator_id
    for i in range(PROCESSES_AMOUNT):
        if alive_processes[i] == True and timeouts[i] > TIMEOUT_AMOUNT_LIMIT:
            print(f"\nProcess with process_id = {i} has crashed!")
            with lock:
                alive_processes[i] = False
                # If the coordinator process has fallen a new election must be called:
                if i == coordinator_id:
                    print("This process was the COORDINATOR")
                    thread = threading.Thread(target=call_election, daemon=True)
                    thread.start()
            return

def send_heartbeats():
    global process_id, timeouts, processes_ports
    heartbeat = {
        'type': Message.HEARTBEAT,
        'process_id': process_id
    }
    payload = json.dumps(heartbeat).encode("utf-8")
    for i in range(PROCESSES_AMOUNT):
        if i != process_id:
            destiny_port = processes_ports[i]
            send_payload(payload, destiny_port)
            with lock:
                timeouts[i] += 1

def heartbeat():
    while True:
        send_heartbeats()
        time.sleep(TIMEOUT_TIME_LIMIT)
        check_heartbeats()

#################################################### SERVER
def send_ok_message(destiny_process):
    global process_id, processes_ports
    ok = {
        'type': Message.OK,
        'process_id': process_id
    }
    payload = json.dumps(ok).encode("utf-8")
    destiny_port = processes_ports[destiny_process]
    send_payload(payload, destiny_port)

def handle_election(election):
    election_id = election["process_id"]
    send_ok_message(election_id)

def handle_ok():
    global in_election
    with lock:
        if in_election == True:
            in_election = False

def handle_coordinator(coordinator):
    global coordinator_id
    with lock:
        coordinator_id = coordinator["process_id"]
    print(f"\nThe process with the id {coordinator_id} is the new COORDINATOR!!!")
    
def handle_heartbeat(heartbeat):
    global timeouts, alive_processes
    heartbeat_id = heartbeat["process_id"] 
    with lock:
        timeouts[heartbeat_id] = 0
        if alive_processes[heartbeat_id] == False:
            print(f"\nProcess with id {heartbeat_id} has returned!")
            alive_processes[heartbeat_id] = True
            thread = threading.Thread(target=call_election, daemon=True)
            thread.start()

def handle_message(message):
    if message["type"] == Message.ELECTION:
        handle_election(message)
    elif message["type"] == Message.OK:
        handle_ok()
    elif message["type"] == Message.COORDINATOR:
        handle_coordinator(message)
    else: # The message is a heartbeat
        handle_heartbeat(message)

def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        message = json.loads(data.decode("utf-8"))
        handle_message(message)
    except json.JSONDecodeError:
        print(f"[{addr}] Error: Invalid JSON!")
    finally:
        conn.close()

def server():
    global server_port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, server_port))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread to handle the client:
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

