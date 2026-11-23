import time
import threading
from math import prod


# Function to calculate partial product
def calculate_product(numbers, results, index):

    results[index] = prod(numbers)


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

    # Store results
    results = [1] * workers

    # Store threads
    threads = []

    # Create threads
    for i in range(workers):

        t = threading.Thread(
            target=calculate_product,
            args=(tasks[i], results, i)
        )

        threads.append(t)

        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Calculate final factorial
    fact = prod(results)

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Factorial of", n, "is:", fact)

    print("Execution Time:",
          end_time - start_time, "seconds")