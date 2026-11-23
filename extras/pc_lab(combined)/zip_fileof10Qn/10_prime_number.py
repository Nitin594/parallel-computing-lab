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

def is_divisor(args):
    number, divisor = args
    return number % divisor == 0

def sequential(n):
    if n <= 1:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True

def process_check(n, divisor, q):
    q.put(n % divisor == 0)

def thread_check(n, divisor, result, index):
    result[index] = (n % divisor == 0)

if __name__ == "__main__":
    n = int(input("Enter a number: "))
    divisors = list(range(2, math.isqrt(n) + 1)) if n > 1 else []

    start = time.perf_counter()
    s = sequential(n)
    print("\nSequential:", "Prime" if s else "Not Prime", "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    if n <= 1:
        p_result = False
    elif not divisors:
        p_result = True
    else:
        with Pool() as pool:
            checks = pool.map(is_divisor, [(n, d) for d in divisors])
        p_result = not any(checks)
    print("Multiprocessing Pool:", "Prime" if p_result else "Not Prime", "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    if n <= 1:
        proc_result = False
    elif not divisors:
        proc_result = True
    else:
        q, processes = Queue(), []
        for d in divisors:
            p = Process(target=process_check, args=(n, d, q))
            processes.append(p)
            p.start()
        checks = [q.get() for _ in divisors]
        for p in processes:
            p.join()
        proc_result = not any(checks)
    print("Multiprocessing Process:", "Prime" if proc_result else "Not Prime", "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    if n <= 1:
        th_result = False
    elif not divisors:
        th_result = True
    else:
        checks, threads = [False] * len(divisors), []
        for i, d in enumerate(divisors):
            t = threading.Thread(target=thread_check, args=(n, d, checks, i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        th_result = not any(checks)
    print("Multithreading:", "Prime" if th_result else "Not Prime", "Time:", time.perf_counter() - start)
