import numpy as np
def GenerateLatinSquare(N):
    if N < 3:
        return 
    Square = np.ones((N, N), dtype = int)
    Square[0] = np.array([i+1 for i in range(N)])
    for i in range(2, N, 2):
        Square[0][i] = N - (i - 2)/2
        if i + 1 < N:
            Square[0][i + 1] = 2 + i / 2
    for i in range(1, N):
        Square[i] = (Square[i - 1]) % (N) + 1
        
    if N % 2 == 1:
        for i in range(N):
            Square[i] = np.flipud(Square[i])
    return Square



if __name__ == '__main__':
    Square = GenerateLatinSquare(9)
    print(Square)
    np.savetxt("../../Calculator/LatinSquare.csv", Square, delimiter=",")