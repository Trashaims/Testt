#!/usr/bin/env python3
# Repoint the container's KOREA card from com.pubg.krmobile to com.pubg.imobile
# by rewriting the Hermes string table entry with full offset fixup.
# Handles both a pristine bundle and one already damaged by a naive byte replace.
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

def score(b, s, entries):
    ok = 0
    for off, ln in entries:
        try:
            if s + off + 1 > len(b):
                continue
            if read_uleb(b, s + off) != ln:
                continue
            if ln and b[s + off + ln] not in (0, 1):
                continue
            ok += 1
        except Exception:
            pass
    return ok, len(entries)

def locate(b, sc, oc):
    """Return (P, S, T, E) for the first string that decodes to TARGET or REPL."""
    for needle in (TARGET, REPL):
        cand = b.find(needle)
        while cand != -1:
            for p in (1, 4, 0):
                if p and b[cand - p:cand] != (uleb(len(needle)) if p == 1 else struct.pack("<I", len(needle))):
                    continue
                for e in range(64, len(b) - 8, 4):
                    if u32(b, e + 4) != len(needle):
                        continue
                    off = u32(b, e)
                    s = cand - off - p
                    if s < 0 or s > cand:
                        continue
                    for pad in range(0, 9):
                        t = s - oc * 16 - sc * 8 - pad
                        if t < 64 or not (t <= e < t + sc * 8):
                            continue
                        stride = max(1, sc // 400)
                        entries = [(u32(b, t + 8 * k), u32(b, t + 8 * k + 4))
                                   for k in range(0, sc, stride)]
                        ok, tot = score(b, s, entries)
                        if tot and ok >= tot * 0.95:
                            return cand, s, t, e, p
            cand = b.find(needle, cand + 1)
    return None

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

    print("hermes version:", u32(b, 8))
    sc = u32(b, 52)
    oc = u32(b, 56)
    sss = u32(b, 60)
    print("stringCount:", sc, "overflowCount:", oc, "storageSize:", sss)
    if not (0 < sc < 2000000) or oc > 100000 or sss > len(b):
        sys.exit("FAIL: header offsets do not look sane")

    found = locate(b, sc, oc)
    if not found:
        sys.exit("FAIL: could not locate the string table entry")
    P, S, T, E, p = found
    off = P - S - p
    print("entry @%d off=%d prefix=%d storage=%d table=%d" % (E, off, p, S, T))

    L = u32(b, E + 4)
    lenbyte = uleb(len(REPL)) if p == 1 else (struct.pack("<I", len(REPL)) if p == 4 else b"")
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
        # naive replace already shrank the file; only the length byte and the
        # offset table are stale. No bytes to delete.
        print("state: naive replace, repairing table")
        b[P - p:P] = lenbyte
        struct.pack_into("<I", b, E + 4, len(REPL))
        fixup()
    else:
        flag = b[P + len(TARGET)]
        print("state: pristine, rewriting entry")
        b[P - p:P + len(TARGET) + 1] = lenbyte + REPL + bytes([flag])
        struct.pack_into("<I", b, E + 4, len(REPL))
        fixup()

    if b.count(TARGET):
        sys.exit("FAIL: target still present")
    q = b.find(REPL)
    if q == -1 or read_uleb(b, q - p) != len(REPL):
        sys.exit("FAIL: replacement not readable")
    if u32(b, 32) != len(b):
        sys.exit("FAIL: fileLength mismatch")

    stride = max(1, sc // 400)
    entries = [(u32(b, T + 8 * k), u32(b, T + 8 * k + 4)) for k in range(0, sc, stride)]
    ok, tot = score(b, S, entries)
    print("post-check %d/%d entries valid" % (ok, tot))
    if ok < tot * 0.95:
        sys.exit("FAIL: table corrupted")

    open(path, "wb").write(bytes(b))
    print("PASS, new size:", len(b))

main()
