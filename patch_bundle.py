#!/usr/bin/env python3
# Repoint the container's KOREA card from com.pubg.krmobile to com.pubg.imobile
# by rewriting the Hermes string table entry with full offset fixup.
import os, struct, sys

TARGET = b"com.pubg.krmobile"
REPL   = b"com.pubg.imobile"
DELTA  = len(TARGET) - len(REPL)
MAGIC  = bytes.fromhex("c61fbc03")

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

def u64(b, o):
    return struct.unpack_from("<Q", b, o)[0]

def read_uleb(b, o):
    v = 0; s = 0
    for _ in range(5):
        byte = b[o]
        v |= (byte & 0x7F) << s
        o += 1; s += 7
        if not byte & 0x80:
            return v
    raise ValueError("uleb too long")

def uleb(v):
    out = bytearray()
    while True:
        byte = v & 0x7F
        v >>= 7
        if v:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)

def decode_ok(b, S, sc, sss):
    """True only if [S, S+sss) decodes as exactly sc uleb-prefixed strings."""
    if S < 64 or S + sss > len(b):
        return False
    pos = S
    end = S + sss
    n = 0
    while pos < end:
        try:
            L = read_uleb(b, pos)
        except Exception:
            return False
        pos += len(uleb(L))
        if pos + L + 1 > end:
            return False
        pos += L
        if b[pos] not in (0, 1):
            return False
        pos += 1
        n += 1
        if n > sc:
            return False
    return n == sc and pos == end

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
        for p in (1, 4, 0):
            pre = uleb(len(needle)) if p == 1 else (struct.pack("<I", len(needle)) if p == 4 else b"")
            if pre and b[cand - p:cand] != pre:
                continue
            for e in range(64, len(b) - 8, 4):
                if u32(b, e + 4) != len(needle):
                    continue
                off = u32(b, e)
                S = cand - off - p
                if not decode_ok(b, S, sc, sss):
                    continue
                hit = (cand, needle, p, S, e)
                break
            if hit:
                break
        if hit:
            break

    if not hit:
        print("FAIL: no storage base validated")
        for cand, needle in cands[:4]:
            print("  @%d %r -> %s" % (cand, needle, bytes(b[cand - 8:cand + 26]).hex()))
        sys.exit(1)

    P, needle, p, S, _ = hit
    off = P - S - p
    print("storage=%d prefix=%d offset=%d" % (S, p, off))

    E = None
    for e in range(S - oc * 16 - sc * 8 - 16, S, 4):
        if e >= 64 and u32(b, e) == off and u32(b, e + 4) == len(needle):
            E = e
            break
    if E is None:
        sys.exit("FAIL: entry with offset %d not found in table" % off)
    T = S - oc * 16 - sc * 8
    while T > 64 and (E - T) % 8:
        T -= 1
    print("entry=%d table=%d" % (E, T))

    lenbyte = uleb(len(REPL)) if p == 1 else (struct.pack("<I", len(REPL)) if p == 4 else b"")
    L = u32(b, E + 4)
    print("entry length:", L)

    def fixup():
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
        struct.pack_into("<I", b, 60, u32(b, 60) - DELTA)
        d = u32(b, 104)
        if d > P:
            struct.pack_into("<I", b, 104, d - DELTA)
        struct.pack_into("<I", b, 32, len(b))

    if L == len(REPL) and b[P + len(REPL)] in (0, 1):
        print("state: already correct")
    elif L == len(TARGET) and b[P + len(REPL)] in (0, 1):
        print("state: length stale, repairing")
        b[P - p:P] = lenbyte
        struct.pack_into("<I", b, E + 4, len(REPL))
        fixup()
    else:
        flag = b[P + len(TARGET)]
        print("state: pristine, rewriting")
        b[P - p:P + len(TARGET) + 1] = lenbyte + REPL + bytes([flag])
        struct.pack_into("<I", b, E + 4, len(REPL))
        fixup()

    if b.count(TARGET):
        sys.exit("FAIL: target still present")
    q = b.find(REPL)
    if q == -1 or read_uleb(b, q - p) != len(REPL):
        sys.exit("FAIL: replacement unreadable")
    if u32(b, 32) != len(b):
        sys.exit("FAIL: fileLength mismatch")
    if not decode_ok(b, S, sc, sss):
        sys.exit("FAIL: storage no longer decodes")

    open(path, "wb").write(bytes(b))
    print("PASS, new size:", len(b))

main()
