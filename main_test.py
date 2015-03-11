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

def test(c):
    accs=map(mk_acc, [0, 1])
    hash=hash_list([27])
    c.spend(int(hash, 16), accs[0]["addr"], accs[1]["addr"], 1000)
    c.reveal_claim(accs[0]["addr"], accs[1]["addr"], 27)
    
def test_team(c):
    accs=map(mk_acc, [0, 1])
    hash=hash_list([27])
    c.spend(utils.big_endian_to_int(hash), accs[0]["addr"], accs[1]["addr"], 1000)
    sig1=mk_sig(hash, accs[0]["priv"])
    sig2=mk_sig(hash, accs[1]["priv"])
    c.team_claim(accs[0]["addr"], accs[1]["addr"], sig1, sig2, 0)
