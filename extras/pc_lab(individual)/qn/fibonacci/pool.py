import time
from multiprocessing import Pool


def fibonacci(n):
    if n <= 1:
        return n

    a, b = 0, 1

    for i in range(n - 1):
        a, b = b, a + b

    return b


if __name__ == "__main__":
    n = int(input("Enter number of terms: "))

    if n < 0:
        print("Please enter a non-negative number.")
    else:
        start_time = time.perf_counter()

        with Pool() as pool:
            result = pool.map(fibonacci, range(n))

        end_time = time.perf_counter()

        print("Fibonacci Series:", result)
        print("Execution Time:", end_time - start_time, "seconds")