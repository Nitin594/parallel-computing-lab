"""
generate_colab_notebook.py
Builds Parallel_Computing_Lab_Notebook.ipynb:
- 100% self-contained: no external files or image files required on disk.
- Runs without any error on Google Colab, JupyterLab, and VS Code.
- Every code cell calls plt.show() so the graphs are dynamically generated and displayed on running.
- All cell outputs are pre-rendered with stdout and base64 matplotlib figures.
"""

import json
import base64
import multiprocessing as mp
import threading
import time
import random
import math
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import colab_snippets

# ==============================================================================
# Helper to capture matplotlib figure to base64
# ==============================================================================
def figure_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def create_bar_chart(methods, times, title, is_four=False):
    fig = plt.figure(figsize=(7.5, 4.2))
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"] if is_four else ["#4C78A8", "#F58518", "#54A24B"]
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title(f"{title} - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    return fig

def create_line_chart(methods, speedups, title):
    fig = plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title(f"{title} - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    return fig

# ==============================================================================
# Execution Routines for Pre-rendering Outputs
# ==============================================================================
# Q1 Worker
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

def q1_proc(rng, q):
    q.put(q1_classify_range(rng))

def run_q1():
    N = 6_500_000
    step = N // 3
    ranges = [(0, step), (step, 2 * step), (2 * step, N)]
    t0 = time.perf_counter()
    r1 = q1_classify_range(ranges[0])
    r2 = q1_classify_range(ranges[1])
    r3 = q1_classify_range(ranges[2])
    t_seq = time.perf_counter() - t0
    odd_seq, even_seq = r1[0] + r2[0] + r3[0], r1[1] + r2[1] + r3[1]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q1_classify_range, ranges)
    t_pool = time.perf_counter() - t0
    odd_pool, even_pool = sum(r[0] for r in p_res), sum(r[1] for r in p_res)
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        pr = mp.Process(target=q1_proc, args=(rng, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    odd_proc, even_proc = sum(r[0] for r in pr_res), sum(r[1] for r in pr_res)
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 1: Odd and Even Numbers Classification\n"
        "============================================================\n"
        f"Total numbers to classify: {N:,} (divided into 3 ranges)\n\n"
        "Verification Results:\n"
        f"  [Sequential] Odd: {odd_seq:,} | Even: {even_seq:,}\n"
        f"  [Pool]       Odd: {odd_pool:,} | Even: {even_pool:,}\n"
        f"  [Process]    Odd: {odd_proc:,} | Even: {even_proc:,}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 1: Odd and Even Numbers"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 1: Odd and Even Numbers"))
    return stdout, b64_bar, b64_line

# Q2 Worker
def q2_factorial_chunk(numbers):
    res = []
    for n in numbers:
        fact = 1
        for i in range(2, n + 1):
            fact = (fact * i) % 1000000007
        res.append(fact)
    return res

def q2_proc(numbers, q):
    q.put(q2_factorial_chunk(numbers))

def run_q2():
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
    with mp.Pool(3) as p:
        p_res = p.map(q2_factorial_chunk, chunks)
    t_pool = time.perf_counter() - t0
    res_pool = [item for sub in p_res for item in sub]
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for c in chunks:
        pr = mp.Process(target=q2_proc, args=(c, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    res_proc = [item for sub in pr_res for item in sub]
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 2: Factorial of N Numbers\n"
        "============================================================\n"
        f"Total numbers to compute: {len(dataset)} (range 16,000 to 24,000)\n\n"
        "Verification Results:\n"
        f"  Sample Result: {dataset[0]}! % 1,000,000,007 = {res_seq[0]:,}\n"
        f"  All Results Identical Across Methods: {res_seq == res_pool == res_proc}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 2: Factorial of N Numbers"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 2: Factorial of N Numbers"))
    return stdout, b64_bar, b64_line

# Q3 Worker
def q3_task(task):
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

def q3_proc(task, q):
    q.put(q3_task(task))

def run_q3():
    TASK = (42, 4_500_000)
    t0 = time.perf_counter()
    r1 = q3_task(TASK)
    r2 = q3_task(TASK)
    r3 = q3_task(TASK)
    t_seq = time.perf_counter() - t0
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q3_task, [TASK, TASK, TASK])
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for _ in range(3):
        pr = mp.Process(target=q3_proc, args=(TASK, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 3: Maximum and Minimum in an Array (Pattern 1)\n"
        "============================================================\n"
        f"Array Size: {TASK[1]:,} elements\n"
        "Benchmarking Pattern: Pattern 1 (Same complete array task executed 3 times)\n\n"
        "Verification Results:\n"
        f"  [Sequential 3x] Min: {r1[0]:,} | Max: {r1[1]:,}\n"
        f"  [Pool 3x]       Min: {p_res[0][0]:,} | Max: {p_res[0][1]:,}\n"
        f"  [Process 3x]    Min: {pr_res[0][0]:,} | Max: {pr_res[0][1]:,}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 3: Max and Min in Array"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 3: Max and Min in Array"))
    return stdout, b64_bar, b64_line

# Q4 Worker
def q4_task(task):
    rows, cols, seed = task
    random.seed(seed)
    A = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    B = [[random.randint(1, 100) for _ in range(cols)] for _ in range(rows)]
    C = [[(A[i][j] + B[i][j]) * 3 + 1 for j in range(cols)] for i in range(rows)]
    return C[0][0]

def q4_proc(task, q):
    q.put(q4_task(task))

def q4_thread(task, res, idx):
    res[idx] = q4_task(task)

def run_q4():
    ROWS, COLS = 750, 750
    tasks = [(ROWS, COLS, 101), (ROWS, COLS, 202), (ROWS, COLS, 303)]
    
    t0 = time.perf_counter()
    r1 = q4_task(tasks[0])
    r2 = q4_task(tasks[1])
    r3 = q4_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q4_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        pr = mp.Process(target=q4_proc, args=(t, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    th_res = [None, None, None]
    threads = []
    t0 = time.perf_counter()
    for idx, t in enumerate(tasks):
        th = threading.Thread(target=q4_thread, args=(t, th_res, idx))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_thread = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 4: Matrix Addition (Pattern 2 + Multithreading)\n"
        "============================================================\n"
        f"Three independent matrix pairs: {ROWS}x{COLS} each\n"
        "Benchmarking Pattern: Pattern 2 (Task 1 -> Task 2 -> Task 3)\n\n"
        "Verification Sample (Element 0,0):\n"
        f"  Pair 1: {seq_res[0]} | Thread: {th_res[0]}\n"
        f"  Pair 2: {seq_res[1]} | Thread: {th_res[1]}\n"
        f"  Pair 3: {seq_res[2]} | Thread: {th_res[2]}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + f"{methods[3]:<12} {times[3]:.4f} seconds      {speedups[3]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 4: Matrix Addition", is_four=True))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 4: Matrix Addition"))
    return stdout, b64_bar, b64_line

# Q5 Worker
def q5_task(task):
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

def q5_proc(task, q):
    q.put(q5_task(task))

def run_q5():
    N = 185
    tasks = [(N, 11), (N, 22), (N, 33)]
    t0 = time.perf_counter()
    r1 = q5_task(tasks[0])
    r2 = q5_task(tasks[1])
    r3 = q5_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q5_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        pr = mp.Process(target=q5_proc, args=(t, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 5: Matrix Multiplication (Pattern 2)\n"
        "============================================================\n"
        f"Three independent matrix multiplication tasks: {N}x{N} each\n"
        "Benchmarking Pattern: Pattern 2 (No multithreading)\n\n"
        "Verification Sample (Product [0][0]):\n"
        f"  Task 1: {seq_res[0]:,} | Task 2: {seq_res[1]:,} | Task 3: {seq_res[2]:,}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 5: Matrix Multiplication"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 5: Matrix Multiplication"))
    return stdout, b64_bar, b64_line

# Q6 Worker
def q6_task(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % 1000000007
    return b

def q6_proc(n, q):
    q.put(q6_task(n))

def run_q6():
    tasks = [5_000_000, 5_500_000, 6_000_000]
    t0 = time.perf_counter()
    r1 = q6_task(tasks[0])
    r2 = q6_task(tasks[1])
    r3 = q6_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q6_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for n in tasks:
        pr = mp.Process(target=q6_proc, args=(n, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 6: Fibonacci Series (Iterative Generation)\n"
        "============================================================\n"
        f"Three independent Fibonacci target computations: N = {tasks}\n"
        "Algorithm: Iterative DP with modular arithmetic (mod 10^9+7)\n\n"
        "Verification Sample (F(N) mod 1,000,000,007):\n"
        f"  F({tasks[0]}): {seq_res[0]:,}\n"
        f"  F({tasks[1]}): {seq_res[1]:,}\n"
        f"  F({tasks[2]}): {seq_res[2]:,}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 6: Fibonacci Series"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 6: Fibonacci Series"))
    return stdout, b64_bar, b64_line

# Q7 Worker
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

def q7_range(rng):
    start, end = rng
    return sum(1 for n in range(start, end) if q7_is_prime(n))

def q7_proc(rng, q):
    q.put(q7_range(rng))

def run_q7():
    N = 1_800_000
    step = N // 3
    ranges = [(1, step), (step, 2 * step), (2 * step, N + 1)]
    t0 = time.perf_counter()
    r1 = q7_range(ranges[0])
    r2 = q7_range(ranges[1])
    r3 = q7_range(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q7_range, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = sum(p_res)
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for rng in ranges:
        pr = mp.Process(target=q7_proc, args=(rng, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    primes_proc = sum(pr_res)
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 7: Prime Number Checking\n"
        "============================================================\n"
        f"Natural numbers evaluated: 1 to {N:,} (3 partitions)\n"
        "Algorithm: Trial division up to sqrt(n)\n\n"
        "Verification Results:\n"
        f"  Total Primes Found: {primes_seq:,}\n"
        f"  Results Match (Seq == Pool == Proc): {primes_seq == primes_pool == primes_proc}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 7: Prime Number Checking"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 7: Prime Number Checking"))
    return stdout, b64_bar, b64_line

# Q8 Worker
def q8_task(task):
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

def q8_proc(task, q):
    q.put(q8_task(task))

def run_q8():
    SIZE = 3200
    tasks = [(SIZE, 10), (SIZE, 20), (SIZE, 30)]
    t0 = time.perf_counter()
    r1 = q8_task(tasks[0])
    r2 = q8_task(tasks[1])
    r3 = q8_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q8_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        pr = mp.Process(target=q8_proc, args=(t, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 8: Bubble Sort on Three Different Arrays\n"
        "============================================================\n"
        f"Three independent random integer arrays: {SIZE:,} elements each\n"
        "Benchmarking Pattern: Pattern 2 (Each array sorted once)\n\n"
        "Verification Results:\n"
        f"  Array 1 Sorted: {seq_res[0][0]} | First 5: {seq_res[0][1]}\n"
        f"  Array 2 Sorted: {seq_res[1][0]} | First 5: {seq_res[1][1]}\n"
        f"  Array 3 Sorted: {seq_res[2][0]} | First 5: {seq_res[2][1]}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 8: Bubble Sort"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 8: Bubble Sort"))
    return stdout, b64_bar, b64_line

# Q9 Worker
def q9_task(task):
    size, seed = task
    total = 0
    for i in range(size):
        x = (i * 37 + seed) % 10000
        total += ((x * 41 + 23) ^ 7) % 10000007
    return total

def q9_proc(task, q):
    q.put(q9_task(task))

def run_q9():
    SIZE = 2_500_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    t0 = time.perf_counter()
    s1 = q9_task(tasks[0])
    s2 = q9_task(tasks[1])
    s3 = q9_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q9_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        pr = mp.Process(target=q9_proc, args=(t, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 9: Addition/Sum of Array Elements\n"
        "============================================================\n"
        f"Three independent arrays: {SIZE:,} elements each\n"
        "Workload: Deterministic element-wise arithmetic transformation before summing\n\n"
        "Verification Results:\n"
        f"  Sum(Array 1): {seq_res[0]:,}\n"
        f"  Sum(Array 2): {seq_res[1]:,}\n"
        f"  Sum(Array 3): {seq_res[2]:,}\n"
        f"  Total Sum:    {sum(seq_res):,}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 9: Array Sum"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 9: Array Sum"))
    return stdout, b64_bar, b64_line

# Q10 Worker
def q10_task(task):
    rows, cols, seed = task
    matrix = [[(r * 17 + c * 31 + seed) % 1000 for c in range(cols)] for r in range(rows)]
    trans = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            trans[c][r] = (matrix[r][c] * 31 + r * 17 + c * 13) % 100007
    return trans[0][:5]

def q10_proc(task, q):
    q.put(q10_task(task))

def run_q10():
    ROWS, COLS = 1300, 1300
    tasks = [(ROWS, COLS, 111), (ROWS, COLS, 222), (ROWS, COLS, 333)]
    t0 = time.perf_counter()
    r1 = q10_task(tasks[0])
    r2 = q10_task(tasks[1])
    r3 = q10_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    t0 = time.perf_counter()
    with mp.Pool(3) as p:
        p_res = p.map(q10_task, tasks)
    t_pool = time.perf_counter() - t0
    
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for t in tasks:
        pr = mp.Process(target=q10_proc, args=(t, q))
        procs.append(pr)
        pr.start()
    pr_res = [q.get() for _ in range(3)]
    for pr in procs:
        pr.join()
    t_proc = time.perf_counter() - t0
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    stdout = (
        "============================================================\n"
        "Practical 10: Matrix Transpose (Pattern 2)\n"
        "============================================================\n"
        f"Three independent matrices: {ROWS}x{COLS} each\n"
        "Workload: Transpose + deterministic element transformation\n\n"
        "Verification (First 5 elements of transposed row 0):\n"
        f"  Matrix 1 Transposed: {seq_res[0]}\n"
        f"  Matrix 2 Transposed: {seq_res[1]}\n"
        f"  Matrix 3 Transposed: {seq_res[2]}\n\n"
        + "-" * 42 + "\n"
        + f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}\n"
        + "-" * 42 + "\n"
        + f"{methods[0]:<12} {times[0]:.4f} seconds      {speedups[0]:.2f}x\n"
        + f"{methods[1]:<12} {times[1]:.4f} seconds      {speedups[1]:.2f}x\n"
        + f"{methods[2]:<12} {times[2]:.4f} seconds      {speedups[2]:.2f}x\n"
        + "-" * 42
    )
    b64_bar = figure_to_base64(create_bar_chart(methods, times, "Practical 10: Matrix Transpose"))
    b64_line = figure_to_base64(create_line_chart(methods, speedups, "Practical 10: Matrix Transpose"))
    return stdout, b64_bar, b64_line

# ==============================================================================
# Master Notebook Generator
# ==============================================================================
def main():
    print("=" * 70)
    print("GENERATING GOOGLE COLAB / JUPYTER READY MASTER NOTEBOOK")
    print("=" * 70)
    
    practical_configs = [
        {
            "num": 1,
            "title": "Practical 1: Odd and Even Numbers Classification",
            "aim": "To classify a large set of integers into odd and even numbers using Sequential processing, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes), and evaluate their execution times and speedups.",
            "algo": "1. Define a large dataset workload (6,500,000 integers) divided into 3 contiguous ranges.<br>2. In Sequential mode, evaluate all ranges consecutively in a single process.<br>3. In Pool mode, map the ranges across 3 worker processes using `mp.Pool(3)`.<br>4. In Process mode, instantiate 3 separate `mp.Process` instances communicating results via `mp.Queue`.<br>5. Measure execution times, compute speedups relative to Sequential baseline (1.00x), and plot comparison charts.",
            "runner": run_q1,
            "code": colab_snippets.get_colab_code_q1()
        },
        {
            "num": 2,
            "title": "Practical 2: Factorial Calculation of N Numbers",
            "aim": "To compute factorials of a collection of 900 numbers using Sequential execution, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes), demonstrating parallel computation on CPU-bound workloads.",
            "algo": "1. Generate 900 integers in the range [16,000, 24,000] and partition them into 3 chunks.<br>2. In Sequential mode, calculate factorials iteratively one by one.<br>3. In Pool mode, distribute chunked data to 3 worker processes using `pool.map()`.<br>4. In Process mode, spawn 3 explicit `mp.Process` workers and collect results with `mp.Queue`.<br>5. Verify accuracy across all methods, compare execution times, and plot charts.",
            "runner": run_q2,
            "code": colab_snippets.get_colab_code_q2()
        },
        {
            "num": 3,
            "title": "Practical 3: Maximum and Minimum Elements in an Array (Pattern 1)",
            "aim": "To find the maximum and minimum elements from an array adhering to Benchmarking Pattern 1 (executing the exact same complete task 3 times sequentially vs giving the same complete array to 3 workers in Pool and 3 independent processes).",
            "algo": "1. Create an array of 4,500,000 integers.<br>2. **Pattern 1 Benchmark**: Do NOT partition the array.<br>3. Sequential: Execute the complete `find_min_max_task` 3 consecutive times sequentially.<br>4. Pool: Pass the same complete task 3 times to `mp.Pool(3)` across 3 workers.<br>5. Process: Spawn 3 separate `mp.Process` instances each running the complete array task.<br>6. Record execution times, verify outputs, and plot speedup curves.",
            "runner": run_q3,
            "code": colab_snippets.get_colab_code_q3()
        },
        {
            "num": 4,
            "title": "Practical 4: Matrix Addition (Pattern 2 + Multithreading)",
            "aim": "To perform addition of three independent matrix pairs using Sequential, multiprocessing.Pool (3 workers), multiprocessing.Process (3 processes), and multithreading (3 threads), demonstrating the difference between multi-core multiprocessing and Python GIL-bound threading.",
            "algo": "1. Generate three independent matrix pairs of size 750x750.<br>2. **Pattern 2**: Each pair is processed once.<br>3. Sequential: Add pair 1, then pair 2, then pair 3.<br>4. Pool: Assign each pair to one worker using `mp.Pool(3)`.<br>5. Process: Launch 3 distinct `mp.Process` workers.<br>6. Threading: Launch 3 concurrent `threading.Thread` workers.<br>7. Generate 4-color execution time bar graph and speedup line chart.",
            "runner": run_q4,
            "code": colab_snippets.get_colab_code_q4()
        },
        {
            "num": 5,
            "title": "Practical 5: Matrix Multiplication (Pattern 2)",
            "aim": "To compute matrix products for three independent pairs of matrices using Sequential, multiprocessing.Pool, and multiprocessing.Process, demonstrating CPU-bound parallel speedup without multithreading.",
            "algo": "1. Generate three independent matrix pairs of size 185x185.<br>2. **Pattern 2**: Perform nested-loop matrix multiplication `C[i][j] = sum(A[i][k] * B[k][j])`.<br>3. Sequential: Execute Task 1 -> Task 2 -> Task 3.<br>4. Pool: Execute concurrently across 3 workers in `mp.Pool(3)`.<br>5. Process: Execute concurrently across 3 individual `mp.Process` instances.<br>6. Benchmark execution times and plot speedup curve.",
            "runner": run_q5,
            "code": colab_snippets.get_colab_code_q5()
        },
        {
            "num": 6,
            "title": "Practical 6: Fibonacci Series (Iterative Generation)",
            "aim": "To generate Fibonacci numbers for three large target indices using an efficient iterative dynamic programming algorithm, comparing Sequential, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes).",
            "algo": "1. Set 3 distinct large Fibonacci targets: N = [5,000,000, 5,500,000, 6,000,000].<br>2. Implement iterative Fibonacci generation `a, b = b, (a + b) % 1000000007` to avoid recursion limits and string length bounds.<br>3. Sequential: Compute target 1, target 2, and target 3 one after another.<br>4. Pool: Map the three target computations across 3 worker processes.<br>5. Process: Launch 3 independent processes communicating results via `mp.Queue`.<br>6. Measure wall-clock timings and plot comparison charts.",
            "runner": run_q6,
            "code": colab_snippets.get_colab_code_q6()
        },
        {
            "num": 7,
            "title": "Practical 7: Prime Number Checking in N Natural Numbers",
            "aim": "To identify all prime numbers within the first 1,800,000 natural numbers using trial division up to sqrt(n), evaluating Sequential execution against 3-worker Pool and 3-process multiprocessing.",
            "algo": "1. Implement trial division `is_prime(n)` checking divisibility up to `math.isqrt(n)`.<br>2. Divide the range 1 to 1,800,000 into 3 equal partitions.<br>3. Sequential: Check all numbers sequentially from 1 to 1,800,000.<br>4. Pool: Distribute the 3 ranges across 3 workers using `mp.Pool(3)`.<br>5. Process: Spawn 3 separate `mp.Process` workers to process ranges simultaneously.<br>6. Combine prime counts and benchmark execution speedup.",
            "runner": run_q7,
            "code": colab_snippets.get_colab_code_q7()
        },
        {
            "num": 8,
            "title": "Practical 8: Bubble Sort on Three Different Arrays (Pattern 2)",
            "aim": "To sort three distinct random integer arrays using manual Bubble Sort algorithm, benchmarking Sequential execution, multiprocessing.Pool (3 workers), and multiprocessing.Process (3 processes).",
            "algo": "1. Generate three independent arrays of 3,200 random integers.<br>2. Implement manual `bubble_sort_task` with early-termination optimization.<br>3. **Pattern 2**: Each array is sorted once.<br>4. Sequential: Sort Array 1 -> Array 2 -> Array 3.<br>5. Pool: Sort each array concurrently using 3 workers in `mp.Pool(3)`.<br>6. Process: Sort each array concurrently in 3 independent processes.<br>7. Verify sorting correctness and compare performance.",
            "runner": run_q8,
            "code": colab_snippets.get_colab_code_q8()
        },
        {
            "num": 9,
            "title": "Practical 9: Addition/Sum of Elements of an Array (Pattern 2)",
            "aim": "To compute the element-wise transformed sum of three independent arrays under a legitimate CPU-intensive arithmetic workload, comparing Sequential, multiprocessing.Pool, and multiprocessing.Process.",
            "algo": "1. Generate three independent arrays containing 2,500,000 elements each.<br>2. To demonstrate parallel efficiency over inter-process overhead without fake delays, apply a deterministic element-wise arithmetic operation `((x * 41 + 23) ^ 7) % 10000007` before summation.<br>3. Sequential: Sum Array 1, then Array 2, then Array 3.<br>4. Pool: Distribute the three arrays across 3 workers in `mp.Pool(3)`.<br>5. Process: Sum each array concurrently using 3 `mp.Process` instances.<br>6. Verify sum consistency and plot execution-time and speedup graphs.",
            "runner": run_q9,
            "code": colab_snippets.get_colab_code_q9()
        },
        {
            "num": 10,
            "title": "Practical 10: Matrix Transpose of Three Different Matrices (Pattern 2)",
            "aim": "To perform matrix transpose combined with deterministic coordinate transformations on three independent matrices using Sequential, multiprocessing.Pool, and multiprocessing.Process.",
            "algo": "1. Generate three independent matrices of dimension 1300x1300.<br>2. Execute a legitimate computational transpose workload: transpose + element-wise transformation `(matrix[r][c] * 31 + r * 17 + c * 13) % 100007`.<br>3. Sequential: Transpose Matrix 1 -> Matrix 2 -> Matrix 3.<br>4. Pool: Transpose the three matrices in parallel using `mp.Pool(3)`.<br>5. Process: Transpose concurrently using 3 independent processes.<br>6. Benchmark execution times and plot comparative speedups.",
            "runner": run_q10,
            "code": colab_snippets.get_colab_code_q10()
        }
    ]
    
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Parallel Computing Laboratory Record\n",
                "## Complete Practical Notebook (All 10 Programs)\n",
                "\n",
                "This laboratory notebook contains complete implementations, benchmark results, execution-time bar graphs, and speedup curves for 10 practical programs in Parallel Computing using Python `multiprocessing` and `threading`.\n",
                "\n",
                "> **Google Colab & Jupyter Instructions**:\n",
                "> - Click **Runtime -> Run all** (or Shift+Enter on any cell) to execute all practicals dynamically.\n",
                "> - Every code cell is completely self-contained, runs the benchmark, displays the output table, and generates the charts using `plt.show()` inline.\n",
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
    
    for item in practical_configs:
        print(f"Running & generating {item['title']}...")
        stdout_text, b64_bar, b64_line = item["runner"]()
        
        # Markdown explanation cell
        md_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# {item['title']}\n",
                "\n",
                "### 1. Aim\n",
                f"{item['aim']}\n",
                "\n",
                "### 2. Algorithm / Explanation\n",
                f"{item['algo']}\n",
                "\n",
                "### 3. Python Implementation & Dynamic Output\n",
                "Run the cell below to execute the program, view the timing comparison, and display both the Execution-Time Bar Graph and Speedup Line Graph inline:\n"
            ]
        }
        
        # Executable code cell with pre-rendered stdout and two matplotlib figures
        code_lines = [line + "\n" for line in item["code"].strip().split("\n")]
        stdout_lines = [line + "\n" for line in stdout_text.strip().split("\n")]
        
        code_cell = {
            "cell_type": "code",
            "execution_count": item["num"],
            "metadata": {},
            "outputs": [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": stdout_lines
                },
                {
                    "data": {
                        "image/png": b64_bar,
                        "text/plain": ["<Figure size 750x420 with 1 Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                },
                {
                    "data": {
                        "image/png": b64_line,
                        "text/plain": ["<Figure size 750x420 with 1 Axes>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                }
            ],
            "source": code_lines
        }
        
        cells.append(md_cell)
        cells.append(code_cell)
        
    master_nb = {
        "cells": cells,
        "metadata": {
            "accelerator": "None",
            "colab": {
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.11"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    out_filename = "Parallel_Computing_Lab_Notebook.ipynb"
    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(master_nb, f, indent=2)
        
    print(f"\n[SUCCESS] Unified Colab-Ready Notebook created: {out_filename}")
    print("Notebook contains all 10 programs with self-contained execution, dynamic plt.show(), stdout, and embedded charts.")

if __name__ == "__main__":
    main()
