def counting_problems(n, m):
    a = [i for i in range(1,n+1)]
    for x in  a:
        for i in range(1, n-2):
            if i != x:
                if x in range(1,m+1):
                    new_arr = [x, i , x]
                    




if __name__ == '__main__':
    t =int(input('T:'))
    for tt in range(t):
        n,m = input('N,M:').strip().split()
        print(n, m)
        print(counting_problems(int(n), int(m)))
