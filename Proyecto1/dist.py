import time

class Node:
     def __init__(self, name):
         self.name = name
         self.processes = []
    
     def add_process(self, process):
         self.processes.append(process)
    
     def get_load(self):
         return sum(process.time for process in self.processes)
    
     def execute_processes(self):
         while self.processes:
             process = self.processes.pop(0)
             print(f"Running process {process.name} on node {self.name}")
             remaining_time = process.time
             while time_remaining > 0:
                 print(f"Process {process.name}: Time remaining = {time_remaining}")
                 time_remaining -= 1
                 time.sleep(1)
             print(f"Process {process.name} terminated at node {self.name}")


class Dispatcher:
     def __init__(self, nodes):
         self.nodes = nodes
    
     def dispatch_process(self, process):
         sorted_nodes = sorted(self.nodes, key=lambda node: node.get_load())
         source_node = sorted_nodes[0]
         destination_node = sorted_nodes[1] if len(sorted_nodes) > 1 else None
        
         if destination_node is None or source_node.get_load() < destination_node.get_load():
             source_node.add_process(process)
             print(f"Process {process.name} will stay in source node {source_node.name}")
         else:
             destination_node.add_process(process)
             print(f"Process {process.name} sent to destination node {destination_node.name}")

     def run_dispatcher(self):
         while True:
             process = Process() # Simulation of a new process
             self.dispatch_process(process)
             time.sleep(1)


class Process:
     counter = 0
    
     def __init__(self):
         Process.counter += 1
         self.name = f"Process{Process.counter}"
         self.time = 5 # Execution time in seconds


# create nodes
node1 = Node("Node1")
node2 = Node("Node2")
node3 = Node("Node3")

# Add nodes to the dispatcher node list
dispatcher = Dispatcher([node1, node2, node3])

# Run the dispatcher in a separate thread
import threading
thread = threading.Thread(target=dispatcher.run_dispatcher)
thread.start()

# Run the nodes
node1.run_processes()
node2.run_processes()
node3.run_processes()
