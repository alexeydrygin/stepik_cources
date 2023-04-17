total = 0
for b in range(1, 10):
    for k in range(1, 20):
        for t in range(1, 200):
            if (b*10 + k*5 + t/2 == 100) and (b + k + t == 100):
                total += 1
                print('b=', b, 'k=', k, 't=', t)
print(total)


# a^5+b^5+c^5+d^5=e^5
n = 0
total = 0
for a in range(27, 28):
    for b in range(84, 85):
        for c in range(110, 111):
            for d in range(133, 134):
                for e in range(1, 150):
                    if a**5 + b**5 + c**5 + d**5 == e**5:
                        total += 1
                        print('a=', a, 'b=', b, 'c=', c, 'd=', d, 'e=', e)
                        print(a + b + c + d + e)
print(total)

