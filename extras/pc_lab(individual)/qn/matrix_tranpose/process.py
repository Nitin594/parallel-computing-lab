import time
from multiprocessing import Process, Queue


# Function to transpose one column
def transpose_column(j, A, q):

    result = []

    for i in range(len(A)):
        result.append(A[i][j])

    # Send result to queue
    q.put((j, result))


if __name__ == "__main__":

    # Define matrix
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    rows = len(A)
    cols = len(A[0])

    # Create queue
    q = Queue()

    # Store processes
    processes = []

    # Start timer
    start_time = time.perf_counter()

    # Create processes
    for j in range(cols):

        p = Process(
            target=transpose_column,
            args=(j, A, q)
        )

        processes.append(p)

        p.start()

    # Wait for all processes
    for p in processes:
        p.join()

    # Create transpose matrix
    T = [[0 for i in range(rows)]
         for j in range(cols)]

    # Collect results
    for i in range(cols):

        col, result = q.get()

        T[col] = result

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Transpose Matrix:")

    for row in T:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")

    q.close()