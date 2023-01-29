# 说明：返回小于upperBound的所有素数
def Euler_sieve(upperBound):                                        
    filter = [False for i in range(upperBound+1)]
    primeNumbers=[]
    for num in range(2,upperBound+1):
        if not filter[num]:
            primeNumbers.append(num)
        for prime in primeNumbers:
            if num * prime > upperBound:
                break
            filter[num * prime]=True
            if num%prime==0:      
                break
    return primeNumbers
 
if __name__=='__main__':
    Result = Euler_sieve(500)
    for i in Result:
        print(i, end = "\t")