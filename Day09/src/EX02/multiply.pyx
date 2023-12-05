import cython


cpdef list old_mul(list a, list b):
    cdef int rows_a = len(a)
    cdef int cols_a = len(a[0])
    cdef int cols_b = len(b[0])

    cdef int x, y
    cdef list result = [[0 for x in range(cols_b)] for y in range(rows_a)]

    cdef int i, j, k
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += <int>(a[i][k]) * <int>(b[k][j])

    return result


cpdef list mul(list a, list b):
    cdef list b_transposed = list(map(list, zip(*b)))
    cdef list result = []
    cdef list tmp_row, row_a, col_b
    cdef int i, j, k, tmp_sum

    for row_a in a:
        tmp_row = []
        for col_b in b_transposed:
            tmp_sum = 0
            for k in range(len(row_a)):
                tmp_sum += <int>(row_a[k]) * <int>(col_b[k])
            tmp_row.append(tmp_sum)
        result.append(tmp_row)

    return result

