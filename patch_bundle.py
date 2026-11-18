#!/usr/bin/env python3
# Repoint the container's KOREA card from com.pubg.krmobile to com.pubg.imobile.
import os, struct, sys

TARGET = b"com.pubg.krmobile"
REPL   = b"com.pubg.imobile"
DELTA  = len(TARGET) - len(REPL)
MAGIC  = bytes.fromhex("c61fbc03")

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

def u64(b, o):
    return struct.unpack_from("<Q", b, o)[0]

def plausible(b, p, sss):
    a = u32(b, p)
    c = u32(b, p + 4)
    return a < sss and 0 < c <= sss and a + c <= sss

def find_tables(b, sss):
    out = []
    pos = 64
    while pos + 8 * 33 <= len(b):
        if plausible(b, pos, sss) and not (pos >= 4 and plausible(b, pos - 4, sss)):
            k = 1
            while k < 32 and plausible(b, pos + 8 * k, sss):
                k += 1
            if k >= 32:
                out.append(pos)
        pos += 4
    return out

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: patch_bundle.py <bundle>")
    path = sys.argv[1]
    if not os.path.exists(path):
        sys.exit("FAIL: %s missing" % path)

    b = bytearray(open(path, "rb").read())
    print("size:", len(b))
    print("magic:", bytes(b[:8]).hex())

    if bytes(b[:4]) != MAGIC:
        print("unknown magic, plain replace")
        n = b.count(TARGET)
        print("occurrences:", n)
        if not n:
            sys.exit("FAIL: target string absent")
        open(path, "wb").write(bytes(b).replace(TARGET, REPL))
        print("PASS plain replace")
        return

    sc = u32(b, 52)
    oc = u32(b, 56)
    sss = u32(b, 60)
    print("stringCount:", sc, "overflowCount:", oc, "storageSize:", sss)
    if not (0 < sc < 2000000) or oc > 100000 or not (0 < sss < len(b)):
        sys.exit("FAIL: header fields not sane")

    tables = find_tables(b, sss)
    print("table candidates:", len(tables), tables[:8])
    if not tables:
        sys.exit("FAIL: no table found")

    hit = None
    for T in tables:
        for S in (T - sss, T + sc * 8 + oc * 16):
            if S < 64 or S + sss > len(b):
                continue
            for needle in (TARGET, REPL):
                cand = b.find(needle)
                while cand != -1:
                    off = cand - S
                    if 0 <= off and off + len(needle) <= sss:
                        for k in range(sc):
                            e = T + 8 * k
                            if u32(b, e) == off and u32(b, e + 4) == len(needle):
                                if bytes(b[cand:cand + len(needle)]) == needle:
                                    hit = (cand, needle, S, e, T, off)
                                    break
                    if hit:
                        break
                    cand = b.find(needle, cand + 1)
                if hit:
                    break
            if hit:
                break
        if hit:
            break

    if not hit:
        print("FAIL: no anchor matched")
        for T in tables[:8]:
            print("  T=%d S=%d" % (T, T - sss))
        sys.exit(1)

    P, needle, S, E, T, off = hit
    L = u32(b, E + 4)
    print("table=%d storage=%d offset=%d entry=%d len=%d" % (T, S, off, E, L))

    if L == len(REPL) and needle == REPL:
        print("state: already correct")
        print("PASS, size:", len(b))
        return
    if L != len(TARGET):
        sys.exit("FAIL: unexpected entry length %d" % L)

    b[P:P + len(REPL)] = REPL
    del b[P + len(REPL):P + len(TARGET)]
    struct.pack_into("<I", b, E + 4, len(REPL))

    for k in range(sc):
        e = T + 8 * k
        o = u32(b, e)
        if o > off:
            struct.pack_into("<I", b, e, o - DELTA)
    for k in range(oc):
        e = T + sc * 8 + 16 * k
        o = u64(b, e)
        if o > off:
            struct.pack_into("<Q", b, e, o - DELTA)
    struct.pack_into("<I", b, 60, sss - DELTA)
    d = u32(b, 104)
    if d > P:
        struct.pack_into("<I", b, 104, d - DELTA)
    struct.pack_into("<I", b, 32, len(b))

    if b.count(TARGET):
        sys.exit("FAIL: target still present")
    if u32(b, 32) != len(b):
        sys.exit("FAIL: fileLength mismatch")

    q = b.find(REPL)
    if q == -1 or u32(b, 32) != len(b):
        sys.exit("FAIL: replacement missing")

    open(path, "wb").write(bytes(b))
    print("PASS, new size:", len(b))

main()
