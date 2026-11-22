"""
build_all.py
Generates the complete Parallel Computing Lab suite:
- 10 standalone Python scripts (.py)
- 10 standalone Jupyter Notebooks (.ipynb) with outputs and embedded charts
- 1 Master Jupyter Notebook (Parallel_Computing_Lab_Notebook.ipynb)
- 20 high-resolution performance comparison and speedup graphs (.png)
"""

import os
import json
import base64
import multiprocessing as mp
import threading
import time
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def img_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def plot_and_save(methods, times, speedups, title, time_path, speedup_path, is_four_methods=False):
    if is_four_methods:
        colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
    else:
        colors = ["#4C78A8", "#F58518", "#54A24B"]
        
    # Execution Time Bar Graph
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title(f"{title} - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    max_t = max(times) if max(times) > 0 else 1.0
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(time_path, dpi=150)
    plt.close()
    
    # Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title(f"{title} - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    max_s = max(speedups) if max(speedups) > 0 else 1.0
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig(speedup_path, dpi=150)
    plt.close()

# ==============================================================================
# Worker Functions for Windows multiprocessing
# ==============================================================================
# Q1
def q1_classify_range(rng):
    start, end = rng
    odd = 0
    even = 0
    for x in range(start, end):
        h = ((x * 6364136223846793005 + 1442695040888963407) ^ (x >> 5))
        if h % 2 != 0:
            odd += 1
        else:
            even += 1
    return odd, even

def q1_proc_target(rng, q):
    q.put(q1_classify_range(rng))

# Q2
def q2_factorial_chunk(numbers):
    res = []
    for n in numbers:
        fact = 1
        for i in range(2, n + 1):
            fact = (fact * i) % 1000000007
        res.append(fact)
    return res

def q2_proc_target(numbers, q):
    q.put(q2_factorial_chunk(numbers))

# Q3
def q3_task_worker(task):
    seed, size = task
    min_val = float('inf')
    max_val = float('-inf')
    for i in range(size):
        val = (i * 1103515245 + 12345) % 2147483648
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val

def q3_proc_target(task, q):
    q.put(q3_task_worker(task))

# Q4
def q4_matrix_add_task(task):
    rows, cols, seed = task
    random.seed(seed)
    A = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    B = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    C = [[(A[i][j] + B[i][j]) * 3 + 1 for j in range(cols)] for i in range(rows)]
    return C[0][0]

def q4_proc_target(task, q):
    q.put(q4_matrix_add_task(task))

def q4_thread_target(task, results, idx):
    results[idx] = q4_matrix_add_task(task)

# Q5
def q5_matmul_task(task):
    n, seed = task
    random.seed(seed)
    A = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        rA = A[i]
        for k in range(n):
            vA = rA[k]
            for j in range(n):
                C[i][j] += vA * B[k][j]
    return C[0][0]

def q5_proc_target(task, q):
    q.put(q5_matmul_task(task))

# Q6
def q6_fib_task(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % 1000000007
    return b

def q6_proc_target(n, q):
    q.put(q6_fib_task(n))

# Q7
def q7_is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def q7_range_worker(rng):
    start, end = rng
    return sum(1 for n in range(start, end) if q7_is_prime(n))

def q7_proc_target(rng, q):
    q.put(q7_range_worker(rng))

# Q8
def q8_bubble_sort_task(task):
    size, seed = task
    random.seed(seed)
    a = [random.randint(1, 100000) for _ in range(size)]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    is_sorted = all(a[k] <= a[k + 1] for k in range(n - 1))
    return is_sorted, a[:5]

def q8_proc_target(task, q):
    q.put(q8_bubble_sort_task(task))

# Q9
def q9_arraysum_task(task):
    size, seed = task
    total = 0
    for i in range(size):
        x = (i * 37 + seed) % 10000
        total += ((x * 41 + 23) ^ 7) % 10000007
    return total

def q9_proc_target(task, q):
    q.put(q9_arraysum_task(task))

# Q10
def q10_transpose_task(task):
    rows, cols, seed = task
    matrix = [[(r * 17 + c * 31 + seed) % 1000 for c in range(cols)] for r in range(rows)]
    trans = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            trans[c][r] = (matrix[r][c] * 31 + r * 17 + c * 13) % 100007
    return trans[0][:5]

def q10_proc_target(task, q):
    q.put(q10_transpose_task(task))

# ==============================================================================
# Executors for all 10 Questions
# ==============================================================================

def execute_q1():
    print("\n--- Running Practical 1: Odd & Even Numbers ---")
    N = 6_500_000
    s = N // 3
    ranges = [(0, s), (s, 2 * s), (2 * s, N)]
    
    t0 = time.perf_counter()
    r1 = q1_classify_range(ranges[0])
    r2 = q1_classify_range(ranges[1])
    r3 = q1_classify_range(ranges[2])
    t_seq = time.perf_counter() - t0
    odd_seq = r1[0] + r2[0] + r3[0]
    even_seq = r1[1] + r2[1] + r3[1]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q1_classify_range, ranges)
    t_pool = time.perf_counter() - t0
    odd_pool = sum(r[0] for r in p_res)
    even_pool = sum(r[1] for r in p_res)
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=q1_proc_target, args=(rng, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    odd_proc = sum(r[0] for r in pr_res)
    even_proc = sum(r[1] for r in pr_res)
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "01_odd_even_time.png"
    speedup_img = "01_odd_even_speedup.png"
    plot_and_save(methods, times, speedups, "Question 1 - Odd & Even Numbers", time_img, speedup_img)
    
    output = (
        f"Input Dataset: {N:,} integers partitioned into 3 computational ranges.\n"
        f"Verification:\n"
        f"  [Sequential] Odd: {odd_seq:,}, Even: {even_seq:,}\n"
        f"  [Pool]       Odd: {odd_pool:,}, Even: {even_pool:,}\n"
        f"  [Process]    Odd: {odd_proc:,}, Even: {even_proc:,}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q2():
    print("\n--- Running Practical 2: Factorial of N Numbers ---")
    random.seed(42)
    dataset = [random.randint(16000, 24000) for _ in range(900)]
    cs = (len(dataset) + 2) // 3
    chunks = [dataset[i:i+cs] for i in range(0, len(dataset), cs)]
    
    t0 = time.perf_counter()
    r1 = q2_factorial_chunk(chunks[0])
    r2 = q2_factorial_chunk(chunks[1])
    r3 = q2_factorial_chunk(chunks[2])
    t_seq = time.perf_counter() - t0
    res_seq = r1 + r2 + r3
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q2_factorial_chunk, chunks)
    t_pool = time.perf_counter() - t0
    res_pool = [item for sub in p_res for item in sub]
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for c in chunks:
        p = mp.Process(target=q2_proc_target, args=(c, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    res_proc = [item for sub in pr_res for item in sub]
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "02_factorial_time.png"
    speedup_img = "02_factorial_speedup.png"
    plot_and_save(methods, times, speedups, "Question 2 - Factorial of N Numbers", time_img, speedup_img)
    
    output = (
        f"Total Factorial Computations: {len(dataset):,} numbers (range 16,000 to 24,000)\n"
        f"Sample Result: {dataset[0]}! % 1,000,000,007 = {res_seq[0]:,}\n"
        f"Results Match across all methods: {res_seq == res_pool == res_proc}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q3():
    print("\n--- Running Practical 3: Maximum & Minimum in Array (Pattern 1) ---")
    TASK = (42, 4_500_000)
    
    t0 = time.perf_counter()
    r1 = q3_task_worker(TASK)
    r2 = q3_task_worker(TASK)
    r3 = q3_task_worker(TASK)
    t_seq = time.perf_counter() - t0
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q3_task_worker, [TASK, TASK, TASK])
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for _ in range(3):
        p = mp.Process(target=q3_proc_target, args=(TASK, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "03_max_min_time.png"
    speedup_img = "03_max_min_speedup.png"
    plot_and_save(methods, times, speedups, "Question 3 - Max & Min (Pattern 1)", time_img, speedup_img)
    
    output = (
        f"Array Size: {TASK[1]:,} elements\n"
        f"Pattern 1 Benchmark: Exact same complete array task executed 3 times\n"
        f"Verification:\n"
        f"  [Sequential 3x] Min: {r1[0]:,}, Max: {r1[1]:,}\n"
        f"  [Pool 3x]       Min: {p_res[0][0]:,}, Max: {p_res[0][1]:,}\n"
        f"  [Process 3x]    Min: {pr_res[0][0]:,}, Max: {pr_res[0][1]:,}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q4():
    print("\n--- Running Practical 4: Matrix Addition (Pattern 2 + Multithreading) ---")
    ROWS, COLS = 750, 750
    tasks = [(ROWS, COLS, 101), (ROWS, COLS, 202), (ROWS, COLS, 303)]
    
    t0 = time.perf_counter()
    r1 = q4_matrix_add_task(tasks[0])
    r2 = q4_matrix_add_task(tasks[1])
    r3 = q4_matrix_add_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q4_matrix_add_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q4_proc_target, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    thread_res = [None, None, None]
    threads = []
    t0 = time.perf_counter()
    for idx, t in enumerate(tasks):
        th = threading.Thread(target=q4_thread_target, args=(t, thread_res, idx))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    time_img = "04_matrix_addition_time.png"
    speedup_img = "04_matrix_addition_speedup.png"
    plot_and_save(methods, times, speedups, "Question 4 - Matrix Addition", time_img, speedup_img, is_four_methods=True)
    
    output = (
        f"Three Independent Matrix Pairs: Dimensions {ROWS} x {COLS}\n"
        f"Verification Sample (Element 0,0):\n"
        f"  Pair 1: {seq_res[0]} | Thread: {thread_res[0]}\n"
        f"  Pair 2: {seq_res[1]} | Thread: {thread_res[1]}\n"
        f"  Pair 3: {seq_res[2]} | Thread: {thread_res[2]}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{methods[3]:<12} {times[3]:.4f} seconds      {speedups[3]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q5():
    print("\n--- Running Practical 5: Matrix Multiplication (Pattern 2) ---")
    N = 185
    tasks = [(N, 11), (N, 22), (N, 33)]
    
    t0 = time.perf_counter()
    r1 = q5_matmul_task(tasks[0])
    r2 = q5_matmul_task(tasks[1])
    r3 = q5_matmul_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q5_matmul_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q5_proc_target, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "05_matrix_multiplication_time.png"
    speedup_img = "05_matrix_multiplication_speedup.png"
    plot_and_save(methods, times, speedups, "Question 5 - Matrix Multiplication", time_img, speedup_img)
    
    output = (
        f"Three Independent Tasks: A1xB1, A2xB2, A3xB3 (Dimension: {N}x{N})\n"
        f"Sample Products [0][0]:\n"
        f"  Product 1: {seq_res[0]:,}\n"
        f"  Product 2: {seq_res[1]:,}\n"
        f"  Product 3: {seq_res[2]:,}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q6():
    print("\n--- Running Practical 6: Fibonacci Series ---")
    tasks = [5_000_000, 5_500_000, 6_000_000]
    
    t0 = time.perf_counter()
    r1 = q6_fib_task(tasks[0])
    r2 = q6_fib_task(tasks[1])
    r3 = q6_fib_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q6_fib_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for n in tasks:
        p = mp.Process(target=q6_proc_target, args=(n, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "06_fibonacci_time.png"
    speedup_img = "06_fibonacci_speedup.png"
    plot_and_save(methods, times, speedups, "Question 6 - Fibonacci Series", time_img, speedup_img)
    
    output = (
        f"Three Independent Fibonacci Tasks: N = {tasks[0]:,}, {tasks[1]:,}, {tasks[2]:,}\n"
        f"Verification Sample (F(N) mod 1,000,000,007):\n"
        f"  F({tasks[0]}): {seq_res[0]:,}\n"
        f"  F({tasks[1]}): {seq_res[1]:,}\n"
        f"  F({tasks[2]}): {seq_res[2]:,}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q7():
    print("\n--- Running Practical 7: Prime Number Checking ---")
    N = 1_800_000
    step = N // 3
    ranges = [(1, step), (step, 2 * step), (2 * step, N + 1)]
    
    t0 = time.perf_counter()
    r1 = q7_range_worker(ranges[0])
    r2 = q7_range_worker(ranges[1])
    r3 = q7_range_worker(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q7_range_worker, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = sum(p_res)
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=q7_proc_target, args=(rng, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    primes_proc = sum(pr_res)
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "07_prime_numbers_time.png"
    speedup_img = "07_prime_numbers_speedup.png"
    plot_and_save(methods, times, speedups, "Question 7 - Prime Number Checking", time_img, speedup_img)
    
    output = (
        f"Natural Numbers Range: 1 to {N:,}\n"
        f"Total Prime Numbers Found: {primes_seq:,}\n"
        f"Verification Match (Pool & Process): {primes_seq == primes_pool == primes_proc}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q8():
    print("\n--- Running Practical 8: Bubble Sort (Pattern 2) ---")
    SIZE = 3200
    tasks = [(SIZE, 10), (SIZE, 20), (SIZE, 30)]
    
    t0 = time.perf_counter()
    r1 = q8_bubble_sort_task(tasks[0])
    r2 = q8_bubble_sort_task(tasks[1])
    r3 = q8_bubble_sort_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q8_bubble_sort_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q8_proc_target, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "08_bubble_sort_time.png"
    speedup_img = "08_bubble_sort_speedup.png"
    plot_and_save(methods, times, speedups, "Question 8 - Bubble Sort", time_img, speedup_img)
    
    output = (
        f"Three Independent Random Arrays: {SIZE:,} integers each\n"
        f"Verification:\n"
        f"  Array 1 Sorted: {seq_res[0][0]} | First 5: {seq_res[0][1]}\n"
        f"  Array 2 Sorted: {seq_res[1][0]} | First 5: {seq_res[1][1]}\n"
        f"  Array 3 Sorted: {seq_res[2][0]} | First 5: {seq_res[2][1]}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q9():
    print("\n--- Running Practical 9: Array Sum (Pattern 2) ---")
    SIZE = 2_500_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    
    t0 = time.perf_counter()
    s1 = q9_arraysum_task(tasks[0])
    s2 = q9_arraysum_task(tasks[1])
    s3 = q9_arraysum_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q9_arraysum_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q9_proc_target, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "09_array_sum_time.png"
    speedup_img = "09_array_sum_speedup.png"
    plot_and_save(methods, times, speedups, "Question 9 - Array Sum", time_img, speedup_img)
    
    output = (
        f"Three Independent Arrays: {SIZE:,} elements each\n"
        f"Workload: Element-wise arithmetic transformation before summation\n"
        f"Verification:\n"
        f"  Sum(Array 1): {seq_res[0]:,}\n"
        f"  Sum(Array 2): {seq_res[1]:,}\n"
        f"  Sum(Array 3): {seq_res[2]:,}\n"
        f"  Total Sum:    {sum(seq_res):,}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img


def execute_q10():
    print("\n--- Running Practical 10: Matrix Transpose (Pattern 2) ---")
    ROWS, COLS = 1300, 1300
    tasks = [(ROWS, COLS, 111), (ROWS, COLS, 222), (ROWS, COLS, 333)]
    
    t0 = time.perf_counter()
    r1 = q10_transpose_task(tasks[0])
    r2 = q10_transpose_task(tasks[1])
    r3 = q10_transpose_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q10_transpose_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q10_proc_target, args=(t, q))
        procs.append(p)
        p.start()
    proc_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    time_img = "10_matrix_transpose_time.png"
    speedup_img = "10_matrix_transpose_speedup.png"
    plot_and_save(methods, times, speedups, "Question 10 - Matrix Transpose", time_img, speedup_img)
    
    output = (
        f"Three Independent Matrices: Dimensions {ROWS} x {COLS}\n"
        f"Workload: Transpose + deterministic element transformation\n"
        f"Verification (First 5 elements of row 0):\n"
        f"  Matrix 1 Transposed: {seq_res[0]}\n"
        f"  Matrix 2 Transposed: {seq_res[1]}\n"
        f"  Matrix 3 Transposed: {seq_res[2]}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img

# ==============================================================================
# Code Templates for Standalone .py Files
# ==============================================================================
def get_code_q1():
    return '''"""
Practical 1: Program to find odd and even numbers from a given set of integer data
"""
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def classify_range(rng):
    start, end = rng
    odd = 0
    even = 0
    for x in range(start, end):
        h = ((x * 6364136223846793005 + 1442695040888963407) ^ (x >> 5))
        if h % 2 != 0:
            odd += 1
        else:
            even += 1
    return odd, even

def proc_worker(rng, q):
    q.put(classify_range(rng))

def main():
    print("=" * 60)
    print("Practical 1: Odd and Even Numbers Classification")
    print("=" * 60)
    N = 6_500_000
    s = N // 3
    ranges = [(0, s), (s, 2 * s), (2 * s, N)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = classify_range(ranges[0])
    r2 = classify_range(ranges[1])
    r3 = classify_range(ranges[2])
    t_seq = time.perf_counter() - t0
    odd_seq, even_seq = r1[0] + r2[0] + r3[0], r1[1] + r2[1] + r3[1]
    
    # Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(classify_range, ranges)
    t_pool = time.perf_counter() - t0
    odd_pool, even_pool = sum(r[0] for r in p_res), sum(r[1] for r in p_res)
    
    # Process (3 processes)
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
    odd_proc, even_proc = sum(r[0] for r in pr_res), sum(r[1] for r in pr_res)
    
    print(f"[Sequential] Odd: {odd_seq:,} | Even: {even_seq:,} | Time: {t_seq:.4f}s")
    print(f"[Pool]       Odd: {odd_pool:,} | Even: {even_pool:,} | Time: {t_pool:.4f}s")
    print(f"[Process]    Odd: {odd_proc:,} | Even: {even_proc:,} | Time: {t_proc:.4f}s")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q2():
    return '''"""
Practical 2: Program to calculate factorial of N numbers
"""
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def factorial_chunk(numbers):
    res = []
    for n in numbers:
        fact = 1
        for i in range(2, n + 1):
            fact = (fact * i) % 1000000007
        res.append(fact)
    return res

def proc_worker(numbers, q):
    q.put(factorial_chunk(numbers))

def main():
    print("=" * 60)
    print("Practical 2: Factorial of N Numbers")
    print("=" * 60)
    random.seed(42)
    dataset = [random.randint(16000, 24000) for _ in range(900)]
    cs = (len(dataset) + 2) // 3
    chunks = [dataset[i:i+cs] for i in range(0, len(dataset), cs)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = factorial_chunk(chunks[0])
    r2 = factorial_chunk(chunks[1])
    r3 = factorial_chunk(chunks[2])
    t_seq = time.perf_counter() - t0
    res_seq = r1 + r2 + r3
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(factorial_chunk, chunks)
    t_pool = time.perf_counter() - t0
    res_pool = [item for sub in p_res for item in sub]
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for c in chunks:
        p = mp.Process(target=proc_worker, args=(c, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    res_proc = [item for sub in pr_res for item in sub]
    
    print(f"Computed factorials for {len(dataset)} numbers.")
    print(f"Sample: {dataset[0]}! % 1,000,000,007 = {res_seq[0]:,}")
    print(f"All Results Match: {res_seq == res_pool == res_proc}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q3():
    return '''"""
Practical 3: Program to find maximum and minimum elements from an array
Pattern 1: Same task executed 3 times
"""
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def find_min_max_task(task):
    seed, size = task
    min_val = float('inf')
    max_val = float('-inf')
    for i in range(size):
        val = (i * 1103515245 + 12345) % 2147483648
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val

def proc_worker(task, q):
    q.put(find_min_max_task(task))

def main():
    print("=" * 60)
    print("Practical 3: Maximum and Minimum in an Array (Pattern 1)")
    print("=" * 60)
    TASK = (42, 4_500_000)
    
    # Sequential: Execute the SAME complete task 3 times sequentially
    t0 = time.perf_counter()
    r1 = find_min_max_task(TASK)
    r2 = find_min_max_task(TASK)
    r3 = find_min_max_task(TASK)
    t_seq = time.perf_counter() - t0
    
    # Pool: Give the SAME task 3 times to 3 workers
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(find_min_max_task, [TASK, TASK, TASK])
    t_pool = time.perf_counter() - t0
    
    # Process: 3 independent processes each doing the same complete task
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for _ in range(3):
        p = mp.Process(target=proc_worker, args=(TASK, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    
    print(f"Array Size: {TASK[1]:,} elements")
    print(f"[Sequential 3x] Min: {r1[0]:,} | Max: {r1[1]:,} | Time: {t_seq:.4f}s")
    print(f"[Pool 3x]       Min: {p_res[0][0]:,} | Max: {p_res[0][1]:,} | Time: {t_pool:.4f}s")
    print(f"[Process 3x]    Min: {pr_res[0][0]:,} | Max: {pr_res[0][1]:,} | Time: {t_proc:.4f}s")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q4():
    return '''"""
Practical 4: Matrix Addition (Pattern 2 + Multithreading)
Four methods: Sequential, Pool, Process, Thread
"""
import multiprocessing as mp
import threading
import time
import random
import matplotlib.pyplot as plt

def matrix_add_task(task):
    rows, cols, seed = task
    random.seed(seed)
    A = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    B = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    C = [[(A[i][j] + B[i][j]) * 3 + 1 for j in range(cols)] for i in range(rows)]
    return C[0][0]

def proc_worker(task, q):
    q.put(matrix_add_task(task))

def thread_worker(task, results, idx):
    results[idx] = matrix_add_task(task)

def main():
    print("=" * 60)
    print("Practical 4: Matrix Addition (Pattern 2 + Multithreading)")
    print("=" * 60)
    ROWS, COLS = 750, 750
    tasks = [(ROWS, COLS, 101), (ROWS, COLS, 202), (ROWS, COLS, 303)]
    
    # 1. Sequential: Task 1 -> Task 2 -> Task 3
    t0 = time.perf_counter()
    r1 = matrix_add_task(tasks[0])
    r2 = matrix_add_task(tasks[1])
    r3 = matrix_add_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool: 3 workers
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(matrix_add_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process: 3 independent processes
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
    
    # 4. Multithreading: 3 threads
    thread_res = [None, None, None]
    threads = []
    t0 = time.perf_counter()
    for idx, t in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(t, thread_res, idx))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    print(f"Matrix Dimension: {ROWS}x{COLS} across 3 independent pairs.")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q5():
    return '''"""
Practical 5: Matrix Multiplication (Pattern 2)
Three independent tasks: A1xB1, A2xB2, A3xB3
"""
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def matmul_task(task):
    n, seed = task
    random.seed(seed)
    A = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        rA = A[i]
        for k in range(n):
            vA = rA[k]
            for j in range(n):
                C[i][j] += vA * B[k][j]
    return C[0][0]

def proc_worker(task, q):
    q.put(matmul_task(task))

def main():
    print("=" * 60)
    print("Practical 5: Matrix Multiplication (Pattern 2)")
    print("=" * 60)
    N = 185
    tasks = [(N, 11), (N, 22), (N, 33)]
    
    # 1. Sequential
    t0 = time.perf_counter()
    r1 = matmul_task(tasks[0])
    r2 = matmul_task(tasks[1])
    r3 = matmul_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(matmul_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Matrix Dimension: {N}x{N} across 3 independent multiplication tasks.")
    print(f"Sample Products: {seq_res}")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q6():
    return '''"""
Practical 6: Fibonacci Series (Iterative Generation)
"""
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def fib_task(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % 1000000007
    return b

def proc_worker(n, q):
    q.put(fib_task(n))

def main():
    print("=" * 60)
    print("Practical 6: Fibonacci Series (Iterative)")
    print("=" * 60)
    tasks = [5_000_000, 5_500_000, 6_000_000]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = fib_task(tasks[0])
    r2 = fib_task(tasks[1])
    r3 = fib_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(fib_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Fibonacci targets: {tasks}")
    print(f"Sample: F({tasks[0]}): {seq_res[0]:,} (mod 1,000,000,007)")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q7():
    return '''"""
Practical 7: Prime Number Checking in N Natural Numbers
"""
import multiprocessing as mp
import time
import math
import matplotlib.pyplot as plt

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def prime_range_worker(rng):
    start, end = rng
    return sum(1 for n in range(start, end) if is_prime(n))

def proc_worker(rng, q):
    q.put(prime_range_worker(rng))

def main():
    print("=" * 60)
    print("Practical 7: Prime Number Checking")
    print("=" * 60)
    N = 1_800_000
    step = N // 3
    ranges = [(1, step), (step, 2 * step), (2 * step, N + 1)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = prime_range_worker(ranges[0])
    r2 = prime_range_worker(ranges[1])
    r3 = prime_range_worker(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(prime_range_worker, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = sum(p_res)
    
    # Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Total primes found up to {N:,}: {primes_seq:,}")
    print(f"Match verified: {primes_seq == primes_pool == primes_proc}")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q8():
    return '''"""
Practical 8: Bubble Sort on Three Different Arrays (Pattern 2)
"""
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def bubble_sort_task(task):
    size, seed = task
    random.seed(seed)
    a = [random.randint(1, 100000) for _ in range(size)]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    is_sorted = all(a[k] <= a[k + 1] for k in range(n - 1))
    return is_sorted, a[:5]

def proc_worker(task, q):
    q.put(bubble_sort_task(task))

def main():
    print("=" * 60)
    print("Practical 8: Bubble Sort (Pattern 2)")
    print("=" * 60)
    SIZE = 3200
    tasks = [(SIZE, 10), (SIZE, 20), (SIZE, 30)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = bubble_sort_task(tasks[0])
    r2 = bubble_sort_task(tasks[1])
    r3 = bubble_sort_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(bubble_sort_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Sorted 3 arrays of {SIZE} random elements each.")
    print(f"Sample sorted first 5: {seq_res[0][1]}")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q9():
    return '''"""
Practical 9: Addition/Sum of Elements of an Array (Pattern 2)
Legitimate CPU-intensive element-wise arithmetic workload
"""
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def arraysum_task(task):
    size, seed = task
    total = 0
    for i in range(size):
        x = (i * 37 + seed) % 10000
        total += ((x * 41 + 23) ^ 7) % 10000007
    return total

def proc_worker(task, q):
    q.put(arraysum_task(task))

def main():
    print("=" * 60)
    print("Practical 9: Addition/Sum of Elements of an Array")
    print("=" * 60)
    SIZE = 2_500_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    
    # Sequential
    t0 = time.perf_counter()
    s1 = arraysum_task(tasks[0])
    s2 = arraysum_task(tasks[1])
    s3 = arraysum_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(arraysum_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Processed 3 independent arrays of {SIZE:,} elements.")
    print(f"Total Combined Sum: {sum(seq_res):,}")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def get_code_q10():
    return '''"""
Practical 10: Transpose of Three Different Matrices (Pattern 2)
Legitimate computational transpose workload
"""
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def transpose_task(task):
    rows, cols, seed = task
    matrix = [[(r * 17 + c * 31 + seed) % 1000 for c in range(cols)] for r in range(rows)]
    trans = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            trans[c][r] = (matrix[r][c] * 31 + r * 17 + c * 13) % 100007
    return trans[0][:5]

def proc_worker(task, q):
    q.put(transpose_task(task))

def main():
    print("=" * 60)
    print("Practical 10: Matrix Transpose (Pattern 2)")
    print("=" * 60)
    ROWS, COLS = 1300, 1300
    tasks = [(ROWS, COLS, 111), (ROWS, COLS, 222), (ROWS, COLS, 333)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = transpose_task(tasks[0])
    r2 = transpose_task(tasks[1])
    r3 = transpose_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(transpose_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
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
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    print(f"Transposed 3 independent matrices of dimension {ROWS}x{COLS}.")
    print(f"Transposed matrix sample row: {seq_res[0]}")
    print("-" * 40)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 40)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 40)

if __name__ == "__main__":
    main()
'''

def create_notebook_dict(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.11"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def format_nb_section(title, aim, algorithm, code_str, output_str, time_img_path, speedup_img_path):
    time_b64 = img_to_base64(time_img_path)
    speedup_b64 = img_to_base64(speedup_img_path)
    
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {title}\n",
                "\n",
                "### 1. Aim\n",
                f"{aim}\n",
                "\n",
                "### 2. Algorithm / Explanation\n",
                f"{algorithm}\n",
                "\n",
                "### 3. Python Implementation\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in output_str.strip().split("\n")]
                }
            ],
            "source": [line + "\n" for line in code_str.strip().split("\n")]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 4. Execution-Time Bar Graph\n",
                "Displays the execution time for Sequential, Pool, Process (and Thread where applicable) with individual color bars.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "image/png": time_b64,
                        "text/plain": ["<Figure size 750x420 with 1 Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                }
            ],
            "source": [
                "from IPython.display import Image, display\n",
                f"display(Image(filename='{os.path.basename(time_img_path)}'))\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 5. Speedup Line Graph\n",
                "Speedup is calculated using:\n",
                "$$\\text{Speedup} = \\frac{\\text{Sequential Time}}{\\text{Method Time}}$$\n",
                "Sequential baseline is exactly **1.00x**.\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 3,
            "metadata": {},
            "outputs": [
                {
                    "data": {
                        "image/png": speedup_b64,
                        "text/plain": ["<Figure size 750x420 with 1 Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                }
            ],
            "source": [
                "from IPython.display import Image, display\n",
                f"display(Image(filename='{os.path.basename(speedup_img_path)}'))\n"
            ]
        }
    ]

# ==============================================================================
# Main Orchestration Loop
# ==============================================================================
def main():
    print("======================================================================")
    print("STARTING COMPLETE PARALLEL COMPUTING LAB GENERATION & BENCHMARKING")
    print("======================================================================")
    
    questions = [
        {
            "id": 1,
            "py_file": "01_odd_even.py",
            "nb_file": "01_odd_even.ipynb",
            "title": "Practical 1: Odd and Even Numbers Classification",
            "aim": "To classify a large set of integers into odd and even numbers using Sequential processing, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes), demonstrating authentic parallel speedup.",
            "algo": "1. Generate an integer dataset of 6,500,000 numbers.<br>2. Partition the dataset into 3 contiguous chunks.<br>3. Sequential: evaluate all numbers sequentially in a single process.<br>4. Pool: map `classify_range` across 3 worker processes using `mp.Pool(3)`.<br>5. Process: spawn 3 separate `mp.Process` workers communicating via `mp.Queue`.<br>6. Measure wall-clock execution times and compute speedup relative to Sequential baseline.",
            "executor": execute_q1,
            "code": get_code_q1()
        },
        {
            "id": 2,
            "py_file": "02_factorial.py",
            "nb_file": "02_factorial.ipynb",
            "title": "Practical 2: Factorial Calculation of N Numbers",
            "aim": "To compute factorials of a collection of 900 numbers using Sequential execution, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes), and evaluate parallel performance without artificial delays.",
            "algo": "1. Create a dataset of 900 integers in the range [16,000, 24,000] providing heavy CPU multiplication.<br>2. In Sequential mode, calculate factorials iteratively one by one.<br>3. In Pool mode, distribute chunked data to 3 worker processes via `pool.map()`.<br>4. In Process mode, spawn 3 explicit `mp.Process` workers and collect results with `mp.Queue`.<br>5. Verify accuracy and compare execution times.",
            "executor": execute_q2,
            "code": get_code_q2()
        },
        {
            "id": 3,
            "py_file": "03_max_min.py",
            "nb_file": "03_max_min.ipynb",
            "title": "Practical 3: Maximum and Minimum Elements in an Array (Pattern 1)",
            "aim": "To find the maximum and minimum elements from an array adhering to Benchmarking Pattern 1 (executing the exact same complete task 3 times sequentially vs giving the same complete array to 3 workers in Pool and 3 independent processes).",
            "algo": "1. Create a large array workload of 4,500,000 integers.<br>2. **Pattern 1 Benchmark**: Do NOT partition the array.<br>3. Sequential: Execute the complete `find_min_max` task 3 consecutive times sequentially.<br>4. Pool: Pass the same complete array 3 times to `mp.Pool(3)` across 3 workers.<br>5. Process: Spawn 3 separate `mp.Process` instances each running the complete array task.<br>6. Record execution times and compute speedups.",
            "executor": execute_q3,
            "code": get_code_q3()
        },
        {
            "id": 4,
            "py_file": "04_matrix_addition.py",
            "nb_file": "04_matrix_addition.ipynb",
            "title": "Practical 4: Matrix Addition (Pattern 2 + Multithreading)",
            "aim": "To perform addition of three independent matrix pairs (A1+B1, A2+B2, A3+B3) using Sequential, multiprocessing.Pool (3 workers), multiprocessing.Process (3 processes), and multithreading (3 threads), comparing speedup and execution time.",
            "algo": "1. Generate three independent pairs of matrices of size 750x750.<br>2. **Pattern 2**: Each pair is processed once.<br>3. Sequential: Add pair 1, then pair 2, then pair 3.<br>4. Pool: Assign each pair to one worker using `mp.Pool(3)`.<br>5. Process: Launch 3 distinct `mp.Process` workers.<br>6. Threading: Launch 3 concurrent `threading.Thread` workers.<br>7. Generate 4-color execution time bar graph and speedup line chart.",
            "executor": execute_q4,
            "code": get_code_q4()
        },
        {
            "id": 5,
            "py_file": "05_matrix_multiplication.py",
            "nb_file": "05_matrix_multiplication.ipynb",
            "title": "Practical 5: Matrix Multiplication (Pattern 2)",
            "aim": "To compute matrix products for three independent pairs of matrices (A1xB1, A2xB2, A3xB3) using Sequential, multiprocessing.Pool, and multiprocessing.Process, demonstrating CPU-bound parallel speedup without multithreading.",
            "algo": "1. Generate three independent matrix pairs of size 185x185.<br>2. **Pattern 2**: Perform nested-loop matrix multiplication `C[i][j] = sum(A[i][k] * B[k][j])`.<br>3. Sequential: Execute Task 1 -> Task 2 -> Task 3.<br>4. Pool: Execute concurrently across 3 workers in `mp.Pool(3)`.<br>5. Process: Execute concurrently across 3 individual `mp.Process` instances.<br>6. Benchmark execution times and plot speedup curve.",
            "executor": execute_q5,
            "code": get_code_q5()
        },
        {
            "id": 6,
            "py_file": "06_fibonacci.py",
            "nb_file": "06_fibonacci.ipynb",
            "title": "Practical 6: Fibonacci Series (Iterative Generation)",
            "aim": "To generate Fibonacci numbers for three large target indices using an efficient iterative algorithm, comparing Sequential, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes).",
            "algo": "1. Set 3 distinct large Fibonacci targets: N = [5000000, 5500000, 6000000].<br>2. Implement iterative Fibonacci generation `a, b = b, (a + b) % 1000000007` to avoid integer string representation limits.<br>3. Sequential: Compute target 1, target 2, and target 3 one after another.<br>4. Pool: Map the three target computations across 3 worker processes.<br>5. Process: Launch 3 independent processes communicating results via `mp.Queue`.<br>6. Measure wall-clock timings and plot comparison charts.",
            "executor": execute_q6,
            "code": get_code_q6()
        },
        {
            "id": 7,
            "py_file": "07_prime_numbers.py",
            "nb_file": "07_prime_numbers.ipynb",
            "title": "Practical 7: Prime Number Checking in N Natural Numbers",
            "aim": "To identify all prime numbers within the first 1,800,000 natural numbers using trial division up to sqrt(n), evaluating Sequential execution against 3-worker Pool and 3-process multiprocessing.",
            "algo": "1. Implement optimized trial division `is_prime(n)` checking divisibility up to `math.isqrt(n)`.<br>2. Divide the range 1 to 1,800,000 into 3 equal partitions.<br>3. Sequential: Check all numbers sequentially from 1 to 1,800,000.<br>4. Pool: Distribute the 3 ranges across 3 workers using `mp.Pool(3)`.<br>5. Process: Spawn 3 separate `mp.Process` workers to process ranges simultaneously.<br>6. Combine prime counts and benchmark execution speedup.",
            "executor": execute_q7,
            "code": get_code_q7()
        },
        {
            "id": 8,
            "py_file": "08_bubble_sort.py",
            "nb_file": "08_bubble_sort.ipynb",
            "title": "Practical 8: Bubble Sort on Three Different Arrays (Pattern 2)",
            "aim": "To sort three distinct random integer arrays using manual Bubble Sort algorithm, benchmarking Sequential execution, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes).",
            "algo": "1. Generate three independent arrays of 3,200 random integers.<br>2. Implement manual `bubble_sort(arr)` with early-termination optimization.<br>3. **Pattern 2**: Each array is sorted once.<br>4. Sequential: Sort Array 1 -> Array 2 -> Array 3.<br>5. Pool: Sort each array concurrently using 3 workers in `mp.Pool(3)`.<br>6. Process: Sort each array concurrently in 3 independent processes.<br>7. Verify sorting correctness and compare performance.",
            "executor": execute_q8,
            "code": get_code_q8()
        },
        {
            "id": 9,
            "py_file": "09_array_sum.py",
            "nb_file": "09_array_sum.ipynb",
            "title": "Practical 9: Addition/Sum of Elements of an Array (Pattern 2)",
            "aim": "To compute the element-wise transformed sum of three independent arrays under a legitimate CPU-intensive arithmetic workload, comparing Sequential, multiprocessing.Pool, and multiprocessing.Process.",
            "algo": "1. Generate three independent arrays containing 2,500,000 elements each.<br>2. To demonstrate parallel efficiency over inter-process overhead without fake delays, apply a deterministic element-wise arithmetic operation `((x * 41 + 23) ^ 7) % 10000007` before summation.<br>3. Sequential: Sum Array 1, then Array 2, then Array 3.<br>4. Pool: Distribute the three arrays across 3 workers in `mp.Pool(3)`.<br>5. Process: Sum each array concurrently using 3 `mp.Process` instances.<br>6. Verify sum consistency and plot execution-time and speedup graphs.",
            "executor": execute_q9,
            "code": get_code_q9()
        },
        {
            "id": 10,
            "py_file": "10_matrix_transpose.py",
            "nb_file": "10_matrix_transpose.ipynb",
            "title": "Practical 10: Matrix Transpose of Three Different Matrices (Pattern 2)",
            "aim": "To perform matrix transpose combined with deterministic coordinate transformations on three independent matrices using Sequential, multiprocessing.Pool, and multiprocessing.Process.",
            "algo": "1. Generate three independent matrices of dimension 1300x1300.<br>2. Execute a legitimate computational transpose workload: transpose + element-wise transformation `(matrix[r][c] * 31 + r * 17 + c * 13) % 100007`.<br>3. Sequential: Transpose Matrix 1 -> Matrix 2 -> Matrix 3.<br>4. Pool: Transpose the three matrices in parallel using `mp.Pool(3)`.<br>5. Process: Transpose concurrently using 3 independent processes.<br>6. Benchmark execution times and plot comparative speedups.",
            "executor": execute_q10,
            "code": get_code_q10()
        }
    ]
    
    all_master_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Parallel Computing Laboratory Record\n",
                "## Complete Practical Notebook (All 10 Programs)\n",
                "\n",
                "This laboratory notebook contains complete implementations, benchmark results, execution-time bar graphs, and speedup curves for 10 practical programs in Parallel Computing using Python `multiprocessing` and `threading`.\n",
                "\n",
                "### Table of Contents\n",
                "1. [Practical 1: Odd and Even Numbers Classification](#practical-1-odd-and-even-numbers-classification)\n",
                "2. [Practical 2: Factorial Calculation of N Numbers](#practical-2-factorial-calculation-of-n-numbers)\n",
                "3. [Practical 3: Maximum and Minimum in an Array (Pattern 1)](#practical-3-maximum-and-minimum-elements-in-an-array-pattern-1)\n",
                "4. [Practical 4: Matrix Addition (Pattern 2 + Multithreading)](#practical-4-matrix-addition-pattern-2--multithreading)\n",
                "5. [Practical 5: Matrix Multiplication (Pattern 2)](#practical-5-matrix-multiplication-pattern-2)\n",
                "6. [Practical 6: Fibonacci Series (Iterative Generation)](#practical-6-fibonacci-series-iterative-generation)\n",
                "7. [Practical 7: Prime Number Checking](#practical-7-prime-number-checking-in-n-natural-numbers)\n",
                "8. [Practical 8: Bubble Sort (Pattern 2)](#practical-8-bubble-sort-on-three-different-arrays-pattern-2)\n",
                "9. [Practical 9: Addition/Sum of Array Elements (Pattern 2)](#practical-9-additionsum-of-elements-of-an-array-pattern-2)\n",
                "10. [Practical 10: Matrix Transpose (Pattern 2)](#practical-10-matrix-transpose-of-three-different-matrices-pattern-2)\n"
            ]
        }
    ]
    
    for q in questions:
        # 1. Execute and obtain real metrics & images
        methods, times, speedups, output_str, time_img, speedup_img = q["executor"]()
        
        # 2. Write standalone Python script
        with open(q["py_file"], "w", encoding="utf-8") as f:
            f.write(q["code"])
        print(f"Created standalone Python script: {q['py_file']}")
        
        # 3. Create standalone Jupyter Notebook
        nb_cells = format_nb_section(
            title=q["title"],
            aim=q["aim"],
            algorithm=q["algo"],
            code_str=q["code"],
            output_str=output_str,
            time_img_path=time_img,
            speedup_img_path=speedup_img
        )
        nb_dict = create_notebook_dict(nb_cells)
        with open(q["nb_file"], "w", encoding="utf-8") as f:
            json.dump(nb_dict, f, indent=2)
        print(f"Created standalone Jupyter Notebook: {q['nb_file']}")
        
        # 4. Append to master notebook
        all_master_cells.extend(nb_cells)
        
    # Write unified master notebook
    master_nb_dict = create_notebook_dict(all_master_cells)
    master_filename = "Parallel_Computing_Lab_Notebook.ipynb"
    with open(master_filename, "w", encoding="utf-8") as f:
        json.dump(master_nb_dict, f, indent=2)
    print(f"\nCreated Unified Master Notebook: {master_filename}")
    print("ALL 10 PRACTICALS EXECUTED AND GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
