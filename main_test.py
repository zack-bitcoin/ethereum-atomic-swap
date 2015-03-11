import bitcoin as b
from pyethereum import utils

def hash_list(l):
    def g(x):
        if type(x) in [int, long]: x=utils.int_to_big_endian(x)
        return x
    y=map(g, l)
    y=[utils.zpad(x, 32) for x in y]
    y=''.join(y)
    #save for pretty print z="".join("{:02x}".format(ord(c)) for c in y)
    return b.sha256(y)
def mk_acc(n):
    out={"priv":utils.sha3("brainwallet"+str(n))}
    out["pub"]=b.privtopub(out["priv"])
    out["addr"]=int(utils.privtoaddr(out["priv"]), 16)
    return(out)
def mk_sig(hash, priv): return list(b.ecdsa_raw_sign(hash, priv))
def mk_mk_sig(msghash): return (lambda p: mk_sig(msghash, p["priv"]))

expiration=1000
accs=map(mk_acc, [0, 1])
secret_hash=int(hash_list([27]), 16)
def test(c):
    h=hash_list([secret_hash, expiration])
    sig1=mk_sig(h, accs[0]["priv"])
    sig2=mk_sig(h, accs[1]["priv"])
    print("h: " +str(int(h, 16)))
    c.spend(secret_hash, accs[0]["addr"], accs[1]["addr"], sig1, sig2, expiration)
    c.reveal_claim(27, secret_hash)
    
def test_team(c):
    h=hash_list([secret_hash, expiration])
    sig1=mk_sig(h, accs[0]["priv"])
    sig2=mk_sig(h, accs[1]["priv"])
    c.spend(int(h, 16), accs[0]["addr"], accs[1]["addr"], expiration)
    sig1=mk_sig(h, accs[0]["priv"])
    sig2=mk_sig(h, accs[1]["priv"])
    c.team_claim(int(hash, 16), sig1, sig2, 0)
