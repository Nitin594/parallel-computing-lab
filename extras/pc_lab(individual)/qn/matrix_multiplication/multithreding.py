import time
import threading


# Function to multiply one row
def multiply_row(i, A, B, C):

    for j in range(len(B[0])):

        total = 0

        for k in range(len(B)):
            total += A[i][k] * B[k][j]

        C[i][j] = total


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
    cols = len(B[0])

    # Create result matrix
    C = [[0 for j in range(cols)]
         for i in range(rows)]

    # Store threads
    threads = []

    # Start timer
    start_time = time.perf_counter()

    # Create threads
    for i in range(rows):

        t = threading.Thread(
            target=multiply_row,
            args=(i, A, B, C)
        )

        threads.append(t)

        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # End timer
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")

    for row in C:
        print(row)

    print("Execution Time:",
          end_time - start_time, "seconds")