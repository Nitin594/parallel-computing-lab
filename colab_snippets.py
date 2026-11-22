"""
colab_snippets.py
Contains complete self-contained executable code strings for each practical question (1 to 10),
tailored for Google Colab, JupyterLab, and VS Code.
Each code snippet implements all 4 execution modes (Sequential, Pool, Process, Thread),
displays verification results, prints the performance comparison table,
and renders both the Execution-Time Bar Graph and Speedup Comparison Line Graph.
"""

def get_colab_code_q1():
    return '''# Practical 1: Odd and Even Numbers Classification
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def classify_range(rng):
    start, end = rng
    arr = np.arange(start, end, dtype=np.int32)
    odd = int(np.count_nonzero(arr % 2 != 0))
    even = (end - start) - odd
    return odd, even

def proc_worker(rng, q):
    q.put(classify_range(rng))

def thread_worker(rng, results, idx):
    results[idx] = classify_range(rng)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 1: Odd and Even Numbers Classification")
    print("=" * 60)
    N = 270_000_000
    s = N // 3
    ranges = [(0, s), (s, 2 * s), (2 * s, N)]
    print(f"Total numbers to classify: {N:,} (divided into 3 ranges)")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = classify_range(ranges[0])
    r2 = classify_range(ranges[1])
    r3 = classify_range(ranges[2])
    t_seq = time.perf_counter() - t0
    odd_seq = r1[0] + r2[0] + r3[0]
    even_seq = r1[1] + r2[1] + r3[1]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(classify_range, ranges)
    t_pool = time.perf_counter() - t0
    odd_pool = sum(r[0] for r in p_res)
    even_pool = sum(r[1] for r in p_res)
    
    # 3. Multiprocessing Process (3 independent processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=proc_worker, args=(rng, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    odd_proc = sum(r[0] for r in pr_res)
    even_proc = sum(r[1] for r in pr_res)
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, rng in enumerate(ranges):
        t = threading.Thread(target=thread_worker, args=(rng, th_res, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    t_thread = time.perf_counter() - t0
    odd_thread = sum(r[0] for r in th_res)
    even_thread = sum(r[1] for r in th_res)
    
    print(f"[Sequential] Odd: {odd_seq:,} | Even: {even_seq:,} | Time: {t_seq:.4f}s")
    print(f"[Pool]       Odd: {odd_pool:,} | Even: {even_pool:,} | Time: {t_pool:.4f}s")
    print(f"[Process]    Odd: {odd_proc:,} | Even: {even_proc:,} | Time: {t_proc:.4f}s")
    print(f"[Thread]     Odd: {odd_thread:,} | Even: {even_thread:,} | Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 1: Execution Time (Odd-Even Classification)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 1: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q2():
    return '''# Practical 2: Factorial of N Numbers
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def factorial_task(n):
    # ln(n!) = sum(ln(1) + ln(2) + ... + ln(n))
    arr = np.arange(1, n + 1, dtype=np.float64)
    return float(np.sum(np.log(arr)))

def proc_worker(n, q):
    q.put(factorial_task(n))

def thread_worker(n, results, idx):
    results[idx] = factorial_task(n)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 2: Factorial of N Numbers")
    print("=" * 60)
    N = 40_000_000
    tasks = [N, N, N]
    print(f"Calculating ln({N:,}!) across 3 independent tasks.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = factorial_task(tasks[0])
    r2 = factorial_task(tasks[1])
    r3 = factorial_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(factorial_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Multiprocessing Process (3 independent processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for n in tasks:
        p = mp.Process(target=proc_worker, args=(n, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, n in enumerate(tasks):
        t = threading.Thread(target=thread_worker, args=(n, th_res, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    t_thread = time.perf_counter() - t0
    
    print(f"Sample: ln({N:,}!) = {seq_res[0]:.4e}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 2: Execution Time (Factorial ln(N!))", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 2: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q3():
    return '''# Practical 3: Maximum and Minimum in an Array
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def find_min_max_task(task):
    size, seed = task
    rng = np.random.default_rng(seed)
    arr = rng.integers(1, 1_000_000_000, size=size)
    return int(np.min(arr)), int(np.max(arr))

def proc_worker(task, q):
    q.put(find_min_max_task(task))

def thread_worker(task, results, idx):
    results[idx] = find_min_max_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 3: Maximum and Minimum in an Array")
    print("=" * 60)
    SIZE = 40_000_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    print(f"Array Size: {SIZE:,} elements per task across 3 workers.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = find_min_max_task(tasks[0])
    r2 = find_min_max_task(tasks[1])
    r3 = find_min_max_task(tasks[2])
    t_seq = time.perf_counter() - t0
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(find_min_max_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"[Sequential] Min: {r1[0]:,} | Max: {r1[1]:,} | Time: {t_seq:.4f}s")
    print(f"[Pool]       Min: {p_res[0][0]:,} | Max: {p_res[0][1]:,} | Time: {t_pool:.4f}s")
    print(f"[Process]    Min: {pr_res[0][0]:,} | Max: {pr_res[0][1]:,} | Time: {t_proc:.4f}s")
    print(f"[Thread]     Min: {th_res[0][0]:,} | Max: {th_res[0][1]:,} | Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 3: Execution Time (Min-Max Search)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 3: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q4():
    return '''# Practical 4: Matrix Addition
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def matrix_add_task(task):
    rows, cols, seed = task
    rng = np.random.default_rng(seed)
    A = rng.integers(1, 100, size=(rows, cols))
    B = rng.integers(1, 100, size=(rows, cols))
    C = A + B
    return int(C[0, 0])

def proc_worker(task, q):
    q.put(matrix_add_task(task))

def thread_worker(task, results, idx):
    results[idx] = matrix_add_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 4: Matrix Addition")
    print("=" * 60)
    ROWS, COLS = 5500, 5500
    tasks = [(ROWS, COLS, 101), (ROWS, COLS, 202), (ROWS, COLS, 303)]
    print(f"Matrix Dimension: {ROWS}x{COLS} integers per task across 3 tasks.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = matrix_add_task(tasks[0])
    r2 = matrix_add_task(tasks[1])
    r3 = matrix_add_task(tasks[2])
    t_seq = time.perf_counter() - t0
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(matrix_add_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"[Sequential] Sample: {r1} | Time: {t_seq:.4f}s")
    print(f"[Pool]       Sample: {p_res[0]} | Time: {t_pool:.4f}s")
    print(f"[Process]    Sample: {pr_res[0]} | Time: {t_proc:.4f}s")
    print(f"[Thread]     Sample: {th_res[0]} | Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 4: Execution Time (Matrix Addition)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 4: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q5():
    return '''# Practical 5: Matrix Multiplication
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def matmul_task(task):
    n, seed = task
    rng = np.random.default_rng(seed)
    A = rng.integers(1, 20, size=(n, n), dtype=np.int32)
    B = rng.integers(1, 20, size=(n, n), dtype=np.int32)
    C = np.matmul(A, B)
    return int(C[0, 0])

def proc_worker(task, q):
    q.put(matmul_task(task))

def thread_worker(task, results, idx):
    results[idx] = matmul_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 5: Matrix Multiplication")
    print("=" * 60)
    N = 720
    tasks = [(N, 101), (N, 202), (N, 303)]
    print(f"Matrix Dimension: {N}x{N} across 3 independent pairs.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = matmul_task(tasks[0])
    r2 = matmul_task(tasks[1])
    r3 = matmul_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(matmul_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"[Sequential] Sample: {seq_res[0]} | Time: {t_seq:.4f}s")
    print(f"[Pool]       Sample: {pool_res[0]} | Time: {t_pool:.4f}s")
    print(f"[Process]    Sample: {proc_res[0]} | Time: {t_proc:.4f}s")
    print(f"[Thread]     Sample: {th_res[0]} | Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 5: Execution Time (Matrix Multiplication)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 5: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q6():
    return '''# Practical 6: Fibonacci Series
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def fib_task(task):
    size, iters = task
    # Matrix Fibonacci: [[1, 1], [1, 0]]^n
    M = np.ones((size, 2, 2), dtype=np.int64)
    M[:, 1, 1] = 0
    step = np.array([[1, 1], [1, 0]], dtype=np.int64)
    for _ in range(iters):
        M = np.matmul(M, step)
    return int(M[0, 0, 0])

def proc_worker(task, q):
    q.put(fib_task(task))

def thread_worker(task, results, idx):
    results[idx] = fib_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 6: Fibonacci Series (Matrix Power)")
    print("=" * 60)
    tasks = [(60_000, 500), (60_000, 500), (60_000, 500)]
    print(f"Fibonacci matrix batch size: {tasks[0][0]:,} across {tasks[0][1]} iterations")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = fib_task(tasks[0])
    r2 = fib_task(tasks[1])
    r3 = fib_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(fib_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"Sample: F(iter): {seq_res[0]}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 6: Execution Time (Fibonacci Matrix Power)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 6: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q7():
    return '''# Practical 7: Prime Number Checking
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def count_primes_task(rng):
    start, end = rng
    nums = np.arange(start, end, dtype=np.int64)
    is_p = (nums > 1) & ((nums == 2) | (nums % 2 != 0))
    limit = int(end**0.5) + 1
    for d in range(3, limit, 2):
        is_p[(nums % d == 0) & (nums != d)] = False
    return int(np.count_nonzero(is_p))

def proc_worker(rng, q):
    q.put(count_primes_task(rng))

def thread_worker(rng, results, idx):
    results[idx] = count_primes_task(rng)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 7: Prime Number Checking")
    print("=" * 60)
    N = 750_000
    s = N // 3
    ranges = [(1, s), (s, 2 * s), (2 * s, N + 1)]
    print(f"Finding primes up to {N:,} across 3 ranges.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = count_primes_task(ranges[0])
    r2 = count_primes_task(ranges[1])
    r3 = count_primes_task(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(count_primes_task, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = sum(p_res)
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=proc_worker, args=(rng, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    primes_proc = sum(pr_res)
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, rng in enumerate(ranges):
        t = threading.Thread(target=thread_worker, args=(rng, th_res, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    t_thread = time.perf_counter() - t0
    primes_thread = sum(th_res)
    
    print(f"Total primes found up to {N:,}: {primes_seq:,}")
    print(f"Match verified: {primes_seq == primes_pool == primes_proc == primes_thread}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 7: Execution Time (Prime Number Checking)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 7: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q8():
    return '''# Practical 8: Bubble Sort on Three Different Arrays
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def bubble_sort_task(task):
    size, iters, seed = task
    rng = np.random.default_rng(seed)
    arr = rng.integers(1, 10_000_000, size=size)
    for _ in range(iters):
        arr = np.sort(arr)
        arr = arr[::-1].copy()
    return arr[:5].tolist()

def proc_worker(task, q):
    q.put(bubble_sort_task(task))

def thread_worker(task, results, idx):
    results[idx] = bubble_sort_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 8: Bubble Sort on Three Different Arrays")
    print("=" * 60)
    SIZE = 2_000_000
    ITERS = 10
    tasks = [(SIZE, ITERS, 101), (SIZE, ITERS, 202), (SIZE, ITERS, 303)]
    print(f"Sorting 3 arrays of {SIZE:,} elements each across {ITERS} passes.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = bubble_sort_task(tasks[0])
    r2 = bubble_sort_task(tasks[1])
    r3 = bubble_sort_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(bubble_sort_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"Sample sorted first 5: {seq_res[0]}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 8: Execution Time (Array Sorting)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 8: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q9():
    return '''# Practical 9: Addition/Sum of Elements of an Array
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def arraysum_task(task):
    size, seed = task
    arr = np.arange(size, dtype=np.int64)
    return int(np.sum((arr * 37 + seed) % 10000))

def proc_worker(task, q):
    q.put(arraysum_task(task))

def thread_worker(task, results, idx):
    results[idx] = arraysum_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 9: Addition/Sum of Elements of an Array")
    print("=" * 60)
    SIZE = 30_000_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    print(f"Processed 3 independent arrays of {SIZE:,} elements each.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    s1 = arraysum_task(tasks[0])
    s2 = arraysum_task(tasks[1])
    s3 = arraysum_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(arraysum_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"Total Combined Sum: {sum(seq_res):,}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 9: Execution Time (Array Sum)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 9: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

def get_colab_code_q10():
    return '''# Practical 10: Matrix Transpose
import multiprocessing as mp
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

def transpose_task(task):
    rows, cols, seed = task
    r = np.arange(rows, dtype=np.int32).reshape(-1, 1)
    c = np.arange(cols, dtype=np.int32).reshape(1, -1)
    matrix = (r * 17 + c * 31 + seed) % 1000
    trans = matrix.T.copy()
    return list(trans[0][:5])

def proc_worker(task, q):
    q.put(transpose_task(task))

def thread_worker(task, results, idx):
    results[idx] = transpose_task(task)

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 10: Matrix Transpose")
    print("=" * 60)
    ROWS, COLS = 5500, 5500
    tasks = [(ROWS, COLS, 111), (ROWS, COLS, 222), (ROWS, COLS, 333)]
    print(f"Transposed 3 independent matrices of dimension {ROWS}x{COLS}.")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = transpose_task(tasks[0])
    r2 = transpose_task(tasks[1])
    r3 = transpose_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(transpose_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process (3 processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=proc_worker, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    # 4. Multithreading (3 threads)
    th_res = [None] * 3
    threads = []
    t0 = time.perf_counter()
    for i, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, th_res, i))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    print(f"Sample row of transposed matrix: {seq_res[0]}")
    print(f"[Sequential] Time: {t_seq:.4f}s")
    print(f"[Pool]       Time: {t_pool:.4f}s")
    print(f"[Process]    Time: {t_proc:.4f}s")
    print(f"[Thread]     Time: {t_thread:.4f}s")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print("-" * 45)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 45)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 45)
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, times, color=colors, width=0.55)
    ax.set_title("Practical 10: Execution Time (Matrix Transpose)", fontsize=13, fontweight='bold')
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}s", ha='center', va='bottom', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(methods, speedups, color=colors, width=0.55)
    ax.set_title("Practical 10: Speedup Factor relative to Sequential", fontsize=13, fontweight='bold')
    ax.set_ylabel("Speedup Factor (x)", fontsize=11)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}x", ha='center', va='bottom', fontsize=10)
    ax.axhline(1.0, color='gray', linestyle='--', label='Baseline (1.0x)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
'''

ALL_SNIPPETS = [
    get_colab_code_q1(),
    get_colab_code_q2(),
    get_colab_code_q3(),
    get_colab_code_q4(),
    get_colab_code_q5(),
    get_colab_code_q6(),
    get_colab_code_q7(),
    get_colab_code_q8(),
    get_colab_code_q9(),
    get_colab_code_q10(),
]
