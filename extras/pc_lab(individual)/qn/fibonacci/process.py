import time
from multiprocessing import Process, Queue


def fibonacci(n, q):
    if n <= 1:
        q.put((n, n))
        return

    a, b = 0, 1

    for i in range(n - 1):
        a, b = b, a + b

    q.put((n, b))


if __name__ == "__main__":
    n = int(input("Enter number of terms: "))

    if n < 0:
        print("Please enter a non-negative number.")
    else:
        start_time = time.perf_counter()

        q = Queue()
        processes = []

        for i in range(n):
            p = Process(target=fibonacci, args=(i, q))
            processes.append(p)
            p.start()

        result = [0] * n

        for i in range(n):
            index, value = q.get()
            result[index] = value

        for p in processes:
            p.join()

        end_time = time.perf_counter()

        print("Fibonacci Series:", result)
        print("Execution Time:", end_time - start_time, "seconds")