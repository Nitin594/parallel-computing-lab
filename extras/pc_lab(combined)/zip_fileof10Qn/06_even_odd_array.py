# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def check_one(number):
    return (number, "Even" if number % 2 == 0 else "Odd")

def sequential(numbers):
    return [check_one(x) for x in numbers]

def process_one(number, index, q):
    q.put((index, check_one(number)))

def thread_one(number, result, index):
    result[index] = check_one(number)

if __name__ == "__main__":
    numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))

    start = time.perf_counter()
    s = sequential(numbers)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        p_result = pool.map(check_one, numbers)
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for i, number in enumerate(numbers):
        p = Process(target=process_one, args=(number, i, q))
        processes.append(p)
        p.start()
    proc_result = [None] * len(numbers)
    for _ in numbers:
        i, value = q.get()
        proc_result[i] = value
    for p in processes:
        p.join()
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * len(numbers), []
    for i, number in enumerate(numbers):
        t = threading.Thread(target=thread_one, args=(number, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Multithreading:", thread_result, "Time:", time.perf_counter() - start)
