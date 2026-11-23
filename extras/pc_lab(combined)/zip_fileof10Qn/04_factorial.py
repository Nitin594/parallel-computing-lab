# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import math
import threading
from multiprocessing import Pool, Process, Queue

def product_part(numbers):
    return math.prod(numbers)

def sequential(n):
    return math.factorial(n)

def process_part(numbers, index, q):
    q.put((index, math.prod(numbers)))

def threaded_part(numbers, result, index):
    result[index] = math.prod(numbers)

if __name__ == "__main__":
    n = int(input("Enter a non-negative integer: "))
    if n < 0:
        print("Factorial is not defined for negative integers.")
        raise SystemExit

    # Split the factors 1..n into up to four groups.
    factors = list(range(1, n + 1))
    parts = [factors[i::4] for i in range(4)]
    parts = [part for part in parts if part]

    start = time.perf_counter()
    s = sequential(n)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        partial = pool.map(product_part, parts)
    p_result = math.prod(partial)
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    if not parts:
        proc_result = 1
    else:
        for i, part in enumerate(parts):
            p = Process(target=process_part, args=(part, i, q))
            processes.append(p)
            p.start()
        partial = [None] * len(parts)
        for _ in parts:
            i, value = q.get()
            partial[i] = value
        for p in processes:
            p.join()
        proc_result = math.prod(partial)
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result = [None] * len(parts)
    threads = []
    for i, part in enumerate(parts):
        t = threading.Thread(target=threaded_part, args=(part, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    th_result = math.prod(thread_result)
    print("Multithreading:", th_result, "Time:", time.perf_counter() - start)
