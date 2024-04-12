## CTF: LACTF 2024
# Category: Crypto
## Challenge: hOlyT
Final points: 422

# Description:
God is trying to talk to you through a noisy wire
Use nc chall.lac.tf 31171 to talk to him.

We are provided with server.py (without the comments)
``` python
from Crypto.Util.number import getPrime, bytes_to_long
import random
def legendre(a, p):
    # returns 1 if a is 1 for sure
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    # returns a square root of n modulo p
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r
def xgcd(a, b): 
    # returns x, y such that ax + by = gcd(a,b)
    if a == 0 : 
        return 0,1
             
    x1,y1 = xgcd(b%a, a) 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return x,y 
def crt(a, b, m, n):
    # Chinese Remainder Theorem
    m1, n1 = xgcd(m, n)
    return ((b *m * m1 + a *n*n1) % (m * n))

def advice(x, p, q):
    if legendre(x, p) != 1:
        exit()
    if legendre(x, q) != 1:
        exit()
    x1 = tonelli(x, p) * random.choice([1, -1])
    x2 = tonelli(x, q) * random.choice([1, -1])
    # x1, x2 are always either 1 or -1
    y = crt(x1, x2, p, q)
    return y
    
def main():
    p = getPrime(1024)
    q = getPrime(1024)
    
    N = p * q
    e = 65537
    m = bytes_to_long(b"lactf{redacted?}")
    ct = pow(m, e, N)
    print(f"ct = {ct}")
    print(f"N = {N}")
    print(f"e = {e}")
    while 1:
        x = int(input("What do you want to ask? > "))
        ad = advice(x, p, q)
        print(ad)

if __name__ == "__main__":
    main()
```

In typical RSA format, this challenge encrypts the flag and provides the encrypted form and both public keys - N and e. The goal, as usual is to decrypt the flag by figuring out p and q somehow. 

We are provided unlimited calls to the advice, which is called with our input along with p and q, so we need to understand how that works.
It first computes the legendre of our input with p and then with q and only continues if both are 1. This is simple enough - we can input 1 to guarantee this check will pass. Then too, with an input of 1, both calls to tonelli will also return 1, because the square root of 1 is 1 mod anything. 
The crt function uses xgcd to get m1 and n1 such that gcd(p, q) = p*m1 + q*n1 and returns that sum mod N. So because we control tonelli(x, p) and tonelli(x, q), we know the four possible outputs are:
crt(1, 1, p, q) = p*m1 + q*n1 (mod N)
crt(1, -1, p, q) = p*m1 - q*n1 (mod N)
crt(-1, 1, p, q) = -p*m1 + q*n1 (mod N)
crt(-1, -1, p, q) = -p*m1 - q*n1 (mod N)

It is random which one we get, but since we get unlimited inputs, we can eventually get each output. This is really nice, because if we take any two different outputs and add them together, we get either
p*2*m1 (mod N)
or 
q*2*n1 (mod N).

So we can extract the private key by computing the gcd between the sum of two outputs and N (which is p * q). The other private key comes easily by dividing N by the one we extracted, and we can decrypt the RSA encrypted flag.

``` python
from Crypto.Util.number import long_to_bytes
ct = 7795478703951910298760800512251016604742954197898050479871934501928567145784802604542002268080404992780678217646124951840673797270491710309688112924721561151731605873112953711785868170966477869814463719384874577110299248963713396172759754647405773964179242806311505685143222093888093347835985735639754440152848146516109884968142336041568834166265316368983280221226951298952481486521619997411247561491239782604374151098554182647251791561517307089804991475650432858727962467022168414859936296189874338448996484184334288550871046087698350678567999518807001116688026839842507335016985102010047274042512865191879615627189
N = 17831104667040256134725887251427780309283441190346378241363820041577227275015801947889351608323543022862201231205425355290220006633567994093510271341296137236696435486220210052887153794743228135603531011013817226919624495642090379006823492988501642462491665647285840701843758122419384518395935175111969431981176852184961902749819593573017708973408100060762005631607410042285600792954074826599343773206465846004997125247332792765111462262606314067259767823386343138746280621268625953047895333695773948796251064112811522554255832429054369092856990234149099315668149570501794323907590910167206485076585099237050507816159
e = 65537

output1 = 17831104667040256134725887251427780309283441190346378241363820041577227275015801947889351608323543022862201231205425355290220006633567994093510271341296137236696435486220210052887153794743228135603531011013817226919624495642090379006823492988501642462491665647285840701843758122419384518395935175111969431981176852184961902749819593573017708973408100060762005631607410042285600792954074826599343773206465846004997125247332792765111462262606314067259767823386343138746280621268625953047895333695773948796251064112811522554255832429054369092856990234149099315668149570501794323907590910167206485076585099237050507816158
output2 = 12543327065801962610744075756846559617980246552922417100872603818493798966059706703055149059011972141365311478492748987671188435357925094775013208156046315891049104385142491732801619782976653736068904735144419446163489344131703025119761873944419880125761507869394862188182720955132188347678851544113421703302734727531242579531323262149507434400369268532075038572395448927911344696402028869425886723564234382595072991003810126823599461424382689088309859000473754968901328087419516027916743538080683918219102060429467560165753443642775973833304701656372325574307951794081942686364095841177702997728532810737341461151015

def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

p = gcd((output1 + output2) % N, N)
q = N // p

d = pow(e, -1, (p - 1) * (q - 1))
m = pow(ct, d, N)

print(long_to_bytes(m))

```
and we get the flag
lactf{1s_r4bin_g0d?}