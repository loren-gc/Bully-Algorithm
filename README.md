# Bully-Algorithm
A method for dynamically electing a coordinator or leader from a group of distributed computer processes.

---

# How to run:
 for i in {1..5}; do gnome-terminal --title="Process $i" --command="bash -c 'python3 process$i.py --id $i; exec bash'": & done
