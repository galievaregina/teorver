import math
def funProb():
     pW = 0.22
     pL = 0.2815 + 0.4985
     sum = 0.0
     for i in range(0,30):
         step = pow(pL,i) * pW
         sum += step
         print(sum)

def vi():
    vi = 1.96 * 1376.4982
    n = 1000
    for i in range(1, n):
        thPayback = vi / math.sqrt(i)
        print(-1 * thPayback)
