# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def multiply_row(args):
    row, B = args
    return [sum(row[k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]

def sequential(A, B):
    return [multiply_row((row, B)) for row in A]

def process_row(row, B, index, q):
    q.put((index, multiply_row((row, B))))

def threaded_row(row, B, result, index):
    result[index] = multiply_row((row, B))

if __name__ == "__main__":
    r1 = int(input("Rows in A: "))
    c1 = int(input("Columns in A / rows in B: "))
    c2 = int(input("Columns in B: "))
    if min(r1, c1, c2) <= 0:
        print("Dimensions must be positive.")
        raise SystemExit

    print("Enter Matrix A:")
    A = [[int(input()) for _ in range(c1)] for _ in range(r1)]
    print("Enter Matrix B:")
    B = [[int(input()) for _ in range(c2)] for _ in range(c1)]

    start = time.perf_counter()
    s = sequential(A, B)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        p_result = pool.map(multiply_row, [(row, B) for row in A])
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for i, row in enumerate(A):
        p = Process(target=process_row, args=(row, B, i, q))
        processes.append(p)
        p.start()
    proc_result = [None] * r1
    for _ in range(r1):
        i, row = q.get()
        proc_result[i] = row
    for p in processes:
        p.join()
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * r1, []
    for i, row in enumerate(A):
        t = threading.Thread(target=threaded_row, args=(row, B, thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Multithreading:", thread_result, "Time:", time.perf_counter() - start)
