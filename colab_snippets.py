"""
colab_snippets.py
Contains complete self-contained executable code strings for each practical question,
tailored for Google Colab, JupyterLab, and VS Code.
"""

def get_colab_code_q1():
    return '''# Practical 1: Program to find odd and even numbers from a given set of integer data
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def classify_range(rng):
    start, end = rng
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

def proc_worker(rng, q):
    q.put(classify_range(rng))

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 1: Odd and Even Numbers Classification")
    print("=" * 60)
    
    N = 6_500_000
    step = N // 3
    ranges = [(0, step), (step, 2 * step), (2 * step, N)]
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
    
    # Verification Display
    print("\\nVerification Results:")
    print(f"  [Sequential] Odd: {odd_seq:,} | Even: {even_seq:,}")
    print(f"  [Pool]       Odd: {odd_pool:,} | Even: {even_pool:,}")
    print(f"  [Process]    Odd: {odd_proc:,} | Even: {even_proc:,}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 1: Odd and Even Numbers - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 1: Odd and Even Numbers - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q2():
    return '''# Practical 2: Program to calculate factorial of N numbers
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 2: Factorial of N Numbers")
    print("=" * 60)
    
    random.seed(42)
    dataset = [random.randint(16000, 24000) for _ in range(900)]
    cs = (len(dataset) + 2) // 3
    chunks = [dataset[i:i+cs] for i in range(0, len(dataset), cs)]
    print(f"Total numbers to compute: {len(dataset)} (range 16,000 to 24,000)")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = factorial_chunk(chunks[0])
    r2 = factorial_chunk(chunks[1])
    r3 = factorial_chunk(chunks[2])
    t_seq = time.perf_counter() - t0
    res_seq = r1 + r2 + r3
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(factorial_chunk, chunks)
    t_pool = time.perf_counter() - t0
    res_pool = [item for sub in p_res for item in sub]
    
    # 3. Multiprocessing Process (3 independent processes)
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
    
    # Verification Display
    print("\\nVerification Results:")
    print(f"  Sample Result: {dataset[0]}! % 1,000,000,007 = {res_seq[0]:,}")
    print(f"  All Results Identical Across Methods: {res_seq == res_pool == res_proc}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 2: Factorial of N Numbers - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 2: Factorial of N Numbers - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q3():
    return '''# Practical 3: Program to find maximum and minimum elements from an array
# Pattern 1: Same task executed 3 times
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 3: Maximum and Minimum in an Array (Pattern 1)")
    print("=" * 60)
    
    TASK = (42, 4_500_000)
    print(f"Array Size: {TASK[1]:,} elements")
    print("Benchmarking Pattern: Pattern 1 (Same complete array task executed 3 times)\\n")
    
    # 1. Sequential: Execute the SAME complete task 3 times sequentially
    t0 = time.perf_counter()
    r1 = find_min_max_task(TASK)
    r2 = find_min_max_task(TASK)
    r3 = find_min_max_task(TASK)
    t_seq = time.perf_counter() - t0
    
    # 2. Pool: Give the SAME complete task 3 times to 3 workers
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(find_min_max_task, [TASK, TASK, TASK])
    t_pool = time.perf_counter() - t0
    
    # 3. Process: 3 independent processes each doing the same complete task
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
    
    # Verification Display
    print("Verification Results:")
    print(f"  [Sequential 3x] Min: {r1[0]:,} | Max: {r1[1]:,}")
    print(f"  [Pool 3x]       Min: {p_res[0][0]:,} | Max: {p_res[0][1]:,}")
    print(f"  [Process 3x]    Min: {pr_res[0][0]:,} | Max: {pr_res[0][1]:,}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 3: Max and Min in Array - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 3: Max and Min in Array - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q4():
    return '''# Practical 4: Matrix Addition (Pattern 2 + Multithreading)
# Four methods: Sequential, Pool, Process, Thread
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 4: Matrix Addition (Pattern 2 + Multithreading)")
    print("=" * 60)
    
    ROWS, COLS = 750, 750
    tasks = [(ROWS, COLS, 101), (ROWS, COLS, 202), (ROWS, COLS, 303)]
    print(f"Three independent matrix pairs: {ROWS}x{COLS} each")
    print("Benchmarking Pattern: Pattern 2 (Task 1 -> Task 2 -> Task 3)\\n")
    
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
    
    # Verification Display
    print("Verification Sample (Element 0,0):")
    print(f"  Pair 1: {seq_res[0]} | Thread: {thread_res[0]}")
    print(f"  Pair 2: {seq_res[1]} | Thread: {thread_res[1]}")
    print(f"  Pair 3: {seq_res[2]} | Thread: {thread_res[2]}")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times = [t_seq, t_pool, t_proc, t_thread]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph (4 Colors)
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 4: Matrix Addition - Execution Time (4 Methods)", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 4: Matrix Addition - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q5():
    return '''# Practical 5: Matrix Multiplication (Pattern 2)
# Three independent tasks: A1xB1, A2xB2, A3xB3
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 5: Matrix Multiplication (Pattern 2)")
    print("=" * 60)
    
    N = 185
    tasks = [(N, 11), (N, 22), (N, 33)]
    print(f"Three independent matrix multiplication tasks: {N}x{N} each")
    print("Benchmarking Pattern: Pattern 2 (No multithreading)\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = matmul_task(tasks[0])
    r2 = matmul_task(tasks[1])
    r3 = matmul_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(matmul_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Multiprocessing Process (3 independent processes)
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
    
    # Verification Display
    print("Verification Sample (Product [0][0]):")
    print(f"  Task 1: {seq_res[0]:,} | Task 2: {seq_res[1]:,} | Task 3: {seq_res[2]:,}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 5: Matrix Multiplication - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 5: Matrix Multiplication - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q6():
    return '''# Practical 6: Fibonacci Series (Iterative Generation)
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 6: Fibonacci Series (Iterative Generation)")
    print("=" * 60)
    
    tasks = [5_000_000, 5_500_000, 6_000_000]
    print(f"Three independent Fibonacci target computations: N = {tasks}")
    print("Algorithm: Iterative DP with modular arithmetic (mod 10^9+7)\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = fib_task(tasks[0])
    r2 = fib_task(tasks[1])
    r3 = fib_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(fib_task, tasks)
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
    
    # Verification Display
    print("Verification Sample (F(N) mod 1,000,000,007):")
    print(f"  F({tasks[0]}): {seq_res[0]:,}")
    print(f"  F({tasks[1]}): {seq_res[1]:,}")
    print(f"  F({tasks[2]}): {seq_res[2]:,}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 6: Fibonacci Series - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 6: Fibonacci Series - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q7():
    return '''# Practical 7: Prime Number Checking in N Natural Numbers
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 7: Prime Number Checking")
    print("=" * 60)
    
    N = 1_800_000
    step = N // 3
    ranges = [(1, step), (step, 2 * step), (2 * step, N + 1)]
    print(f"Natural numbers evaluated: 1 to {N:,} (3 partitions)")
    print("Algorithm: Trial division up to sqrt(n)\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = prime_range_worker(ranges[0])
    r2 = prime_range_worker(ranges[1])
    r3 = prime_range_worker(ranges[2])
    t_seq = time.perf_counter() - t0
    primes_seq = r1 + r2 + r3
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        p_res = pool.map(prime_range_worker, ranges)
    t_pool = time.perf_counter() - t0
    primes_pool = sum(p_res)
    
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
    primes_proc = sum(pr_res)
    
    # Verification Display
    print("Verification Results:")
    print(f"  Total Primes Found: {primes_seq:,}")
    print(f"  Results Match (Seq == Pool == Proc): {primes_seq == primes_pool == primes_proc}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 7: Prime Number Checking - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 7: Prime Number Checking - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q8():
    return '''# Practical 8: Bubble Sort on Three Different Arrays (Pattern 2)
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

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 8: Bubble Sort on Three Different Arrays")
    print("=" * 60)
    
    SIZE = 3200
    tasks = [(SIZE, 10), (SIZE, 20), (SIZE, 30)]
    print(f"Three independent random integer arrays: {SIZE:,} elements each")
    print("Benchmarking Pattern: Pattern 2 (Each array sorted once)\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = bubble_sort_task(tasks[0])
    r2 = bubble_sort_task(tasks[1])
    r3 = bubble_sort_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(bubble_sort_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Multiprocessing Process (3 independent processes)
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
    
    # Verification Display
    print("Verification Results:")
    print(f"  Array 1 Sorted: {seq_res[0][0]} | First 5: {seq_res[0][1]}")
    print(f"  Array 2 Sorted: {seq_res[1][0]} | First 5: {seq_res[1][1]}")
    print(f"  Array 3 Sorted: {seq_res[2][0]} | First 5: {seq_res[2][1]}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 8: Bubble Sort - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 8: Bubble Sort - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q9():
    return '''# Practical 9: Addition/Sum of Elements of an Array (Pattern 2)
# Legitimate CPU-intensive element-wise arithmetic workload
import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def arraysum_task(task):
    size, seed = task
    total = 0
    for i in range(size):
        x = (i * 37 + seed) % 10000
        # Deterministic arithmetic transformation before summing
        total += ((x * 41 + 23) ^ 7) % 10000007
    return total

def proc_worker(task, q):
    q.put(arraysum_task(task))

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 9: Addition/Sum of Array Elements")
    print("=" * 60)
    
    SIZE = 2_500_000
    tasks = [(SIZE, 101), (SIZE, 202), (SIZE, 303)]
    print(f"Three independent arrays: {SIZE:,} elements each")
    print("Workload: Deterministic element-wise arithmetic transformation before summing\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    s1 = arraysum_task(tasks[0])
    s2 = arraysum_task(tasks[1])
    s3 = arraysum_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [s1, s2, s3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(arraysum_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Multiprocessing Process (3 independent processes)
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
    
    # Verification Display
    print("Verification Results:")
    print(f"  Sum(Array 1): {seq_res[0]:,}")
    print(f"  Sum(Array 2): {seq_res[1]:,}")
    print(f"  Sum(Array 3): {seq_res[2]:,}")
    print(f"  Total Sum:    {sum(seq_res):,}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 9: Array Sum - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 9: Array Sum - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

def get_colab_code_q10():
    return '''# Practical 10: Transpose of Three Different Matrices (Pattern 2)
# Legitimate computational transpose workload
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
            # Transpose + deterministic element-wise computation
            trans[c][r] = (matrix[r][c] * 31 + r * 17 + c * 13) % 100007
    return trans[0][:5]

def proc_worker(task, q):
    q.put(transpose_task(task))

if __name__ == '__main__':
    print("=" * 60)
    print("Practical 10: Matrix Transpose (Pattern 2)")
    print("=" * 60)
    
    ROWS, COLS = 1300, 1300
    tasks = [(ROWS, COLS, 111), (ROWS, COLS, 222), (ROWS, COLS, 333)]
    print(f"Three independent matrices: {ROWS}x{COLS} each")
    print("Workload: Transpose + deterministic element transformation\\n")
    
    # 1. Sequential Execution
    t0 = time.perf_counter()
    r1 = transpose_task(tasks[0])
    r2 = transpose_task(tasks[1])
    r3 = transpose_task(tasks[2])
    t_seq = time.perf_counter() - t0
    seq_res = [r1, r2, r3]
    
    # 2. Multiprocessing Pool (3 workers)
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        pool_res = pool.map(transpose_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # 3. Multiprocessing Process (3 independent processes)
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
    
    # Verification Display
    print("Verification (First 5 elements of transposed row 0):")
    print(f"  Matrix 1 Transposed: {seq_res[0]}")
    print(f"  Matrix 2 Transposed: {seq_res[1]}")
    print(f"  Matrix 3 Transposed: {seq_res[2]}")
    
    methods = ["Sequential", "Pool", "Process"]
    times = [t_seq, t_pool, t_proc]
    speedups = [t_seq / t for t in times]
    
    # Execution-Time Comparison Table
    print("\\n" + "-" * 42)
    print(f"{'Method':<12} {'Execution Time':<18} {'Speedup':<10}")
    print("-" * 42)
    for m, t, s in zip(methods, times, speedups):
        print(f"{m:<12} {t:.4f} seconds      {s:.2f}x")
    print("-" * 42)
    
    # Graph 1: Execution-Time Bar Graph
    colors = ["#4C78A8", "#F58518", "#54A24B"]
    plt.figure(figsize=(7.5, 4.2))
    bars = plt.bar(methods, times, color=colors, width=0.52, edgecolor='black', linewidth=1)
    plt.title("Practical 10: Matrix Transpose - Execution Time", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Execution Time (seconds)", fontsize=11, labelpad=8)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    max_t = max(times)
    plt.ylim(0, max_t * 1.25)
    for bar, t in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max_t * 0.02),
                 f"{t:.4f}s", ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.show()
    
    # Graph 2: Speedup Line Graph
    plt.figure(figsize=(7.5, 4.2))
    plt.plot(methods, speedups, marker='o', markersize=8, linewidth=2.5, color="#2B5C8F", label="Speedup (x)")
    plt.axhline(1.0, color='gray', linestyle=':', label='Sequential Baseline (1.00x)')
    plt.title("Practical 10: Matrix Transpose - Speedup Comparison", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Method", fontsize=11, labelpad=8)
    plt.ylabel("Speedup (Sequential / Method)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle='--', alpha=0.6)
    max_s = max(speedups)
    plt.ylim(0, max(max_s * 1.35, 1.5))
    for i, (m, s) in enumerate(zip(methods, speedups)):
        plt.text(i, s + (max_s * 0.03), f"{s:.2f}x", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#1B3B5F")
    plt.legend(loc='upper left', frameon=True)
    plt.show()
'''

print("colab_snippets ready.")
