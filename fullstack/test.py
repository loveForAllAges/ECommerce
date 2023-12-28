def foo(num: int) -> list:
	start, end = (0, num+1) if num >= 0 else (num, 1)
	return [-i for i in range(start, end) if i % 2 == 0]


def test() -> None:
	assert foo(10) == [0, 2, 4, 6, 8, 10]


print(foo(-2))
print(foo(10))
print(foo(0))
# print(test())
