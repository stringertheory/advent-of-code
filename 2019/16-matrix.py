import numpy as np
from scipy import sparse

a = np.arange(9).reshape(3, 3)
a_sparse = sparse.csr_matrix(a)

b = np.array([[1, 2, 3]])
print(a)
print(b.T)
print(a * b.T)
print(a_sparse.dot(b.T).sum(axis=1))

result = [
    0 * 1 + 1 * 2 + 2 * 3,
    3 * 1 + 4 * 2 + 5 * 3,
    6 * 1 + 7 * 2 + 8 * 3,
]
print(result)
