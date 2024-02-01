import hashlib
from sage.all import FiniteField, EllipticCurve, Integer, randint

# elliptic curve domain parameters, prime192v1
F = FiniteField(2**192 - 2**64 - 1)  # 소수
a = -3  # 파라미터, 타원곡선의 계수 a,b
b = 0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1
E = EllipticCurve(F, [a, b])  # 계수를 가지고 F에 정의된 점을 뽑아용
P = E(
    (
        0x188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012,
        0x07192B95FFC8DA78631011ED6B24CDD573F977A11E794811,
    )
)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831
Fn = FiniteField(n)  # order를 모듈러 함.


def digest(msg):
    msg = str(msg)
    return Integer("0x" + hashlib.sha1(msg.encode()).hexdigest())


def ec_keygen():
    d = randint(1, n - 1)
    Q = d * P
    return (Q, d)


def ecdsa_sign(d, m):
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = randint(1, n - 1)
            Q = k * P
            (x1, y1) = Q.xy()
            r = Fn(x1)
        kk = Fn(k)
        e = digest(m)
        s = (kk ** (-1)) * (e + d * r)
    return [r, s]


def ecdsa_verify(Q, m, r, s):
    e = digest(m)
    w = s ** (-1)
    u1 = e * w
    u2 = r * w
    P1 = Integer(u1) * P
    P2 = Integer(u2) * Q
    X = P1 + P2
    (x, y) = X.xy()
    v = Fn(x)
    return v == r


# TEST
(Q, d) = ec_keygen()
m = "signed message"
not_m = "signed message"

[r, s] = ecdsa_sign(d, m)
result = ecdsa_verify(Q, not_m, r, s)

print("EC Public Key       : ", Q.xy())
print("EC Private Key      : ", d)
print("Signed Message      : ", m)
print("Signature     : ")
print(" r = ", r)
print(" s = ", s)
print("Verified Message    : ", not_m)
print("Verification Result : ", result)
