# -*- coding:utf-8 -*-

open_file = open('/Users/KibaNeko/Project/python/practice/algo.txt')
a = []

for line in open_file:
    a.append(int(line))

#print(a)
#print("==========================")

for i in range(0,100000):
    i2 = i
    if a[i] == i2:
        print(i2)
