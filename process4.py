# Lorenzo Grippo Chiachio - 823917
# João Vitor Seiji - 822767

import threading
from utils import environment_start, heartbeat, server

############################################################### CONSTANTS ##############################################################

# process variables
PROCESS_ID = 3
SERVER_PORT = 5050+PROCESS_ID

################################################################# MAIN #################################################################

if __name__ == "__main__":
    # Starting the queues for the communication between threads and calling for an openning election:
    environment_start(PROCESS_ID, SERVER_PORT)
    # Starting threads:
    thread1 = threading.Thread(target=heartbeat)
    thread2 = threading.Thread(target=server)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
