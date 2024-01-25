p  = random_prime(2**321, False, 2**320)
print('p =', p)

q = random_prime(2**11, False, 2**(11-1))
print('q =', q)


n = p*q
phi = euler_phi(n)
print('phi =', phi)

e=65537

d = e^(-1)%phi
print('d=', d)
print (e*d % phi)

m = 1234567890123456789
a= mod(m, n)^e
print('a=', a)

dm = mod(a, n)^d
print('dm= ', dm)



