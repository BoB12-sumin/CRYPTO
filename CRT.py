
import time

def MyExpMod(a, n, m):
    return a.powermod(n,m)

'''
def MyExpMod(a,n,m):
    bin = n.digits(2)
    k = len(bin)
    A = a
    for i in range(k-2,-1,-1):
        A = A^2 % m
        if bin[i] == 1 :
            A = A*a % m        
    return A
'''


def MyExtEuclid(a,b):
    #a>= b assumed    
    if a == b :
        return a,1,0    
    r1 = a % b; q1 = int(a/b)
    x1 = 1; y1 = - q1
    if r1 == 0:
        return b,0,1
     
    q2 = b//r1; r2 = b - r1*q2
    x2 = -q2; y2 = 1 + q1*q2
   
    while True :
        q3 = r1//r2; r3 = r1 - r2*q3
        if r3 == 0:
            break
        x3 = x1 - q3*x2; y3 = y1 - q3*y2
        r1 = r2; r2 = r3
        x1 = x2; y1 = y2
        x2 = x3; y2 = y3
    return r1,x2,y2

def MyInvMod(a,m) :
    g,x,invmodm = MyExtEuclid(m,a%m)
    return invmodm%m
   
#MyExpMod(a,n,m)

p=next_prime(2^1024-123)
q=next_prime(p)

n = p*q
phi_n = (p-1)*(q-1)
e = 2^16+1
d = MyInvMod(e,phi_n)

print("p="+str(p))
print("q="+str(q))
print("e="+str(e))
print("d="+str(d))
print("e*d mod phi_n="+str(e*d%phi_n))
print("n="+str(n))

pt = 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

ct = MyExpMod(pt,e,n)

start = time.time() ## RSA 복호화 시간측정 시작 ##
for i in range(1,1000) :
    dt = MyExpMod(ct,d,n)

print("time :", time.time() - start) ## RSA 복호화 시간측정 끝 ##

print("Ciphertext="+str(ct))
print("Decrypted="+str(dt))


###RSA-CRT 복호화 코드 삽입 시작 ###
start = time.time() ## RSA-CRT 복호화 시간측정 시작 ##


d1 = MyExpMod(d, 1, p-1)
d2 = MyExpMod(d, 1, q-1)
dq = inverse_mod(q, p)

for i in range(1,1000):
# m1 = ct^d1(mod p)
    m1 = MyExpMod(ct, d1, p)
# m2 = ct^d2(mod q)
    m2 = MyExpMod(ct, d2, q)
    dt_crt = m2 + (m1 - m2) * q  * (MyExpMod(dq, 1, p)) #m1 mod p
    ###RSA-CRT 복호화 코드 삽입 끝###
   
print("CRT time :", time.time() - start) ## RSA-CRT 복호화 시간측정 끝 ##

print("Decrypted using CRT="+str(dt_crt))
