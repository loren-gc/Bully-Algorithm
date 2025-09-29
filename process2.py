# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import threading
from utils import environment_setup, heartbeat, server, call_election

############################################################### CONSTANTS ##############################################################

# process variables
PROCESS_ID = 1
SERVER_PORT = 5050+PROCESS_ID

################################################################# MAIN #################################################################

if __name__ == "__main__":
    # Starting the queues for the communication between threads and calling for an openning election:
    environment_setup(PROCESS_ID, SERVER_PORT)
    # Starting threads:
    thread1 = threading.Thread(target=server)
    thread2 = threading.Thread(target=heartbeat)
    thread3 = threading.Thread(target=call_election)
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

