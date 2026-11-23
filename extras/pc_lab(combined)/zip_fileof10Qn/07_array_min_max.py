# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def min_max(part):
    return (min(part), max(part))

def chunks(values, count=4):
    return [values[i::count] for i in range(count) if values[i::count]]

def sequential(numbers):
    return (min(numbers), max(numbers))

def process_part(part, index, q):
    q.put((index, min_max(part)))

def thread_part(part, result, index):
    result[index] = min_max(part)

if __name__ == "__main__":
    numbers = list(map(int, input("Enter array elements separated by spaces: ").split()))
    if not numbers:
        print("Array cannot be empty.")
        raise SystemExit
    parts = chunks(numbers)

    start = time.perf_counter()
    s = sequential(numbers)
    print("\nSequential (min, max):", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        partial = pool.map(min_max, parts)
    p_result = (min(x[0] for x in partial), max(x[1] for x in partial))
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
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
    proc_result = (min(x[0] for x in partial), max(x[1] for x in partial))
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * len(parts), []
    for i, part in enumerate(parts):
        t = threading.Thread(target=thread_part, args=(part, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    th_result = (min(x[0] for x in thread_result), max(x[1] for x in thread_result))
    print("Multithreading:", th_result, "Time:", time.perf_counter() - start)
