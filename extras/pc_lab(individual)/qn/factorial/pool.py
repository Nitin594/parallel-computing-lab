import time
from multiprocessing import Pool
from math import prod


# Function to calculate partial product
def calculate_product(numbers):
    return prod(numbers)


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

    # Create process pool
    with Pool(processes=workers) as pool:

        # Calculate partial products
        results = pool.map(calculate_product, tasks)

    # Calculate final factorial
    fact = prod(results)

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Factorial of", n, "is:", fact)

    print("Execution Time:",
          end_time - start_time, "seconds")