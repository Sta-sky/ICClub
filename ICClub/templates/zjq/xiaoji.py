"""
母鸡5  3  小1  100只  200块
"""


o = 0
for i in range(26):
    ss = 200 - i * 5
    if ss < 100 - i:
        continue
    for j in range(100 - i):
        sc = 200 - 5 * i - 3 * j
        if sc < 100 - i - j or sc < 0 or sc > 100 - i - j:
            continue
        o += 1

print(o)
