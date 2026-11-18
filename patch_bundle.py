#!/usr/bin/env python3
import os, struct, sys

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

path = sys.argv[1]
b = bytearray(open(path, "rb").read())
sc = u32(b, 52); oc = u32(b, 56); sss = u32(b, 60)
print("size:", len(b), "sc:", sc, "oc:", oc, "sss:", sss)
print("kinds:", u32(b, 44), "identifiers:", u32(b, 48))

for T in (240636, 258780):
    for pad in range(0, 17):
        S = T - sss - pad
        if S < 64 or S + sss > len(b):
            continue
        n = 0
        for k in range(sc):
            e = T + 8 * k
            off = u32(b, e)
            ln = u32(b, e + 4)
            if off + 8 > sss or ln < 8:
                continue
            if bytes(b[S + off:S + off + 8]) == b"com.pubg":
                print("T=%d pad=%d k=%d off=%d len=%d str=%r" % (T, pad, k, off, ln, bytes(b[S + off:S + off + min(ln, 40)])))
                n += 1
                if n >= 6:
                    break
        print("  pad %d done, hits %d" % (pad, n))
        if n:
            break
print("DONE")
