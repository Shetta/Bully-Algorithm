from BullyAlgorithm import Bully
from BullyLogging import BullyLogging

def main():
    """
    initializes the program by taking an input from the user for the number of processes to be created.
    It validates the user's input and creates a Bully object with the given number of processes.
    The Bully Algorithm is started and the task is distributed among the processes.
    The minimum value from each process is collected and printed out.
    :return: Logging of the BullyAlgorithm and NodeWrapper Classes

    ::Process ->
        1. Instantiate a new Bully object with the given number of processes by the user and validate the input.
        2. Start the Bully Algorithm and distribute the task.
        3. Collect the min value from each process and print it out and validate the algorithm.
    """
    num_processes = None
    while num_processes is None:
        try:
            num_processes = int(input("Enter the number of processes: "))
            if num_processes <= 0:
                raise ValueError("Number of processes must be a positive integer")
        except ValueError as e:
            print(f"Error: {e}")
            print("Please enter a positive integer for the number of processes.")

    try:
        bully = Bully(num_processes)

        bully.start()

        minimum = bully.collect_results()
        print(f"The minimum value in the array is {minimum}")

    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred while running the Bully Algorithm. Please try again.")

if __name__ == '__main__':
    main()
