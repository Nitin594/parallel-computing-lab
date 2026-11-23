# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def get_column(args):
    matrix, j = args
    return [row[j] for row in matrix]

def sequential(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def process_column(A, j, q):
    q.put((j, get_column((A, j))))

def threaded_column(A, j, result):
    result[j] = get_column((A, j))

if __name__ == "__main__":
    rows = int(input("Enter rows: "))
    cols = int(input("Enter columns: "))
    if rows <= 0 or cols <= 0:
        print("Dimensions must be positive.")
        raise SystemExit
    print("Enter matrix elements:")
    A = [[int(input()) for _ in range(cols)] for _ in range(rows)]

    start = time.perf_counter()
    s = sequential(A)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        columns = pool.map(get_column, [(A, j) for j in range(cols)])
    p_result = columns
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for j in range(cols):
        p = Process(target=process_column, args=(A, j, q))
        processes.append(p)
        p.start()
    proc_result = [None] * cols
    for _ in range(cols):
        j, column = q.get()
        proc_result[j] = column
    for p in processes:
        p.join()
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * cols, []
    for j in range(cols):
        t = threading.Thread(target=threaded_column, args=(A, j, thread_result))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Multithreading:", thread_result, "Time:", time.perf_counter() - start)
