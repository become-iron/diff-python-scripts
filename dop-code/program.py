# coding=utf-8
r = 16  # количество разрядов
while True:
    i = 0
    w = []
    try:
        q = int(input())
        if q < 0 and q >= -(2**r):
            q += 1
            q = bin(q)[3::]
            for i in range(len(q)):
                w += [q[i]]
                w[i] = 0 if w[i] == '1' else 1
            print((r-len(w)) * '1', sep = '', end = '')
            i = 0
            for i in range(len(w)):
                print(w[i], sep = '', end = '')
            print('\n')
        elif q >= 0 and q <= 2 ** r - 1:
            q = bin(q)[2::]
            print((r-len(str(q))) * '0', q, '\n', sep = '')
        else:
            print('\nЧисло слишком большое/маленькое\n')
    except ValueError:
        print('\nВведите число\n')
