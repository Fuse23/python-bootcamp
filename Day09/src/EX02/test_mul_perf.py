from time import time

import matrix
import mul_base


# x = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9],
#     [10, 11, 12],
# ]
# y = [
#     [1, 2],
#     [1, 2],
#     [3, 4],
# ]
x = [[j for j in range(100)] for i in range(100)]
y = [[j for j in range(100)] for i in range(100)]


def show(matrix: list[list[int]]) -> None:
    for _ in matrix:
        print(_)
    print()


# print(f"matrix A:\n{show(x)}")
# print(f"matrix B:{show(y)}")

start_cy = time()
res_cy = matrix.mul(x, y)
end_cy = time()
time_cy = end_cy - start_cy

start_py = time()
res_py = mul_base.mul(x, y)
end_py = time()
time_py = end_py - start_py

# start_old = time()
# res_old = matrix.old_mul(x, y)
# end_old = time()
# time_old = end_old - start_old

assert res_cy == res_py

print(f"Cython time: {time_cy}")
print(f"Python time: {time_py}")
# print(f"Old Cython time: {time_old}")
print(
    f"Difference between pure python and cython is {time_py - time_cy}"
    f"=> cython faster than python in {(time_py*10000)/(time_cy*10000)} times"
)
