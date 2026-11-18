#!/usr/bin/env python3
import os, struct, sys

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

path = sys.argv[1]
b = bytearray(open(path, "rb").read())
sc = u32(b, 52); oc = u32(b, 56); sss = u32(b, 60)
print("size:", len(b))
print("stringCount:", sc, "overflowCount:", oc, "storageSize:", sss)
print("fileLength:", u32(b, 32), "debugInfo:", u32(b, 104), "kinds:", u32(b, 44), "identifiers:", u32(b, 48))

T = 240636
print("hex @240600:", bytes(b[240600:240700]).hex())
print("hex @295560:", bytes(b[295560:295760]).hex())

bad = None
for k in range(sc):
    e = T + 8 * k
    a = u32(b, e); c = u32(b, e + 4)
    if a >= sss or a + c > sss:
        bad = k
        break
print("first implausible entry index:", bad, "of", sc)
print("first 24 pairs:")
for k in range(24):
    e = T + 8 * k
    print("  %d: %d %d" % (k, u32(b, e), u32(b, e + 4)))
print("last 6 pairs:")
for k in range(sc - 6, sc):
    e = T + 8 * k
    print("  %d: %d %d" % (k, u32(b, e), u32(b, e + 4)))
print("bytes just before T:", bytes(b[T - 48:T]).hex())
print("DONE")
