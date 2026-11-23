import time
import threading


def fibonacci(n, result):
    if n <= 1:
        result[n] = n
        return

    a, b = 0, 1

    for i in range(n - 1):
        a, b = b, a + b

    result[n] = b


if __name__ == "__main__":
    n = int(input("Enter number of terms: "))

    if n < 0:
        print("Please enter a non-negative number.")
    else:
        start_time = time.perf_counter()

        result = [0] * n
        threads = []

        for i in range(n):
            t = threading.Thread(
                target=fibonacci,
                args=(i, result)
            )

            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end_time = time.perf_counter()

        print("Fibonacci Series:", result)
        print("Execution Time:", end_time - start_time, "seconds")