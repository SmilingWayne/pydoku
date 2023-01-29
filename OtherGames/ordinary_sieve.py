# 构造一个从3开始的奇数序列
def init():
	n = 3
	while True:
		yield n
		n += 2
# 筛选函数：
def choose(n):
	return lambda x: x % n > 0
# 定义一个生成器,不断返回下一个素数：
def primes():
	yield 2
	m = init()
	while True:
		n = next(m)
		yield n
		m = filter(choose(n),m)

if __name__ == "__main__":
    N = 20000
    for n in primes():
        if n < N:
            print(n,end='\t')
        else:
            break

