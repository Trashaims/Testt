#!/usr/bin/env python3
# Repoint the container's KOREA card from com.pubg.krmobile to com.pubg.imobile.
# Hermes storage is a bare concatenation; lengths live only in the string table,
# so shrinking means deleting bytes and shifting every offset after them.
import os, struct, sys

TARGET = b"com.pubg.krmobile"
REPL   = b"com.pubg.imobile"
DELTA  = len(TARGET) - len(REPL)
MAGIC  = bytes.fromhex("c61fbc03")

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

def u64(b, o):
    return struct.unpack_from("<Q", b, o)[0]

def storage_ok(b, S, T, sc, sss):
    """Entries must be cumulative from 0 and sum to storageSize exactly."""
    if S < 64 or S + sss > len(b):
        return False
    if u32(b, T) != 0:
        return False
    cur = 0
    for k in range(sc):
        e = T + 8 * k
        if u32(b, e) != cur:
            return False
        cur += u32(b, e + 4)
        if cur > sss:
            return False
    return cur == sss

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

    ver = u32(b, 8)
    sc = u32(b, 52)
    oc = u32(b, 56)
    sss = u32(b, 60)
    print("hermes version:", ver)
    print("stringCount:", sc, "overflowCount:", oc, "storageSize:", sss)
    if not (0 < sc < 2000000) or oc > 100000 or not (0 < sss < len(b)):
        sys.exit("FAIL: header fields not sane")

    cands = []
    for needle in (TARGET, REPL):
        c = b.find(needle)
        while c != -1:
            cands.append((c, needle))
            c = b.find(needle, c + 1)
    print("candidates:", len(cands))
    if not cands:
        sys.exit("FAIL: neither string present")

    hit = None
    for cand, needle in cands:
        for e in range(64, len(b) - 8, 4):
            if u32(b, e + 4) != len(needle):
                continue
            off = u32(b, e)
            S = cand - off
            if S < 64 or S > cand:
                continue
            for pad in range(0, 9):
                T = S - oc * 16 - sc * 8 - pad
                if T < 64 or (e - T) % 8:
                    continue
                if storage_ok(b, S, T, sc, sss):
                    hit = (cand, needle, S, e, T)
                    break
            if hit:
                break
        if hit:
            break

    if not hit:
        sys.exit("FAIL: no storage base validated")

    P, needle, S, E, T = hit
    off = P - S
    L = u32(b, E + 4)
    print("storage=%d offset=%d entry=%d table=%d len=%d" % (S, off, E, T, L))

    if L == len(REPL) and bytes(b[P:P + len(REPL)]) == REPL:
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
    if not storage_ok(b, S, T, sc, sss - DELTA):
        sys.exit("FAIL: table invariant broken")

    open(path, "wb").write(bytes(b))
    print("PASS, new size:", len(b))

main()
