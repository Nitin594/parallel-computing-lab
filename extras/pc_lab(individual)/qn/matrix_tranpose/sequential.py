import time

# Define matrix
A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Get dimensions
rows = len(A)
cols = len(A[0])

# Start timer
start_time = time.perf_counter()

# Create transpose matrix
T = [[0 for i in range(rows)]
     for j in range(cols)]

# Perform transpose
for i in range(rows):
    for j in range(cols):
        T[j][i] = A[i][j]

# End timer
end_time = time.perf_counter()

# Display result
print("Original Matrix:")
for row in A:
    print(row)

print("\nTranspose Matrix:")
for row in T:
    print(row)

print("\nExecution Time:",
      end_time - start_time, "seconds")