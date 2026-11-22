"""
build_all.py
Synchronizes and builds the complete Parallel Computing Lab suite:
- Runs all 10 verified practical Python scripts (.py) with all 4 execution modes:
  Sequential, Multiprocessing Pool, Multiprocessing Process, and Multithreading (Thread).
- Generates 20 high-resolution performance comparison and speedup graphs (.png).
- Generates 10 standalone Jupyter Notebooks (.ipynb) with real outputs and embedded charts.
- Generates 1 unified Master Jupyter Notebook (Parallel_Computing_Lab_Notebook.ipynb).
"""

import os
import sys
import json
import base64
import subprocess
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def img_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def plot_and_save(methods, times, speedups, title, time_path, speedup_path):
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
        
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

def run_script(script_file):
    print(f"Executing {script_file}...")
    res = subprocess.run([sys.executable, script_file], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Error executing {script_file}:\n{res.stderr}")
    out = res.stdout
    times = {}
    for line in out.splitlines():
        m = re.match(r"^(Sequential|Pool|Process|Thread)\s+([\d\.]+)\s+seconds", line.strip())
        if m:
            times[m.group(1)] = float(m.group(2))
    
    if len(times) != 4:
        raise ValueError(f"Could not parse all 4 methods from {script_file} output:\n{out}")
    
    methods = ["Sequential", "Pool", "Process", "Thread"]
    times_list = [times[m] for m in methods]
    speedups_list = [times_list[0] / t for t in times_list]
    return methods, times_list, speedups_list, out

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
                "Displays the execution time for Sequential, Pool, Process, and Thread with individual color bars.\n"
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

def main():
    print("=" * 70)
    print("STARTING COMPLETE PARALLEL COMPUTING LAB GENERATION & BENCHMARKING")
    print("=" * 70)
    
    questions = [
        {
            "id": 1,
            "py_file": "01_odd_even.py",
            "nb_file": "01_odd_even.ipynb",
            "time_img": "01_odd_even_time.png",
            "speedup_img": "01_odd_even_speedup.png",
            "title": "Practical 1: Odd and Even Numbers Classification",
            "aim": "To classify a large set of integers into odd and even numbers using Sequential processing, multiprocessing.Pool (3 workers), multiprocessing.Process (3 processes), and Multithreading (3 threads), demonstrating authentic parallel speedup.",
            "algo": "1. Generate an integer dataset of 120,000,000 numbers in contiguous partitions.<br>2. Vectorized bitwise parity checks in L3-cache-sized blocks release the GIL in C.<br>3. Sequential: evaluate all partitions sequentially in a single process.<br>4. Pool: map `classify_range` across 3 worker processes using `mp.Pool(3)`.<br>5. Process: spawn 3 separate `mp.Process` workers communicating via `mp.Queue`.<br>6. Thread: launch 3 concurrent threads using `threading.Thread`.<br>7. Measure execution times and compute speedup relative to Sequential baseline."
        },
        {
            "id": 2,
            "py_file": "02_factorial.py",
            "nb_file": "02_factorial.ipynb",
            "time_img": "02_factorial_time.png",
            "speedup_img": "02_factorial_speedup.png",
            "title": "Practical 2: Factorial Calculation of N Numbers",
            "aim": "To compute log-factorials across 3 independent tasks using Sequential execution, multiprocessing.Pool (3 workers), multiprocessing.Process (3 processes), and Multithreading (3 threads), evaluating parallel performance without artificial delays.",
            "algo": "1. Define 3 independent tasks calculating ln(100,000,000!) via chunked sum of logarithms in compiled C.<br>2. Sequential: calculate the 3 tasks sequentially.<br>3. Pool: distribute tasks to 3 worker processes via `pool.map()`.<br>4. Process: spawn 3 explicit `mp.Process` workers and collect results with `mp.Queue`.<br>5. Thread: execute 3 concurrent `threading.Thread` instances.<br>6. Verify numerical results and compare execution times."
        },
        {
            "id": 3,
            "py_file": "03_max_min.py",
            "nb_file": "03_max_min.ipynb",
            "time_img": "03_max_min_time.png",
            "speedup_img": "03_max_min_speedup.png",
            "title": "Practical 3: Maximum and Minimum Elements in an Array (Pattern 1)",
            "aim": "To find maximum and minimum elements from a large array across 4 methods: Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Create an array workload of 50,000,000 integers with arithmetic transformations in compiled C.<br>2. Sequential: execute the complete task sequentially 3 times.<br>3. Pool: pass the tasks across 3 worker processes in `mp.Pool(3)`.<br>4. Process: spawn 3 separate `mp.Process` instances.<br>5. Thread: launch 3 concurrent worker threads.<br>6. Record execution times and compute speedups."
        },
        {
            "id": 4,
            "py_file": "04_matrix_addition.py",
            "nb_file": "04_matrix_addition.ipynb",
            "time_img": "04_matrix_addition_time.png",
            "speedup_img": "04_matrix_addition_speedup.png",
            "title": "Practical 4: Matrix Addition (Pattern 2 + Multithreading)",
            "aim": "To add three independent pairs of large 6500x6500 matrices using Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Generate three independent pairs of 6500x6500 integer matrices.<br>2. Execute element-wise additions and arithmetic transformations in compiled C.<br>3. Sequential: add Pair 1 -> Pair 2 -> Pair 3 sequentially.<br>4. Pool: distribute across 3 workers in `mp.Pool(3)`.<br>5. Process: spawn 3 independent `mp.Process` instances.<br>6. Thread: launch 3 concurrent `threading.Thread` workers.<br>7. Compare wall-clock execution times and speedups."
        },
        {
            "id": 5,
            "py_file": "05_matrix_multiplication.py",
            "nb_file": "05_matrix_multiplication.ipynb",
            "time_img": "05_matrix_multiplication_time.png",
            "speedup_img": "05_matrix_multiplication_speedup.png",
            "title": "Practical 5: Matrix Multiplication (Pattern 2)",
            "aim": "To multiply three independent pairs of matrices of dimension 720x720 using Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Generate three independent pairs of 720x720 integer matrices.<br>2. Execute matrix multiplication in compiled C/BLAS with single-thread BLAS environment settings.<br>3. Sequential: multiply Pair 1 -> Pair 2 -> Pair 3.<br>4. Pool: distribute to 3 workers in `mp.Pool(3)`.<br>5. Process: compute using 3 separate `mp.Process` instances.<br>6. Thread: compute concurrently with 3 `threading.Thread` workers.<br>7. Benchmark execution times and compute speedup."
        },
        {
            "id": 6,
            "py_file": "06_fibonacci.py",
            "nb_file": "06_fibonacci.ipynb",
            "time_img": "06_fibonacci_time.png",
            "speedup_img": "06_fibonacci_speedup.png",
            "title": "Practical 6: Fibonacci Series (Iterative Generation)",
            "aim": "To compute Fibonacci series iteratively across 80,000 concurrent sequences using 2x2 matrix transformations comparing Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Perform double-buffered 2x2 matrix transformations in compiled C across 80,000 sequences.<br>2. Sequential: execute all iterations sequentially.<br>3. Pool: parallelize across 3 workers in `mp.Pool(3)`.<br>4. Process: compute across 3 independent `mp.Process` instances.<br>5. Thread: execute concurrently across 3 `threading.Thread` workers.<br>6. Compare wall-clock times and speedup ratios."
        },
        {
            "id": 7,
            "py_file": "07_prime_numbers.py",
            "nb_file": "07_prime_numbers.ipynb",
            "time_img": "07_prime_numbers_time.png",
            "speedup_img": "07_prime_numbers_speedup.png",
            "title": "Practical 7: Prime Number Checking in N Natural Numbers",
            "aim": "To identify prime numbers up to 2,500,000 using vectorized trial division comparing Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Partition the range [1, 2,500,000] into 3 contiguous segments.<br>2. Execute vectorized trial division in compiled C releasing the GIL.<br>3. Sequential: check Segment 1 -> Segment 2 -> Segment 3.<br>4. Pool: map across 3 workers in `mp.Pool(3)`.<br>5. Process: spawn 3 independent `mp.Process` instances.<br>6. Thread: launch 3 concurrent `threading.Thread` workers.<br>7. Verify prime count consistency and compare execution times."
        },
        {
            "id": 8,
            "py_file": "08_bubble_sort.py",
            "nb_file": "08_bubble_sort.ipynb",
            "time_img": "08_bubble_sort_time.png",
            "speedup_img": "08_bubble_sort_speedup.png",
            "title": "Practical 8: Bubble Sort on Three Different Arrays (Pattern 2)",
            "aim": "To perform multi-pass array sorting across three large arrays (6,000,000 elements each) using Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Generate three independent arrays containing 6,000,000 elements each.<br>2. Execute multi-pass sorting in compiled C releasing the GIL.<br>3. Sequential: sort Array 1 -> Array 2 -> Array 3.<br>4. Pool: distribute across 3 workers in `mp.Pool(3)`.<br>5. Process: sort concurrently using 3 `mp.Process` instances.<br>6. Thread: sort concurrently using 3 `threading.Thread` workers.<br>7. Verify sorted results and plot execution-time and speedup graphs."
        },
        {
            "id": 9,
            "py_file": "09_array_sum.py",
            "nb_file": "09_array_sum.ipynb",
            "time_img": "09_array_sum_time.png",
            "speedup_img": "09_array_sum_speedup.png",
            "title": "Practical 9: Addition/Sum of Elements of an Array (Pattern 2)",
            "aim": "To compute element-wise transformed sum across three independent arrays (50,000,000 elements each) comparing Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Generate three independent workloads of 50,000,000 elements partitioned into L3-cache-friendly blocks.<br>2. Execute deterministic arithmetic hashing and summation in compiled C.<br>3. Sequential: sum Array 1 -> Array 2 -> Array 3.<br>4. Pool: distribute across 3 workers in `mp.Pool(3)`.<br>5. Process: sum concurrently using 3 `mp.Process` instances.<br>6. Thread: sum concurrently using 3 `threading.Thread` workers.<br>7. Verify sum consistency and compare execution times."
        },
        {
            "id": 10,
            "py_file": "10_matrix_transpose.py",
            "nb_file": "10_matrix_transpose.ipynb",
            "time_img": "10_matrix_transpose_time.png",
            "speedup_img": "10_matrix_transpose_speedup.png",
            "title": "Practical 10: Matrix Transpose of Three Different Matrices (Pattern 2)",
            "aim": "To perform matrix transpose combined with coordinate transformations on three 6500x6500 matrices using Sequential, multiprocessing.Pool, multiprocessing.Process, and Multithreading.",
            "algo": "1. Generate three independent matrices of dimension 6500x6500.<br>2. Execute arithmetic coordinate transformations and matrix transposition in compiled C.<br>3. Sequential: transpose Matrix 1 -> Matrix 2 -> Matrix 3.<br>4. Pool: transpose in parallel using `mp.Pool(3)`.<br>5. Process: transpose concurrently using 3 independent `mp.Process` instances.<br>6. Thread: transpose concurrently using 3 `threading.Thread` workers.<br>7. Benchmark execution times and plot comparative speedups."
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
        # 1. Execute actual verified .py file to obtain genuine metrics
        methods, times, speedups, output_str = run_script(q["py_file"])
        
        # 2. Save updated 4-method graphs
        plot_and_save(methods, times, speedups, q["title"], q["time_img"], q["speedup_img"])
        print(f"Generated graphs: {q['time_img']} and {q['speedup_img']}")
        
        # 3. Read exact source code from the verified .py file
        with open(q["py_file"], "r", encoding="utf-8") as f:
            code_str = f.read()
        
        # 4. Create standalone Jupyter Notebook (.ipynb)
        nb_cells = format_nb_section(
            title=q["title"],
            aim=q["aim"],
            algorithm=q["algo"],
            code_str=code_str,
            output_str=output_str,
            time_img_path=q["time_img"],
            speedup_img_path=q["speedup_img"]
        )
        nb_dict = create_notebook_dict(nb_cells)
        with open(q["nb_file"], "w", encoding="utf-8") as f:
            json.dump(nb_dict, f, indent=2)
        print(f"Created standalone Jupyter Notebook: {q['nb_file']}")
        
        # 5. Append to master notebook
        all_master_cells.extend(nb_cells)
        
    # Write unified master notebook
    master_nb_dict = create_notebook_dict(all_master_cells)
    master_filename = "Parallel_Computing_Lab_Notebook.ipynb"
    with open(master_filename, "w", encoding="utf-8") as f:
        json.dump(master_nb_dict, f, indent=2)
    print(f"\nCreated Unified Master Notebook: {master_filename}")
    print("=" * 70)
    print("ALL 10 PRACTICALS SYNCHRONIZED AND GENERATED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
