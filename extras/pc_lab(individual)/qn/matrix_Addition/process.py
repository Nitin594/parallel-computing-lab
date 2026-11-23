import time
from multiprocessing import Process, Queue

# Function to add matrix rows
def add_rows(A, B, row, q):

    result = []

    for j in range(len(A[row])):
        result.append(A[row][j] + B[row][j])

    q.put((row, result))


if __name__ == "__main__":

    # Define matrices
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    B = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    rows = len(A)

    # Create queue
    q = Queue()

    # Start execution time
    start_time = time.perf_counter()

    processes = []

    # Create separate processes
    for i in range(rows):

        p = Process(
            target=add_rows,
            args=(A, B, i, q)
        )

        processes.append(p)
        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    # Collect results
    C = [[0] * len(A[0]) for _ in range(rows)]

    for _ in range(rows):
        row, result = q.get()
        C[row] = result

    # End execution time
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")
    for row in C:
        print(row)

    print("\nExecution Time:",
          end_time - start_time, "seconds")