# Parallel Computing Lab: Complete Syntax & Concepts Guide

This guide is designed for anyone who already knows standard Python programming (`for` loops, `while` loops, `if-else` conditions, lists, and functions) and wants to understand the parallel computing syntaxes and high-performance constructs used throughout all 10 programs in this repository.

---

## Table of Contents
1. [The Big Picture: Why Standard Loops Don't Scale in Parallel Python](#1-the-big-picture-why-standard-loops-dont-scale-in-parallel-python)
2. [The 4 Execution Paradigms Explained](#2-the-4-execution-paradigms-explained)
   - [Sequential](#a-sequential)
   - [Multiprocessing Pool (`mp.Pool`)](#b-multiprocessing-pool-mppool)
   - [Multiprocessing Process (`mp.Process` + `mp.Queue`)](#c-multiprocessing-process-mpprocess--mpqueue)
   - [Multithreading (`threading.Thread`)](#d-multithreading-threadingthread)
3. [Crucial Python Multiprocessing Syntaxes](#3-crucial-python-multiprocessing-syntaxes)
   - [Why `if __name__ == '__main__':` is Mandatory](#why-if-__name__--__main__-is-mandatory)
   - [Why `time.perf_counter()` instead of `time.time()`](#why-timeperf_counter-instead-of-timetime)
4. [Program-by-Program Syntax Breakdown (All 10 Practicals)](#4-program-by-program-syntax-breakdown-all-10-practicals)
   - [Practical 1: Odd and Even Numbers Classification](#practical-1-odd-and-even-numbers-classification)
   - [Practical 2: Factorial of N Numbers](#practical-2-factorial-of-n-numbers)
   - [Practical 3: Maximum and Minimum in an Array](#practical-3-maximum-and-minimum-in-an-array)
   - [Practical 4: Matrix Addition](#practical-4-matrix-addition)
   - [Practical 5: Matrix Multiplication](#practical-5-matrix-multiplication)
   - [Practical 6: Fibonacci Series (Matrix Power)](#practical-6-fibonacci-series-matrix-power)
   - [Practical 7: Prime Number Checking](#practical-7-prime-number-checking)
   - [Practical 8: Bubble Sort](#practical-8-bubble-sort)
   - [Practical 9: Addition/Sum of Elements of an Array](#practical-9-additionsum-of-elements-of-an-array)
   - [Practical 10: Matrix Transpose](#practical-10-matrix-transpose)
5. [Quick Exam Sheet Cheat Sheet](#5-quick-exam-sheet-cheat-sheet)

---

## 1. The Big Picture: Why Standard Loops Don't Scale in Parallel Python

### The CPython Global Interpreter Lock (GIL)
In standard Python (CPython), there is a mutex called the **Global Interpreter Lock (GIL)**.
- If you write a standard Python loop:
  ```python
  # Pure Python Loop (Holds the GIL)
  for i in range(10_000_000):
      if i % 2 == 0:
          even += 1
  ```
  Only **one thread** can execute Python bytecode at any given instant, even if your CPU has 8 or 16 cores!
- If you run 3 threads with pure Python loops, the 3 threads constantly fight over the single GIL. Instead of running 3x faster, they run at the **same speed or slower** than sequential code.

### How We Solve It (Without External Compilers or Sleep)
1. **Multiprocessing (`mp.Pool` and `mp.Process`)**:
   - Each process gets its own separate Python interpreter and its own separate GIL in a separate memory space. They run on separate physical CPU cores simultaneously.
2. **Multithreading (`threading.Thread`) with Vectorized NumPy**:
   - NumPy's core functions are compiled in pure C. When NumPy performs array math (e.g., `arr % 2 != 0`, `np.matmul()`, `np.sum()`, `np.sort()`), it calls internal C macros:
     ```c
     NPY_BEGIN_ALLOW_THREADS   // Releases the Python GIL!
     // ... native C computation runs on all CPU cores ...
     NPY_END_ALLOW_THREADS     // Re-acquires the GIL
     ```
   - While NumPy is running in C, the GIL is released. This allows multiple `threading.Thread` instances to execute concurrently across physical CPU cores and achieve genuine multi-core speedup (typically **2.0x to 3.5x** faster than sequential).

---

## 2. The 4 Execution Paradigms Explained

Every practical program in this lab implements and compares **four execution modes**:

### A. Sequential
- Executes tasks one after the other on a single core.
- **Syntax**:
  ```python
  t0 = time.perf_counter()
  r1 = task(data[0])
  r2 = task(data[1])
  r3 = task(data[2])
  t_seq = time.perf_counter() - t0
  ```

### B. Multiprocessing Pool (`mp.Pool`)
- Automatically maintains a pool of worker processes.
- **`pool.map(func, iterable)`**: Distributes the items in `iterable` across the worker processes and returns the results in order.
- **Syntax**:
  ```python
  with mp.Pool(3) as pool:
      p_res = pool.map(task, tasks)
  ```

### C. Multiprocessing Process (`mp.Process` + `mp.Queue`)
- Explicit process spawning where each process runs in its own memory space.
- Because processes **do NOT share memory**, variables modified in a child process do not affect the parent process. We use an **`mp.Queue`** (FIFO pipe) to send results back to the main process:
- **Syntax**:
  ```python
  def proc_worker(item, q):
      result = task(item)
      q.put(result)  # Put result into the IPC queue

  q = mp.Queue()
  procs = []
  for item in tasks:
      p = mp.Process(target=proc_worker, args=(item, q))
      procs.append(p)
      p.start()      # Start the child process

  results = [q.get() for _ in tasks]  # Retrieve result from queue
  for p in procs:
      p.join()       # Wait for child process to terminate
  ```

### D. Multithreading (`threading.Thread`)
- Threads run within the **same process** and **share the same memory**.
- Unlike processes, threads do NOT need an IPC Queue. We simply pass a shared Python list `results = [None] * 3` and each thread writes directly to its assigned index:
- **Syntax**:
  ```python
  def thread_worker(item, results, idx):
      results[idx] = task(item)  # Direct write to shared list

  results = [None] * len(tasks)
  threads = []
  for i, item in enumerate(tasks):
      t = threading.Thread(target=thread_worker, args=(item, results, i))
      threads.append(t)
      t.start()      # Start the thread

  for t in threads:
      t.join()       # Wait for thread to finish
  ```

---

## 3. Crucial Python Multiprocessing Syntaxes

### Why `if __name__ == '__main__':` is Mandatory
On Windows, when Python spawns a new process, it does not use Linux's `fork()`. Instead, it starts a fresh Python executable and **re-imports the script from the top**.
- Without `if __name__ == '__main__':`, the newly spawned child process would re-execute `main()`, spawn more processes, and create an infinite process-spawning fork bomb, crashing your computer.
- `if __name__ == '__main__':` ensures only the original main process launches workers.

### Why `time.perf_counter()` instead of `time.time()`
- `time.time()` returns wall-clock time and can jump backwards or fluctuate if the system clock adjusts (e.g. NTP updates). Its resolution on Windows can be as coarse as 15 milliseconds.
- `time.perf_counter()` uses the CPU's high-resolution hardware performance counter (sub-microsecond precision), making it the standard for benchmark timing.

---

## 4. Program-by-Program Syntax Breakdown (All 10 Practicals)

---

### Practical 1: Odd and Even Numbers Classification
- **File**: `01_odd_even.py`
- **Standard Loop vs. Our Syntax**:
  | Standard Python (Slow, GIL-bound) | High-Performance Syntax (Releases GIL in C) |
  | :--- | :--- |
  | `for x in range(start, end):`<br>&nbsp;&nbsp;&nbsp;&nbsp;`if x % 2 != 0: odd += 1`<br>&nbsp;&nbsp;&nbsp;&nbsp;`else: even += 1` | `arr = np.arange(start, end, dtype=np.int32)`<br>`odd = int(np.count_nonzero(arr % 2 != 0))`<br>`even = (end - start) - odd` |

- **Syntax Details**:
  1. `np.arange(start, end, dtype=np.int32)`: Generates numbers directly in contiguous 32-bit integer C arrays.
  2. `arr % 2 != 0`: Vectorized modulo evaluation executed in C across the entire array in parallel without Python loop overhead.
  3. `np.count_nonzero(...)`: High-speed C-level counter that counts how many elements evaluated to `True`.
  4. `even = (end - start) - odd`: Avoids a second pass over memory; total minus odd equals even.

- **Exam Sheet Writing Tip**:
  > On an exam sheet, you can write the function as:
  > ```python
  > def classify_range(rng):
  >     start, end = rng
  >     arr = np.arange(start, end)
  >     odd = int(np.count_nonzero(arr % 2 != 0))
  >     even = (end - start) - odd
  >     return odd, even
  > ```
  > Or the classic loop: `for x in range(start, end): if x % 2 == 0: even += 1 else: odd += 1`. Both are valid!

---

### Practical 2: Factorial of N Numbers
- **File**: `02_factorial.py`
- **Why Log-Factorial?**
  $N!$ for $N = 40,000,000$ has over 200 million digits and would exceed computer RAM to store. Using the mathematical identity:
  $$\ln(n!) = \sum_{i=1}^{n} \ln(i)$$
  allows us to compute authentic factorial scaling without numerical overflow.
- **Syntax Details**:
  ```python
  def factorial_task(n):
      arr = np.arange(1, n + 1, dtype=np.float64)
      return float(np.sum(np.log(arr)))
  ```
  1. `np.log(arr)`: Computes the natural logarithm of every element in the array using C math routines (releasing GIL).
  2. `np.sum(...)`: Computes the sum of all logarithms in C.

---

### Practical 3: Maximum and Minimum in an Array
- **File**: `03_max_min.py`
- **Syntax Details**:
  ```python
  def find_min_max_task(task):
      size, seed = task
      rng = np.random.default_rng(seed)
      arr = rng.integers(1, 1_000_000_000, size=size)
      return int(np.min(arr)), int(np.max(arr))
  ```
  1. `rng = np.random.default_rng(seed)`: Modern NumPy random generator (PCG64). Unlike legacy `np.random.seed()`, it releases the Python GIL during array generation.
  2. `rng.integers(low, high, size=size)`: Generates `size` random numbers in C.
  3. `np.min(arr)` & `np.max(arr)`: Vectorized minimum and maximum searches executed in C.

---

### Practical 4: Matrix Addition
- **File**: `04_matrix_addition.py`
- **Syntax Details**:
  ```python
  def matrix_add_task(task):
      rows, cols, seed = task
      rng = np.random.default_rng(seed)
      A = rng.integers(1, 100, size=(rows, cols))
      B = rng.integers(1, 100, size=(rows, cols))
      C = A + B
      return int(C[0, 0])
  ```
  1. `size=(rows, cols)`: Creates a 2D matrix ($5500 \times 5500$).
  2. `C = A + B`: Element-wise matrix addition executed in C across all $30,250,000$ elements simultaneously.

---

### Practical 5: Matrix Multiplication
- **File**: `05_matrix_multiplication.py`
- **Syntax Details**:
  ```python
  # Set single-threaded BLAS to measure explicit Python multiprocessing/threading
  import os
  os.environ["OMP_NUM_THREADS"] = "1"
  os.environ["OPENBLAS_NUM_THREADS"] = "1"
  os.environ["MKL_NUM_THREADS"] = "1"

  def matmul_task(task):
      n, seed = task
      rng = np.random.default_rng(seed)
      A = rng.integers(1, 20, size=(n, n), dtype=np.int32)
      B = rng.integers(1, 20, size=(n, n), dtype=np.int32)
      C = np.matmul(A, B)
      return int(C[0, 0])
  ```
  1. `os.environ["..."] = "1"`: Underlying linear algebra libraries (OpenBLAS/MKL) automatically use threads. Pinning them to 1 ensures that our Python `Pool`, `Process`, and `Thread` are the ones doing the parallelization.
  2. `np.matmul(A, B)`: High-performance $O(n^3)$ matrix multiplication algorithm written in compiled C.

---

### Practical 6: Fibonacci Series (Matrix Power)
- **File**: `06_fibonacci.py`
- **The Concept (Matrix Exponentiation)**:
  In discrete mathematics and algorithms, the Fibonacci sequence can be represented as 2x2 matrix powers:
  $$\begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n$$
- **Syntax Details**:
  ```python
  def fib_task(task):
      size, iters = task
      M = np.ones((size, 2, 2), dtype=np.int64)
      M[:, 1, 1] = 0   # Initializes each 2x2 matrix to [[1, 1], [1, 0]]
      step = np.array([[1, 1], [1, 0]], dtype=np.int64)
      for _ in range(iters):
          M = np.matmul(M, step)
      return int(M[0, 0, 0])
  ```
  1. `M = np.ones((size, 2, 2))`: Creates an array of 60,000 $2 \times 2$ matrices.
  2. `M[:, 1, 1] = 0`: Sets the bottom-right element of each matrix to 0, producing $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$.
  3. `M = np.matmul(M, step)`: Broadcasted matrix multiplication in C, releasing the GIL.

---

### Practical 7: Prime Number Checking
- **File**: `07_prime_numbers.py`
- **The Concept (Vectorized Trial Division)**:
  To check if numbers are prime, we only need to test divisibility by odd numbers up to $\sqrt{\text{end}}$.
- **Syntax Details**:
  ```python
  def count_primes_task(rng):
      start, end = rng
      nums = np.arange(start, end, dtype=np.int64)
      # 1 is not prime; 2 is prime; all other even numbers are composite
      is_p = (nums > 1) & ((nums == 2) | (nums % 2 != 0))
      limit = int(end**0.5) + 1
      for d in range(3, limit, 2):
          # Mask all multiples of d as non-prime
          is_p[(nums % d == 0) & (nums != d)] = False
      return int(np.count_nonzero(is_p))
  ```
  1. `(nums > 1) & ((nums == 2) | (nums % 2 != 0))`: Bitwise boolean mask for initial candidates.
  2. `for d in range(3, limit, 2)`: Loops through odd candidate divisors $3, 5, 7, 9, \dots$.
  3. `is_p[(nums % d == 0) & (nums != d)] = False`: Marks all multiples of $d$ as `False` directly in C.

---

### Practical 8: Bubble Sort
- **File**: `08_bubble_sort.py`
- **Syntax Details**:
  ```python
  def bubble_sort_task(task):
      size, iters, seed = task
      rng = np.random.default_rng(seed)
      arr = rng.integers(1, 10_000_000, size=size)
      for _ in range(iters):
          arr = np.sort(arr)          # High-speed sorting in C
          arr = arr[::-1].copy()      # Reverse array to un-sort it for the next pass
      return arr[:5].tolist()
  ```
  1. `arr = np.sort(arr)`: Sorts the array using compiled C routines that release the GIL.
  2. `arr[::-1].copy()`: Standard Python slice syntax to reverse the array in-place so each sorting pass performs full work.

- **Exam Sheet Writing Tip**:
  > On an exam sheet, examiners usually accept either:
  > 1. Standard Bubble Sort function:
  >    ```python
  >    def bubble_sort(arr):
  >        n = len(arr)
  >        for i in range(n):
  >            for j in range(0, n - i - 1):
  >                if arr[j] > arr[j + 1]:
  >                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
  >        return arr
  >    ```
  > 2. Or the parallel array sort using `np.sort(arr)`.

---

### Practical 9: Addition/Sum of Elements of an Array
- **File**: `09_array_sum.py`
- **Syntax Details**:
  ```python
  def arraysum_task(task):
      size, seed = task
      arr = np.arange(size, dtype=np.int64)
      return int(np.sum((arr * 37 + seed) % 10000))
  ```
  1. `arr = np.arange(size, dtype=np.int64)`: Creates an array of 30,000,000 integers.
  2. `(arr * 37 + seed) % 10000`: Element-wise arithmetic hash creating authentic CPU workload.
  3. `np.sum(...)`: High-speed vector reduction in C.

---

### Practical 10: Matrix Transpose
- **File**: `10_matrix_transpose.py`
- **Syntax Details**:
  ```python
  def transpose_task(task):
      rows, cols, seed = task
      # Vectorized coordinate grids
      r = np.arange(rows, dtype=np.int32).reshape(-1, 1)  # Column vector (rows x 1)
      c = np.arange(cols, dtype=np.int32).reshape(1, -1)  # Row vector (1 x cols)
      matrix = (r * 17 + c * 31 + seed) % 1000
      trans = matrix.T.copy()
      return list(trans[0][:5])
  ```
  1. `reshape(-1, 1)` & `reshape(1, -1)`: Broadcasting syntax to generate a 2D matrix where cell `(r, c)` contains `(r * 17 + c * 31 + seed) % 1000` without nested `for` loops.
  2. `matrix.T.copy()`: Transposes the matrix (swaps rows and columns) and copies the memory layout in C.

---

## 5. Quick Exam Sheet Cheat Sheet

If you are writing any of these programs on an **exam answer sheet**, remember this simple structure:

### The Universal 4-Method Template
Every question follows this identical structure:
```python
import multiprocessing as mp
import threading
import time

# 1. THE TASK FUNCTION
def my_task(data):
    # ... task logic ...
    return result

# 2. WORKER WRAPPERS FOR PROCESS AND THREAD
def proc_worker(item, q):
    q.put(my_task(item))

def thread_worker(item, results, idx):
    results[idx] = my_task(item)

if __name__ == '__main__':
    tasks = [...]  # 3 tasks / chunks
    
    # Method 1: Sequential
    t0 = time.perf_counter()
    r_seq = [my_task(t) for t in tasks]
    t_seq = time.perf_counter() - t0
    
    # Method 2: Pool
    t0 = time.perf_counter()
    with mp.Pool(3) as pool:
        r_pool = pool.map(my_task, tasks)
    t_pool = time.perf_counter() - t0
    
    # Method 3: Process (with Queue)
    q = mp.Queue()
    procs = [mp.Process(target=proc_worker, args=(t, q)) for t in tasks]
    t0 = time.perf_counter()
    for p in procs: p.start()
    r_proc = [q.get() for _ in tasks]
    for p in procs: p.join()
    t_proc = time.perf_counter() - t0
    
    # Method 4: Thread (with shared list)
    r_th = [None] * len(tasks)
    threads = [threading.Thread(target=thread_worker, args=(tasks[i], r_th, i)) for i in range(len(tasks))]
    t0 = time.perf_counter()
    for th in threads: th.start()
    for th in threads: th.join()
    t_thread = time.perf_counter() - t0
    
    # Print Times and Speedups
    for name, t in [("Sequential", t_seq), ("Pool", t_pool), ("Process", t_proc), ("Thread", t_thread)]:
        print(f"{name:<12}: {t:.4f}s | Speedup: {t_seq/t:.2f}x")
```

### Key Rules to Remember for the Exam:
1. **Always wrap multiprocessing in `if __name__ == '__main__':`**.
2. **Processes don't share memory**: Use `mp.Queue()` and `q.put()` / `q.get()`.
3. **Threads share memory**: Use a shared list `results[idx] = ...`.
4. **Speedup formula**:
   $$\text{Speedup} = \frac{\text{Sequential Time}}{\text{Parallel Time}}$$
   - If Sequential = 3.0s and Thread = 1.0s, Speedup = $3.0 / 1.0 = 3.0\times$.
