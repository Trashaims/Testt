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

def find_tables(b, sss, sc):
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
    return [t for t in out if t + 8 * sc <= len(b)]

def looks_like_text(b, S, off, ln):
    s = b[S + off:S + off + ln]
    if len(s) != ln:
        return False
    if all(0x20 <= c <= 0x7E for c in s):
        return True
    if ln >= 4 and ln % 2 == 0 and all(s[i] == 0 for i in range(1, ln, 2)):
        return True
    return False

def sample_ok(b, S, T, sc, sss, step):
    good = tot = 0
    for k in range(0, sc, step):
        e = T + 8 * k
        off = u32(b, e)
        ln = u32(b, e + 4)
        if ln == 0 or off + ln > sss:
            continue
        tot += 1
        if looks_like_text(b, S, off, ln):
            good += 1
    return good, tot

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

    tables = find_tables(b, sss, sc)
    print("table candidates:", len(tables), tables[:8])
    if not tables:
        sys.exit("FAIL: no table found")

    hit = None
    near = []
    for T in tables:
        for pad in range(0, 25):
            S = T - sss - pad
            if S < 64 or S + sss > len(b):
                continue
            good, tot = sample_ok(b, S, T, sc, sss, max(1, sc // 60))
            if tot < 10 or good < tot * 0.6:
                continue
            for k in range(sc):
                e = T + 8 * k
                off = u32(b, e)
                ln = u32(b, e + 4)
                if ln < len(TARGET) or off + len(TARGET) > sss:
                    continue
                if bytes(b[S + off:S + off + len(TARGET)]) == TARGET:
                    hit = (S + off, S, e, T, off, ln)
                    break
            if len(near) < 6:
                near.append((T, pad, S, good, tot))
            if hit:
                break
        if hit:
            break

    if not hit:
        print("FAIL: no string entry matched by content")
        for T, pad, S, good, tot in near:
            print("  T=%d pad=%d S=%d text=%d/%d" % (T, pad, S, good, tot))
        for T in tables[:2]:
            S = T - sss
            for k in range(0, sc, 4):
                e = T + 8 * k
                off = u32(b, e)
                if 91500 <= off <= 92100:
                    ln = u32(b, e + 4)
                    print("  near off=%d len=%d -> %r" % (off, ln, bytes(b[S + off:S + off + min(ln, 40)])))
        sys.exit(1)

    P, S, E, T, off, L = hit
    print("table=%d storage=%d offset=%d entry=%d len=%d" % (T, S, off, E, L))

    if L == len(REPL):
        print("state: already correct")
        print("PASS, size:", len(b))
        return

    b[P:P + len(REPL)] = REPL
    del b[P + len(REPL):P + len(TARGET)]
    struct.pack_into("<I", b, E + 4, L - DELTA)

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

    open(path, "wb").write(bytes(b))
    print("PASS, new size:", len(b))

main()
