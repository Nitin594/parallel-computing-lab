import time
import threading

# Function to add matrix rows
def add_rows(A, B, C, row):

    for j in range(len(A[row])):
        C[row][j] = A[row][j] + B[row][j]


# Main program
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
    cols = len(A[0])

    # Create result matrix
    C = [[0] * cols for _ in range(rows)]

    # Start execution time
    start_time = time.perf_counter()

    threads = []

    # Create threads
    for i in range(rows):

        t = threading.Thread(
            target=add_rows,
            args=(A, B, C, i)
        )

        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # End execution time
    end_time = time.perf_counter()

    # Display result
    print("Resultant Matrix:")
    for row in C:
        print(row)

    print("\nExecution Time:",
          end_time - start_time, "seconds")