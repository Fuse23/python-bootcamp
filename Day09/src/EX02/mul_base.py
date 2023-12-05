from itertools import tee


def mul(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


x = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]
y = [
    [1, 2],
    [1, 2],
    [3, 4],
]

if __name__ == "__main__":
    print(mul(x, y))
# [
#   [12, 18],
#   [27, 42],
#   [42, 66],
#   [57, 90]
# ]
