def copyfile(read,write):
    write(read())

if __name__=='__main__':
    import sys
    copyfile(sys.stdin.read,sys.stdout.write)

