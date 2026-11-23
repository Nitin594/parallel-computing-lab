# Each program compares four approaches:
# 1. Sequential
# 2. Multiprocessing with Pool
# 3. Multiprocessing with Process + Queue
# 4. Multithreading
# Run from a .py file (especially on Windows), not from an interactive cell.

import time
import threading
from multiprocessing import Pool, Process, Queue

def sequential(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def add_row(args):
    row_a, row_b = args
    return [x + y for x, y in zip(row_a, row_b)]

def process_row(row_a, row_b, index, q):
    q.put((index, add_row((row_a, row_b))))

def threaded_row(row_a, row_b, result, index):
    result[index] = add_row((row_a, row_b))

if __name__ == "__main__":
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    if rows <= 0 or cols <= 0:
        print("Rows and columns must be positive.")
        raise SystemExit

    print("Enter elements of Matrix A:")
    A = [[int(input()) for _ in range(cols)] for _ in range(rows)]
    print("Enter elements of Matrix B:")
    B = [[int(input()) for _ in range(cols)] for _ in range(rows)]

    start = time.perf_counter()
    s = sequential(A, B)
    print("\nSequential:", s, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    with Pool() as pool:
        p_result = pool.map(add_row, list(zip(A, B)))
    print("Multiprocessing Pool:", p_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    q, processes = Queue(), []
    for i in range(rows):
        p = Process(target=process_row, args=(A[i], B[i], i, q))
        processes.append(p)
        p.start()
    proc_result = [None] * rows
    for _ in range(rows):
        i, row = q.get()
        proc_result[i] = row
    for p in processes:
        p.join()
    print("Multiprocessing Process:", proc_result, "Time:", time.perf_counter() - start)

    start = time.perf_counter()
    thread_result, threads = [None] * rows, []
    for i in range(rows):
        t = threading.Thread(target=threaded_row, args=(A[i], B[i], thread_result, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Multithreading:", thread_result, "Time:", time.perf_counter() - start)
