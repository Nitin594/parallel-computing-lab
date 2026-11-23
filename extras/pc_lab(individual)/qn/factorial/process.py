import time
from multiprocessing import Process, Queue
from math import prod


# Function to calculate partial product
def calculate_product(numbers, q):

    result = prod(numbers)

    q.put(result)


if __name__ == "__main__":

    # Take input
    n = int(input("Enter a number: "))

    # Start timer
    start_time = time.perf_counter()

    # Divide numbers into groups
    numbers = list(range(1, n + 1))

    workers = 3

    tasks = [
        numbers[i::workers]
        for i in range(workers)
    ]

    # Create queue
    q = Queue()

    # Store processes
    processes = []

    # Create processes
    for task in tasks:

        p = Process(
            target=calculate_product,
            args=(task, q)
        )

        processes.append(p)

        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    # Collect partial results
    fact = 1

    for i in range(workers):
        fact = fact * q.get()

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Factorial of", n, "is:", fact)

    print("Execution Time:",
          end_time - start_time, "seconds")

    q.close()