import time
import threading


# Function to transpose one column
def transpose_column(j, A, T):

    for i in range(len(A)):
        T[j][i] = A[i][j]


if __name__ == "__main__":

    # Define matrix
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    rows = len(A)
    cols = len(A[0])

    # Create transpose matrix
    T = [[0 for i in range(rows)]
         for j in range(cols)]

    # Store threads
    threads = []

    # Start timer
    start_time = time.perf_counter()

    # Create threads
    for j in range(cols):

        t = threading.Thread(
            target=transpose_column,
            args=(j, A, T)
        )

        threads.append(t)

        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Transpose Matrix:")

    for row in T:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")