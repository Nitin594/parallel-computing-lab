"""
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
