n = eval((input()))
mat = [ [0 for i in range(n)] for j in range(n)]
visited = []
num = 1
i ,j = (n-1)//2, (n-1)//2
prev=(i, j)
if n%2 :
    val = (0, n-1)
else:
    val = (n-1, 0)
    
while not ( (i, j) == val) and 0 <= i < n and 0 <= j < n:
    mat[i][j] = num 
    num += 1
    visited.append((i,j))
    if (i,j) == prev:
        j+=1
    elif prev == (i,j-1):
        prev = (i,j)
        if (i+1,j) in visited:
            j += 1
        else:
            i += 1
    elif prev == (i,j+1):
        prev = (i,j)
        if (i-1,j) in visited:
            j -= 1
        else:
            i -= 1
    elif prev == (i-1,j):
        prev = (i,j)
        if (i,j-1) in visited:
            i += 1
        else:
            j -= 1
    elif prev == (i+1,j):
        prev = (i,j)
        if (i,j+1) in visited:
            i -= 1
        else:
            j += 1
    mat[val[0]][val[1]] = num
for row in mat:
    for cell in row:
        print(cell,end='\t')
    print()