import numba
import multiprocessing as mp
import threading
import time

@numba.jit(nopython=True, nogil=True)
def fib_core(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    for _ in range(2, n + 1):
        c = (a + b) % 1000000007
        a = b
        b = c
    return b

def fib_task(n):
    return fib_core(n)

def proc_worker(n, q):
    q.put(fib_task(n))

def thread_worker(n, results, idx):
    results[idx] = fib_task(n)

def warmup():
    _ = fib_core(10)

if __name__ == '__main__':
    warmup()
    # N = 350_000_000
    N = 350_000_000
    tasks = [N, N, N]

    # 1. Sequential
    t0 = time.perf_counter()
    r1 = fib_task(tasks[0])
    r2 = fib_task(tasks[1])
    r3 = fib_task(tasks[2])
    t_seq = time.perf_counter() - t0

    # 2. Pool
    t0 = time.perf_counter()
    with mp.Pool(3, initializer=warmup) as pool:
        p_res = pool.map(fib_task, tasks)
    t_pool = time.perf_counter() - t0

    # 3. Process
    q = mp.Queue()
    procs = []
    t0 = time.perf_counter()
    for n in tasks:
        p = mp.Process(target=proc_worker, args=(n, q))
        procs.append(p)
        p.start()
    pr_res = [q.get() for _ in range(3)]
    for p in procs:
        p.join()
    t_proc = time.perf_counter() - t0

    # 4. Multithreading
    thread_res = [None, None, None]
    threads = []
    t0 = time.perf_counter()
    for idx, n in enumerate(tasks):
        th = threading.Thread(target=thread_worker, args=(n, thread_res, idx))
        threads.append(th)
        th.start()
    for th in threads:
        th.join()
    t_th = time.perf_counter() - t0

    print(f"Sequential: {t_seq:.4f}s  (1.00x)")
    print(f"Pool:       {t_pool:.4f}s  ({t_seq/t_pool:.2f}x)")
    print(f"Process:    {t_proc:.4f}s  ({t_seq/t_proc:.2f}x)")
    print(f"Thread:     {t_th:.4f}s  ({t_seq/t_th:.2f}x)")
