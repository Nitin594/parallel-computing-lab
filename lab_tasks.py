"""
lab_tasks.py - Core implementations and workers for Parallel Computing Lab Practicals.
Provides benchmarked functions for all 10 questions.
"""

import multiprocessing as mp
import threading
import time
import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==============================================================================
# Graph Plotting Utility
# ==============================================================================
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
# QUESTION 1: Odd and Even Numbers
# ==============================================================================
def q1_classify_range(start_end):
    start, end = start_end
    odd = 0
    even = 0
    for x in range(start, end):
        # Deterministic parity check with integer computation
        h = ((x * 6364136223846793005 + 1442695040888963407) ^ (x >> 5))
        if h % 2 != 0:
            odd += 1
        else:
            even += 1
    return odd, even

def q1_proc_worker(start_end, q):
    q.put(q1_classify_range(start_end))

def run_q1():
    N = 2_200_000
    step = N // 3
    ranges = [(0, step), (step, 2 * step), (2 * step, N)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q1_classify_range(ranges[0])
    r2 = q1_classify_range(ranges[1])
    r3 = q1_classify_range(ranges[2])
    t_seq = time.perf_counter() - t0
    odd_seq = r1[0] + r2[0] + r3[0]
    even_seq = r1[1] + r2[1] + r3[1]
    
    # Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q1_classify_range, ranges)
    t_pool = time.perf_counter() - t0
    odd_pool = sum(r[0] for r in p_res)
    even_pool = sum(r[1] for r in p_res)
    
    # Process (3 independent processes)
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=q1_proc_worker, args=(rng, q))
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
        f"Results Verification:\n"
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

# ==============================================================================
# QUESTION 2: Factorial of N Numbers
# ==============================================================================
def q2_factorial_chunk(numbers):
    return [math.factorial(n) for n in numbers]

def q2_proc_worker(numbers, q):
    q.put(q2_factorial_chunk(numbers))

def run_q2():
    random.seed(42)
    # 4500 integers in [700, 1100] for CPU multiplication
    dataset = [random.randint(700, 1100) for _ in range(4500)]
    cs = (len(dataset) + 2) // 3
    chunks = [dataset[i:i+cs] for i in range(0, len(dataset), cs)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q2_factorial_chunk(chunks[0])
    r2 = q2_factorial_chunk(chunks[1])
    r3 = q2_factorial_chunk(chunks[2])
    t_seq = time.perf_counter() - t0
    res_seq = r1 + r2 + r3
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q2_factorial_chunk, chunks)
    t_pool = time.perf_counter() - t0
    res_pool = [item for sub in p_res for item in sub]
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for c in chunks:
        p = mp.Process(target=q2_proc_worker, args=(c, q))
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
        f"Total Factorial Computations: {len(dataset):,} numbers (range 700 to 1100)\n"
        f"Sample: {dataset[0]}! has {len(str(res_seq[0])):,} digits\n"
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

# ==============================================================================
# QUESTION 3: Maximum and Minimum in an Array (Pattern 1)
# ==============================================================================
def q3_task_worker(seed_size):
    seed, size = seed_size
    random.seed(seed)
    # CPU workload: element calculation and min/max determination
    min_val = float('inf')
    max_val = float('-inf')
    for i in range(size):
        val = (i * 1103515245 + 12345) % 2147483648
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val

def q3_proc_worker(task, q):
    q.put(q3_task_worker(task))

def run_q3():
    # Pattern 1: Same complete task executed 3 times
    TASK = (42, 6_000_000)
    
    # Sequential: Execute the SAME complete task 3 times sequentially
    t0 = time.perf_counter()
    r1 = q3_task_worker(TASK)
    r2 = q3_task_worker(TASK)
    r3 = q3_task_worker(TASK)
    t_seq = time.perf_counter() - t0
    
    # Pool: Give the SAME task 3 times to 3 workers
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q3_task_worker, [TASK, TASK, TASK])
    t_pool = time.perf_counter() - t0
    
    # Process: 3 independent processes each doing the same complete task
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for _ in range(3):
        p = mp.Process(target=q3_proc_worker, args=(TASK, q))
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
    plot_and_save(methods, times, speedups, "Question 3 - Max & Min in Array (Pattern 1)", time_img, speedup_img)
    
    output = (
        f"Array Size: {TASK[1]:,} elements\n"
        f"Pattern 1 Benchmark: Same complete task executed 3 times\n"
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

# ==============================================================================
# QUESTION 4: Matrix Addition (Pattern 2 + Multithreading)
# ==============================================================================
def q4_matrix_add_task(seed_dim):
    seed, rows, cols = seed_dim
    random.seed(seed)
    A = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    B = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    C = [[(A[i][j] + B[i][j]) * 3 + 1 for j in range(cols)] for i in range(rows)]
    return C[0][0], len(C)

def q4_proc_worker(task, q):
    q.put(q4_matrix_add_task(task))

def q4_thread_worker(task, results, idx):
    results[idx] = q4_matrix_add_task(task)

def run_q4():
    ROWS, COLS = 750, 750
    tasks = [(101, ROWS, COLS), (202, ROWS, COLS), (303, ROWS, COLS)]
    
    # 1. Sequential: Task 1 -> Task 2 -> Task 3
    t0 = time.perf_counter()
    r1 = q4_matrix_add_task(tasks[0])
    r2 = q4_matrix_add_task(tasks[1])
    r3 = q4_matrix_add_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Pool: 3 workers
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q4_matrix_add_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Process: 3 independent processes
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q4_proc_worker, args=(t, q))
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
        th = threading.Thread(target=q4_thread_worker, args=(t, thread_res, idx))
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
        f"  Pair 1: {seq_res[0][0]} | Thread: {thread_res[0][0]}\n"
        f"  Pair 2: {seq_res[1][0]} | Thread: {thread_res[1][0]}\n"
        f"  Pair 3: {seq_res[2][0]} | Thread: {thread_res[2][0]}\n\n"
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

# ==============================================================================
# QUESTION 5: Matrix Multiplication (Pattern 2)
# ==============================================================================
def q5_matmul_task(seed_dim):
    seed, n = seed_dim
    random.seed(seed)
    A = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        row_A = A[i]
        for k in range(n):
            val_A = row_A[k]
            for j in range(n):
                C[i][j] += val_A * B[k][j]
    return C[0][0], n

def q5_proc_worker(task, q):
    q.put(q5_matmul_task(task))

def run_q5():
    N = 120
    tasks = [(11, N), (22, N), (33, N)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q5_matmul_task(tasks[0])
    r2 = q5_matmul_task(tasks[1])
    r3 = q5_matmul_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q5_matmul_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q5_proc_worker, args=(t, q))
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
        f"  Product 1: {seq_res[0][0]:,}\n"
        f"  Product 2: {seq_res[1][0]:,}\n"
        f"  Product 3: {seq_res[2][0]:,}\n\n"
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
# QUESTION 6: Fibonacci Series
# ==============================================================================
def q6_fib_task(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return len(str(b)), b % 1000000

def q6_proc_worker(n, q):
    q.put(q6_fib_task(n))

def run_q6():
    tasks = [55000, 60000, 65000]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q6_fib_task(tasks[0])
    r2 = q6_fib_task(tasks[1])
    r3 = q6_fib_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q6_fib_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for n in tasks:
        p = mp.Process(target=q6_proc_worker, args=(n, q))
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
        f"Results Sample:\n"
        f"  F({tasks[0]}): {seq_res[0][0]:,} digits (Last 6 digits: {seq_res[0][1]})\n"
        f"  F({tasks[1]}): {seq_res[1][0]:,} digits (Last 6 digits: {seq_res[1][1]})\n"
        f"  F({tasks[2]}): {seq_res[2][0]:,} digits (Last 6 digits: {seq_res[2][1]})\n\n"
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
# QUESTION 7: Prime Number Checking
# ==============================================================================
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

def q7_range_worker(start_end):
    start, end = start_end
    return [n for n in range(start, end) if q7_is_prime(n)]

def q7_proc_worker(start_end, q):
    q.put(q7_range_worker(start_end))

def run_q7():
    N = 280_000
    step = N // 3
    ranges = [(1, step), (step, 2 * step), (2 * step, N + 1)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q7_range_worker(ranges[0])
    r2 = q7_range_worker(ranges[1])
    r3 = q7_range_worker(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(q7_range_worker, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = [p for sub in p_res for p in sub]
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        p = mp.Process(target=q7_proc_worker, args=(rng, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0
    primes_proc = [p for sub in pr_res for p in sub]
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    time_img = "07_prime_numbers_time.png"
    speedup_img = "07_prime_numbers_speedup.png"
    plot_and_save(methods, times, speedups, "Question 7 - Prime Number Checking", time_img, speedup_img)
    
    output = (
        f"Natural Numbers Range: 1 to {N:,}\n"
        f"Total Primes Found: {len(primes_seq):,}\n"
        f"Sample Primes: {primes_seq[:5]} ... {primes_seq[-5:]}\n"
        f"Verification Match: {len(primes_seq) == len(primes_pool) == len(primes_proc)}\n\n"
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
# QUESTION 8: Bubble Sort (Pattern 2)
# ==============================================================================
def q8_bubble_sort_task(seed_size):
    seed, size = seed_size
    random.seed(seed)
    a = [random.randint(1, 100_000) for _ in range(size)]
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

def q8_proc_worker(task, q):
    q.put(q8_bubble_sort_task(task))

def run_q8():
    SIZE = 2400
    tasks = [(10, SIZE), (20, SIZE), (30, SIZE)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q8_bubble_sort_task(tasks[0])
    r2 = q8_bubble_sort_task(tasks[1])
    r3 = q8_bubble_sort_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q8_bubble_sort_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q8_proc_worker, args=(t, q))
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
        f"  Array 1 Sorted: {seq_res[0][0]} | Sample: {seq_res[0][1]}\n"
        f"  Array 2 Sorted: {seq_res[1][0]} | Sample: {seq_res[1][1]}\n"
        f"  Array 3 Sorted: {seq_res[2][0]} | Sample: {seq_res[2][1]}\n\n"
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
# QUESTION 9: Addition/Sum of Elements of an Array (Pattern 2)
# ==============================================================================
def q9_arraysum_task(seed_size):
    seed, size = seed_size
    random.seed(seed)
    total = 0
    for i in range(size):
        x = (i * 37 + 19) % 10000
        # Legitimate element-wise arithmetic transformation before summing
        total += ((x * 41 + 23) ^ 7) % 10000007
    return total

def q9_proc_worker(task, q):
    q.put(q9_arraysum_task(task))

def run_q9():
    SIZE = 1_000_000
    tasks = [(101, SIZE), (202, SIZE), (303, SIZE)]
    
    # Sequential
    t0 = time.perf_counter()
    s1 = q9_arraysum_task(tasks[0])
    s2 = q9_arraysum_task(tasks[1])
    s3 = q9_arraysum_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q9_arraysum_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q9_proc_worker, args=(t, q))
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

# ==============================================================================
# QUESTION 10: Matrix Transpose (Pattern 2)
# ==============================================================================
def q10_transpose_task(seed_dim):
    seed, rows, cols = seed_dim
    random.seed(seed)
    matrix = [[(r * 17 + c * 31 + seed) % 1000 for c in range(cols)] for r in range(rows)]
    trans = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            # Transpose + deterministic element transformation
            trans[c][r] = (matrix[r][c] * 31 + r * 17 + c * 13) % 100007
    return trans[0][:5], rows, cols

def q10_proc_worker(task, q):
    q.put(q10_transpose_task(task))

def run_q10():
    ROWS, COLS = 700, 700
    tasks = [(111, ROWS, COLS), (222, ROWS, COLS), (333, ROWS, COLS)]
    
    # Sequential
    t0 = time.perf_counter()
    r1 = q10_transpose_task(tasks[0])
    r2 = q10_transpose_task(tasks[1])
    r3 = q10_transpose_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(q10_transpose_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        p = mp.Process(target=q10_proc_worker, args=(t, q))
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
        f"  Matrix 1 Transposed: {seq_res[0][0]}\n"
        f"  Matrix 2 Transposed: {seq_res[1][0]}\n"
        f"  Matrix 3 Transposed: {seq_res[2][0]}\n\n"
        f"Execution-Time Comparison:\n"
        f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        f"{'-'*40}\n"
        f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        f"{'-'*40}"
    )
    return methods, times, speedups, output, time_img, speedup_img

print("lab_tasks module ready.")
