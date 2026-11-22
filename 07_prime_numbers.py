"""
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
