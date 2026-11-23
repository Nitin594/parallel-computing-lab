import time

# Define two matrices
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

# Get matrix dimensions
rows = len(A)
cols = len(A[0])

# Start execution time
start_time = time.perf_counter()

# Create result matrix
C = [[0 for j in range(cols)] for i in range(rows)]

# Sequential matrix addition
for i in range(rows):
    for j in range(cols):
        C[i][j] = A[i][j] + B[i][j]

# End execution time
end_time = time.perf_counter()

# Display result
print("Matrix A:")
for row in A:
    print(row)

print("\nMatrix B:")
for row in B:
    print(row)

print("\nResultant Matrix:")
for row in C:
    print(row)

print("\nExecution Time:",
      end_time - start_time, "seconds")