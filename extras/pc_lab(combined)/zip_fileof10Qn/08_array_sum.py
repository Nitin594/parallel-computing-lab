# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def sum_part(part):
    return sum(part)

def chunks(values, count=4):
    return [values[i::count] for i in range(count) if values[i::count]]

def sequential(numbers):
    total = 0
    for value in numbers:
        total += value
    return total

def process_part(part, index, q):
    q.put((index, sum(part)))

def thread_part(part, result, index):
    result[index] = sum(part)

if __name__ == "__main__":
    numbers = list(map(int, input("Enter array elements separated by spaces: ").split()))

    start = time.perf_counter()
    s = sequential(numbers)
    print("\nSequential sum:", s, "Time:", time.perf_counter() - start)

    parts = chunks(numbers)
    start = time.perf_counter()
    with Pool() as pool:
        p_result = sum(pool.map(sum_part, parts))
    print("Multiprocessing Pool sum:", p_result, "Time:", time.perf_counter() - start)

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
    proc_result = sum(partial)
    print("Multiprocessing Process sum:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [0] * len(parts), []
    for i, part in enumerate(parts):
        t = threading.Thread(target=thread_part, args=(part, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    th_result = sum(thread_result)
    print("Multithreading sum:", th_result, "Time:", time.perf_counter() - start)
