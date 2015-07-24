# -*- coding:utf-8 -*-
input_file = open('/Users/KibaNeko/Project/python/practice/test.txt')
output_file = open('/Users/KibaNeko/Project/python/practice/test_out.txt','w')

output_file.write(input_file.read())

input_file.close()
output_file.close()

