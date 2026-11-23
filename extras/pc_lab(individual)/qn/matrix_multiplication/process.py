import time
from multiprocessing import Process, Queue


# Function to multiply one row
def multiply_row(i, A, B, q):

    result = []

    for j in range(len(B[0])):

        total = 0

        for k in range(len(B)):
            total += A[i][k] * B[k][j]

        result.append(total)

    # Send result to queue
    q.put((i, result))


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

    # Store processes
    processes = []

    # Start timer
    start_time = time.perf_counter()

    # Create processes
    for i in range(rows):

        p = Process(
            target=multiply_row,
            args=(i, A, B, q)
        )

        processes.append(p)

        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    # Create result matrix
    C = [[0 for j in range(len(B[0]))]
         for i in range(rows)]

    # Collect results
    for i in range(rows):

        row, result = q.get()

        C[row] = result

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")

    for row in C:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")

    q.close()