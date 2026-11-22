"""
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
