# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def fib(index):
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a

def sequential(n):
    result, a, b = [], 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

def process_fib(index, q):
    q.put((index, fib(index)))

def threaded_fib(index, result):
    result[index] = fib(index)

if __name__ == "__main__":
    n = int(input("Enter number of terms: "))
    if n < 0:
        print("Enter a non-negative number.")
        raise SystemExit

    start = time.perf_counter()
    s = sequential(n)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        p_result = pool.map(fib, range(n))
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for i in range(n):
        p = Process(target=process_fib, args=(i, q))
        processes.append(p)
        p.start()
    proc_result = [None] * n
    for _ in range(n):
        i, value = q.get()
        proc_result[i] = value
    for p in processes:
        p.join()
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * n, []
    for i in range(n):
        t = threading.Thread(target=threaded_fib, args=(i, thread_result))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Multithreading:", thread_result, "Time:", time.perf_counter() - start)
