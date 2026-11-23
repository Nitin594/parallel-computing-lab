10 Python Programs: Sequential, Multiprocessing, and Multithreading

Files:
01_matrix_addition.py
02_matrix_multiplication.py
03_matrix_transpose.py
04_factorial.py
05_fibonacci_series.py
06_even_odd_array.py
07_array_min_max.py
08_array_sum.py
09_bubble_sort.py
10_prime_number.py

Each file is a separate complete program and compares:
- Sequential execution
- Multiprocessing with Pool
- Multiprocessing with Process and Queue
- Multithreading

How to run:
1. Install Python 3.
2. Save/extract the files.
3. Open Command Prompt or Terminal in the folder.
4. Run: python 01_matrix_addition.py
5. Replace the filename to run another program.

Important:
- For multiprocessing, run each program as a normal .py file. On Windows, do not remove
  the if __name__ == "__main__": guard.
- For small inputs, sequential execution is often faster because creating processes
  and threads has overhead. Python threads generally do not speed up CPU-bound Python
  code because of the GIL.
- The parallel bubble-sort version sorts separate chunks and merges them; it is a
  demonstration of parallel work, not the usual fastest way to sort an array.
