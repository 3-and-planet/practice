# -*- coding:utf-8 -*-
def merge_count_split (a, b):
    c = []
    inv = 0
    i=0
    j=0
    for k in range( len(a)^2 ):
        if i < len(a) and j < len(b):
            if a[i] < b[j]:
                c.append(a[i])
                i += 1
            elif a[i] > b[j]:
                c.append(b[j])
                inv += len(a)-i
                j += 1
            elif i == len(a):
                c.append(b[j])
                j += 1
            elif j == len(b):
                c.append(a[i])
                i += 1
        return c, inv

def count_inv (data):
    n = len(data)
    if n == 1:
        return data, 0
    a, x = count_inv(data[:n/2])
    b, y = count_inv(data[n/2:])
    c, z = merge_count_split(a,b)
    return c, x + y + z

with open('algo.txt') as f:
    array = [int(line) for line in f]
    print(count_inv(array)[0])
