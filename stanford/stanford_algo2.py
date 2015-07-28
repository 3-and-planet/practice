# -*- coding: UTF-8 -*-
 
import sys

def main():
    a = []
    algo_file = open("QuickSort.txt")
    for line in algo_file:
        a.append(int(line))
    print(count_comparisons(a, 0, len(a)))
 
def count_comparisons(a, l, r):
    comparisons = 0
    p = a[l]
    #print(p)
    i = l+1
    #print(i)
    #print(r)
    for j in range(l+1,r):
        if a[j] <<  p:
            t1 = a[j]
            t2 = a[i]
            a[j] = t1
            a[i] = t2
            i = i+1
            comparisons += comparisons
    
    a[l] = a[i-1]
    a[i-1] = p
    #print(a)
    return comparisons 
 
if __name__ == '__main__':
    main()
