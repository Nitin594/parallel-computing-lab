# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import heapq
import threading
from multiprocessing import Pool, Process, Queue

def bubble_sort(part):
    arr = part.copy()
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def chunks(values, count=4):
    return [values[i::count] for i in range(count) if values[i::count]]

def process_sort(part, index, q):
    q.put((index, bubble_sort(part)))

def thread_sort(part, result, index):
    result[index] = bubble_sort(part)

if __name__ == "__main__":
    numbers = list(map(int, input("Enter array elements separated by spaces: ").split()))

    start = time.perf_counter()
    s = bubble_sort(numbers)
    print("\nSequential sorted array:", s, "Time:", time.perf_counter() - start)

    parts = chunks(numbers)
    start = time.perf_counter()
    with Pool() as pool:
        sorted_parts = pool.map(bubble_sort, parts)
    p_result = list(heapq.merge(*sorted_parts))
    print("Multiprocessing Pool sorted array:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for i, part in enumerate(parts):
        p = Process(target=process_sort, args=(part, i, q))
        processes.append(p)
        p.start()
    sorted_parts = [None] * len(parts)
    for _ in parts:
        i, value = q.get()
        sorted_parts[i] = value
    for p in processes:
        p.join()
    proc_result = list(heapq.merge(*sorted_parts))
    print("Multiprocessing Process sorted array:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * len(parts), []
    for i, part in enumerate(parts):
        t = threading.Thread(target=thread_sort, args=(part, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    th_result = list(heapq.merge(*thread_result))
    print("Multithreading sorted array:", th_result, "Time:", time.perf_counter() - start)
