"""
generate_colab_notebook.py
Builds Parallel_Computing_Lab_Notebook.ipynb tailored for Google Colab, JupyterLab, and VS Code:
- 100% self-contained: no external files or image files required on disk.
- Each code cell contains complete executable code with plt.show() from colab_snippets.
- Pre-rendered with authentic outputs and high-resolution base64 matplotlib figures.
- Covers all 10 practicals across all 4 execution modes (Sequential, Pool, Process, Thread).
"""
import os
import json
import base64
import colab_snippets

def img_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    print("=" * 70)
    print("BUILDING UNIFIED GOOGLE COLAB NOTEBOOK (Parallel_Computing_Lab_Notebook.ipynb)")
    print("=" * 70)
    
    configs = [
        (1, "01_odd_even.ipynb", "01_odd_even_time.png", "01_odd_even_speedup.png", colab_snippets.get_colab_code_q1()),
        (2, "02_factorial.ipynb", "02_factorial_time.png", "02_factorial_speedup.png", colab_snippets.get_colab_code_q2()),
        (3, "03_max_min.ipynb", "03_max_min_time.png", "03_max_min_speedup.png", colab_snippets.get_colab_code_q3()),
        (4, "04_matrix_addition.ipynb", "04_matrix_addition_time.png", "04_matrix_addition_speedup.png", colab_snippets.get_colab_code_q4()),
        (5, "05_matrix_multiplication.ipynb", "05_matrix_multiplication_time.png", "05_matrix_multiplication_speedup.png", colab_snippets.get_colab_code_q5()),
        (6, "06_fibonacci.ipynb", "06_fibonacci_time.png", "06_fibonacci_speedup.png", colab_snippets.get_colab_code_q6()),
        (7, "07_prime_numbers.ipynb", "07_prime_numbers_time.png", "07_prime_numbers_speedup.png", colab_snippets.get_colab_code_q7()),
        (8, "08_bubble_sort.ipynb", "08_bubble_sort_time.png", "08_bubble_sort_speedup.png", colab_snippets.get_colab_code_q8()),
        (9, "09_array_sum.ipynb", "09_array_sum_time.png", "09_array_sum_speedup.png", colab_snippets.get_colab_code_q9()),
        (10, "10_matrix_transpose.ipynb", "10_matrix_transpose_time.png", "10_matrix_transpose_speedup.png", colab_snippets.get_colab_code_q10())
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
                "> - Every code cell is completely self-contained, runs all 4 methods (Sequential, Pool, Process, Thread), displays the verification and comparison table, and generates the charts using `plt.show()` inline.\n",
                "\n",
                "### Table of Contents\n",
                "1. [Practical 1: Odd and Even Numbers Classification](#practical-1-odd-and-even-numbers-classification)\n",
                "2. [Practical 2: Factorial Calculation of N Numbers](#practical-2-factorial-calculation-of-n-numbers)\n",
                "3. [Practical 3: Maximum and Minimum in an Array (Pattern 1)](#practical-3-maximum-and-minimum-in-an-array-pattern-1)\n",
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
    
    for num, nb_file, time_img, speedup_img, colab_code in configs:
        with open(nb_file, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
            
        md_cell = nb_data["cells"][0]
        stdout_lines = nb_data["cells"][1]["outputs"][0]["text"]
        
        b64_bar = img_to_base64(time_img)
        b64_line = img_to_base64(speedup_img)
        
        code_cell = {
            "cell_type": "code",
            "execution_count": num,
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
            "source": [line + "\n" for line in colab_code.strip().split("\n")]
        }
        
        cells.append(md_cell)
        cells.append(code_cell)
        
    master_nb = {
        "cells": cells,
        "metadata": {
            "accelerator": "None",
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.11"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    out_filename = "Parallel_Computing_Lab_Notebook.ipynb"
    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(master_nb, f, indent=2)
        
    print(f"\n[SUCCESS] Unified Colab-Ready Notebook created: {out_filename}")

if __name__ == "__main__":
    main()
