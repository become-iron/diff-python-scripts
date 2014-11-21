import random
min_number=-10
max_number=10
a=[[random.randint(min_number,max_number) for i in range(3)] for j in range(3)]
b=[[random.randint(min_number,max_number) for i in range(3)] for j in range(3)]
print(a,'\n',b,'\n',sep='')
print([[a[line][0]*b[0][j]+a[line][1]*b[1][j]+a[line][2]*b[2][j] for j in range(3)] for line in range(3)])
