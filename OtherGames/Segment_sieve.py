import math
MAXN = 100005
LL = 1000005
def segment_sieve(low, high):
    prime_num = 0
    is_prime_small = [False for _ in range(MAXN)]
    is_prime = [False for _ in range(MAXN)]
    prime = [0 for _ in range(MAXN)]
    result = []
    for i in range(int(math.sqrt(high))):
        is_prime_small[i] = True
    for i in range(high - low):
        is_prime[i] = True
    for i in range(2, int(math.sqrt(high))):
        if is_prime_small[i]:
            j = 2 * i
            while j < int(math.sqrt(high)):
                is_prime_small[j] = False
                j += i
            j = max(2, (low + i - 1)//i) * i
            while j < high:
                is_prime[j - low] = False
                j += i
    for i in range(high - low):
        if is_prime[i]:
            result.append(i + low)
    return result
    
if __name__ == "__main__":
    t = segment_sieve(37,492)
    for i in t:
        print(i, end = "\t")