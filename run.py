#!/usr/bin/env python
import sys
from pyethereum import tester as t
s=t.state()
c=s.abi_contract(sys.argv[1]+".se")
test=__import__(sys.argv[1]+"_test")
print(test.test(c))
