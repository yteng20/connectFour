def check_three_in_a_row(arr, c, k):
    n = len(arr)
    m = len(arr[0])

    # Check horizontally
    for i in range(n):
        for j in range(m - k + 1):
            if all(arr[i][j + l] == c for l in range(k)):
                return True

    # Check vertically
    for i in range(n - k + 1):
        for j in range(m):
            if all(arr[i + l][j] == c for l in range(k)):
                return True

    # Check diagonally (top-left to bottom-right)
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            if all(arr[i + l][j + l] == c for l in range(k)):
                return True

    # Check diagonally (top-right to bottom-left)
    for i in range(n - k + 1):
        for j in range(k - 1, m):
            if all(arr[i + l][j - l] == c for l in range(k)):
                return True

    return False

# Test cases
arr1 = [
    ['a', 'b', 'f', 'c'],
    ['e', 'f', 'c', 'c'],
    ['h', 'c', 'f', 'c'],
    ['c', 'l', 'm', 't']
]

arr2 = [
    ['a', 'b', 'c', 'd', 'r'],
    ['e', 'c', 'g', 'c', 'r'],
    ['i', 'j', 'k', 'l', 'c'],
    ['m', 'n', 'o', 'p', 'c']
]

print(check_three_in_a_row(arr1, 'c', 1))  # True
print(check_three_in_a_row(arr2, 'c', 3))  # False
