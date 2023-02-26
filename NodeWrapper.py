import time
import multiprocessing as mp


class NodeWrapper:
    def __init__(self, process_id, processes, array):
        """
        :param process_id: Current Process ID
        :param processes: A list of all NodeWrapper instances in the system.
        :param array: An array of values to be divided among the processes.
        """
        """"
        @__init__: Initializes a NodeWrapper instance with the process ID, list of all processes, and array to be divided.
        @self.process_id: Current Process ID.
        @self.coordinator: Stores the ID of the process elected as the coordinator.
        @self.processes: Stores a list of all NodeWrapper instances in the system.
        @self.start_time: Stores the start time of the program.
        @self.election_lock: A lock to protect the start_election() method from race conditions.
        @self.array: Stores the array to be divided among the processes.
        @self.chunk: Stores the chunk of the array assigned to this process.
        @self.message_handler: registers the message handler.  
        """
        self.process_id = process_id
        self.coordinator = None
        self.processes = processes
        self.start_time = time.time()
        self.election_lock = mp.Lock()
        self.array = array
        self.chunk = None
        self.message_handler = None

    def set_message_handler(self, handler):
        """
        Def: This module is to allow an external object to register a message handler callback function to handle incoming messages.
        :param handler: sets the current handler
        :return: Setter.
        """
        self.message_handler = handler

    def send_message(self, message, receiver_id):
        """
        Def: This module sends a message to a specified process.
        :param message: Election message to be passed.
        :param receiver_id: The Process self ID.
        :return: Message (String) Return type.
        """
        receiver = next((p for p in self.processes if p.process_id == receiver_id), None)
        if receiver:
            receiver.receive_message(message, self.process_id)

    def start_election(self):
        """
        Def: This module should initiate the election process.
        :return: Returns an election object if we have found the process.
        """
        print(f"<{time.time() - self.start_time:.2f}> Process <{self.process_id}>: starting election")
        self.coordinator = None

        for process in self.processes:
            if process.process_id > self.process_id:
                try:
                    print(
                        f"<{time.time() - self.start_time:.2f}> Process <{self.process_id}>: sending ELECTION to process <{process.process_id}>")
                    process.receive_message("ELECTION", self.process_id)
                except:
                    pass
        self.wait_for_coordinator()

    def wait_for_coordinator(self):
        """
        Def: This module should wait for a coordinator to be elected as the winner.
        :return: Declare the victory for a process.
        """
        if not self.coordinator:
            self.declare_victory()
        while self.coordinator is None:
            time.sleep(1)

    def declare_victory(self):
        """
        Def: This module declares the current process the coordinator.
        :return: Sets the coordinator to be the current process.
        """
        print(f"<{time.time() - self.start_time:.2f}> Process <{self.process_id}>: declaring victory")
        self.coordinator = self.process_id
        for process in self.processes:
            if process.process_id > self.process_id:
                try:
                    process.receive_message("COORDINATOR", self.process_id)
                except:
                    pass

    def receive_message(self, message, sender_id):
        """
        Def: This module should be used to pass messages between processes.
        :param message: Message to be passed.
        :param sender_id: Sender ID of the process.
        :return: Receive a String Message.
        """
        print(
            f"<{time.time() - self.start_time:.2f}> Process <{self.process_id}>: received <{message}> from process <{sender_id}>")
        if self.message_handler is not None:
            self.message_handler(self, message, sender_id)
        elif message == "ELECTION":
            self.start_election()
        elif message == "COORDINATOR":
            self.coordinator = sender_id
            self.divide_array()

    def divide_array(self):
        """
        Def: This module should divide an array into chunks and assigns a smaller chunk to each process.
        :return: return a min amount of number.
        """
        num_processes = len(self.processes)
        chunk_size = len(self.array) // num_processes
        start = self.process_id * chunk_size
        end = start + chunk_size
        if self.process_id == num_processes - 1:
            end = len(self.array)
        self.chunk = self.array[start:end]
        self.find_minimum()

    def find_minimum(self):
        """
        Def: This module should find the min value in the assigned chunk and sends it to the coordinator.
        :return: min value of int.
        """
        min_value = min(self.chunk)
        print(f"<{time.time() - self.start_time:.2f}> Process <{self.process_id}>: min chunk is {min_value}")
        self.send_message(min_value, self.coordinator)
