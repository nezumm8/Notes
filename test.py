def colorbgfg():
    file = open('setting.txt', 'r')
    a = file.readline()
    b = file.readline()
    c = file.readline()
    file.close()
    return a[8:-1], b[8:], c[8:]
print(colorbgfg())