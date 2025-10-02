# Bully-Algorithm

---

## 📋 Description

A method for dynamically electing a coordinator or leader from a group of distributed computer processes.
This project implements the Bully Algorithm, a classical distributed systems algorithm used for leader election in a network of processes. The algorithm ensures that when a coordinator (leader) fails, the remaining processes can elect a new coordinator in a deterministic manner. To elect the new leader, the lowest process_id among the current running/alive processes in the system is used as criteria.

## 🏗️ Architecture

5 independent processes (process1.py to process5.py)
Each process runs 3 concurrent threads:

- **Server Thread**: Listens for incoming messages
- **Heartbeat Thread**: Monitors other processes' availability
- **Election Thread**: Handles leader election process

## 📐 Estrutura do Projeto

    bully-algorithm/
    ├── process1.py          # Process with ID 0 (port 5050)
    ├── process2.py          # Process with ID 1 (port 5051)
    ├── process3.py          # Process with ID 2 (port 5052)
    ├── process4.py          # Process with ID 3 (port 5053)
    ├── process5.py          # Process with ID 4 (port 5054)
    ├── utils.py             # Core algorithm implementation
    └── README.md

## 🚀 How to run

Use the command to simultaneously run the 5 processes:
```bash
for i in {1..5}; do
    gnome-terminal --title="Process $i" --command="bash -c 'python3 process$i.py --id $i; exec bash'" &
    sleep 0.2
done
```

<p align="center">**You might need to ajust the time between the executions depending on your machine !!!**</p>

---

The program will run normally until one or more of the processes dies/fails. If that process was the COORDINATOR, the algorithm will elect a new leader.
<p align="center">You can kill a process with Ctrl+C, or through terminal, to test the algorithm! ;)</p>
 
