from NodeWrapper import *
import time
import random


class Bully:
    def __init__(self, num_processes):
        """
        Def: Initializing a Bully Object.
        :param num_processes: Number of processes to be initialized upon the algorithm.
        """
        """
        @self.processes: A list of NodeWrapper Objects.
        @self.array: Creating an array of 1000 random int.
        @self.start_time: Time value.
        ::Loop -> Initialize each NodeWrapper object with its own process id, the list of processes,and the array to be processed.
                  Then assign the first NodeWrapper object to be the initial coordinator. 
        @self.result: A dictionary to store the results of the computation.
        @self.coordinator: Assign the coordinator as the first NodeWrapper object.
        """
        self.processes = []
        self.start_time = time.time()
        self.array = [random.randint(0, 100) for _ in range(1000)]
        for i in range(num_processes):
            process = NodeWrapper(i, self.processes, self.array)
            self.processes.append(process)
            if i == 0:
                process.coordinator = i
        self.results = {process.process_id: None for process in self.processes}
        self.coordinator = self.processes[0]

    def start(self):
        """
        Def: This module should run the process until all results are collected.
        :return: result value.
        """
        """
        ::Process ->
            1. Wait for 3 seconds before starting the election process.
            2. Start the election process for each NodeWrapper object that has no coordinator.
            3. Log the current coordinator of each NodeWrapper object.
            4. If all results have been collected, find the minimum value and print it out.
            5. Reset the results dictionary to be empty.
            6. Send a message to the coordinator to let it know that the results have been collected.
            7. Wait for 3 seconds before distributing the task again.
        """
        while True:
            time.sleep(3)
            for process in self.processes:
                if process.coordinator is None:
                    process.start_election()
                else:
                    print(
                        f"<{time.time() - self.start_time:.2f}> Process <{process.process_id}>: current coordinator is <{process.coordinator}>")
            if all(result is not None for result in self.results.values()):
                min_result = min(self.results.values())
                print(f"<{time.time() - self.start_time:.2f}> Coordinator: minimum value is {min_result}")
                self.results = {process.process_id: None for process in self.processes}
                self.coordinator.send_message("RESULT", None)
                time.sleep(3)
                self.distribute_task()

    def distribute_task(self):
        """
        Bonus Task.
        Def: This should divide a chunk of an array into several bits.
        :return: an array of int.
        """
        """
        ::Process ->
            1. Divide the array into chunks of equal size.
            2. Assign a chunk to each NodeWrapper object and record the result.
            3. Log the result for this process.
        """
        chunk_size = len(self.array) // len(self.processes)
        chunks = [self.array[i:i + chunk_size] for i in range(0, len(self.array), chunk_size)]
        for i, process in enumerate(self.processes):
            process_chunk = chunks[i]
            result = process.divide_array()
            self.results[process.process_id] = result

    def collect_results(self):
        """
        Def: This module should return a min value from each Node.
        :return: min of Int
        """
        results = [process.find_minimum() for process in self.processes]
        return min(results)
