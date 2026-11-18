.class public final Ltp/mu/k;
.super Ljava/lang/Object;
.source "k.java"


# static fields
.field static final KB:[I

.field static final KM:I = 0xcf

.field static final ON:[I

.field static final PN:[I

.field static final SM:I = 0xc2


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .line 13
    const/16 v0, 0x20

    new-array v0, v0, [I

    fill-array-data v0, :array_0

    sput-object v0, Ltp/mu/k;->KB:[I

    .line 22
    const/16 v0, 0x1b

    new-array v0, v0, [I

    fill-array-data v0, :array_1

    sput-object v0, Ltp/mu/k;->ON:[I

    .line 29
    const/16 v0, 0x13

    new-array v0, v0, [I

    fill-array-data v0, :array_2

    sput-object v0, Ltp/mu/k;->PN:[I

    return-void

    :array_0
    .array-data 4
        0x3b
        0x5d
        0x49
        0xe
        0x4b
        0x32
        0x22
        0x9a
        0xcf
        0x55
        0x55
        0xd
        0x8d
        0xdd
        0x2
        0x11
        0xdc
        0x6d
        0x99
        0x61
        0x34
        0xd4
        0x1c
        0xcf
        0xf4
        0x49
        0xf4
        0x82
        0x67
        0xc4
        0x5b
        0x51
    .end array-data

    :array_1
    .array-data 4
        0x264
        0x277
        0x1bb
        0x188
        0x196
        0x1b6
        0x1af
        0x1d5
        0x1c9
        0x1dd
        0x1bc
        0x1fd
        0x119
        0x119
        0x13b
        0x12b
        0x16a
        0x152
        0x146
        0x17a
        0x17f
        0x16c
        0x91
        0xc7
        0xb1
        0xa0
        0xa1
    .end array-data

    :array_2
    .array-data 4
        0x1d4
        0x1fb
        0x1fb
        0x1ab
        0x109
        0x103
        0x16c
        0x134
        0x12a
        0x14d
        0x148
        0x17b
        0x13f
        0x177
        0x86
        0x86
        0xa4
        0xaa
        0xa6
    .end array-data
.end method

.method private constructor <init>()V
    .locals 0

    .line 10
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static dec([B)Ljava/util/List;
    .locals 13
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "([B)",
            "Ljava/util/List<",
            "[B>;"
        }
    .end annotation

    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 73
    if-eqz p0, :cond_7

    array-length v0, p0

    const/16 v1, 0x18

    if-lt v0, v1, :cond_7

    .line 74
    const/4 v0, 0x0

    aget-byte v1, p0, v0

    const/16 v2, 0x5a

    if-ne v1, v2, :cond_6

    const/4 v1, 0x1

    aget-byte v3, p0, v1

    const/16 v4, 0x52

    if-ne v3, v4, :cond_6

    const/4 v3, 0x2

    aget-byte v5, p0, v3

    const/16 v6, 0x58

    if-ne v5, v6, :cond_6

    const/4 v5, 0x3

    aget-byte v7, p0, v5

    const/16 v8, 0x31

    if-ne v7, v8, :cond_6

    .line 77
    const/16 v7, 0x10

    new-array v8, v7, [B

    .line 78
    const/4 v9, 0x4

    invoke-static {p0, v9, v8, v0, v7}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    .line 79
    array-length v7, p0

    const/16 v10, 0x14

    sub-int/2addr v7, v10

    .line 80
    new-array v11, v7, [B

    .line 81
    invoke-static {p0, v10, v11, v0, v7}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    .line 82
    nop

    .line 83
    const-string p0, "AES/CTR/NoPadding"

    invoke-static {p0}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object p0

    .line 84
    new-instance v7, Ljavax/crypto/spec/SecretKeySpec;

    .line 85
    invoke-static {}, Ltp/mu/k;->key()[B

    move-result-object v10

    const-string v12, "AES"

    invoke-direct {v7, v10, v12}, Ljavax/crypto/spec/SecretKeySpec;-><init>([BLjava/lang/String;)V

    new-instance v10, Ljavax/crypto/spec/IvParameterSpec;

    invoke-direct {v10, v8}, Ljavax/crypto/spec/IvParameterSpec;-><init>([B)V

    .line 84
    invoke-virtual {p0, v3, v7, v10}, Ljavax/crypto/Cipher;->init(ILjava/security/Key;Ljava/security/spec/AlgorithmParameterSpec;)V

    .line 87
    invoke-virtual {p0, v11}, Ljavax/crypto/Cipher;->doFinal([B)[B

    move-result-object p0

    .line 88
    array-length v7, p0

    const/16 v8, 0x8

    if-lt v7, v8, :cond_5

    aget-byte v7, p0, v0

    if-ne v7, v2, :cond_5

    aget-byte v2, p0, v1

    if-ne v2, v4, :cond_5

    aget-byte v2, p0, v3

    if-ne v2, v6, :cond_5

    aget-byte v2, p0, v5

    const/16 v4, 0x44

    if-ne v2, v4, :cond_5

    .line 92
    invoke-static {p0, v9}, Ltp/mu/k;->rd32([BI)I

    move-result v2

    .line 93
    if-lt v2, v1, :cond_4

    const/16 v4, 0x40

    if-gt v2, v4, :cond_4

    .line 94
    new-instance v4, Ljava/util/ArrayList;

    invoke-direct {v4}, Ljava/util/ArrayList;-><init>()V

    .line 95
    nop

    .line 96
    move v6, v0

    move v7, v8

    :goto_0
    if-ge v6, v2, :cond_3

    .line 97
    add-int/lit8 v9, v7, 0x4

    array-length v10, p0

    if-gt v9, v10, :cond_2

    .line 98
    invoke-static {p0, v7}, Ltp/mu/k;->rd32([BI)I

    move-result v7

    .line 99
    nop

    .line 100
    if-lt v7, v8, :cond_1

    add-int v10, v9, v7

    array-length v11, p0

    if-gt v10, v11, :cond_1

    .line 101
    new-array v11, v7, [B

    .line 102
    invoke-static {p0, v9, v11, v0, v7}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    .line 103
    nop

    .line 105
    aget-byte v7, v11, v0

    const/16 v9, 0x64

    if-ne v7, v9, :cond_0

    aget-byte v7, v11, v1

    const/16 v9, 0x65

    if-ne v7, v9, :cond_0

    aget-byte v7, v11, v3

    const/16 v9, 0x78

    if-ne v7, v9, :cond_0

    aget-byte v7, v11, v5

    const/16 v9, 0xa

    if-ne v7, v9, :cond_0

    .line 109
    invoke-virtual {v4, v11}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 96
    add-int/lit8 v6, v6, 0x1

    move v7, v10

    goto :goto_0

    .line 107
    :cond_0
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad dex magic"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 100
    :cond_1
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad dex"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 97
    :cond_2
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad len"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 111
    :cond_3
    return-object v4

    .line 93
    :cond_4
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad count"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 90
    :cond_5
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad frame"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 75
    :cond_6
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad magic"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0

    .line 73
    :cond_7
    new-instance p0, Ljava/lang/Exception;

    const-string v0, "bad blob"

    invoke-direct {p0, v0}, Ljava/lang/Exception;-><init>(Ljava/lang/String;)V

    throw p0
.end method

.method public static key()[B
    .locals 5

    .line 38
    sget-object v0, Ltp/mu/k;->KB:[I

    .line 39
    array-length v1, v0

    new-array v1, v1, [B

    .line 40
    const/4 v2, 0x0

    :goto_0
    array-length v3, v0

    if-ge v2, v3, :cond_0

    .line 42
    array-length v3, v0

    add-int/lit8 v3, v3, -0x1

    sub-int/2addr v3, v2

    aget v3, v0, v3

    mul-int/lit8 v4, v2, 0x7

    add-int/lit16 v4, v4, 0xcf

    and-int/lit16 v4, v4, 0xff

    xor-int/2addr v3, v4

    int-to-byte v3, v3

    aput-byte v3, v1, v2

    .line 40
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 44
    :cond_0
    return-object v1
.end method

.method public static o()Ljava/lang/String;
    .locals 1

    .line 58
    sget-object v0, Ltp/mu/k;->ON:[I

    invoke-static {v0}, Ltp/mu/k;->s([I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static p()Ljava/lang/String;
    .locals 1

    .line 63
    sget-object v0, Ltp/mu/k;->PN:[I

    invoke-static {v0}, Ltp/mu/k;->s([I)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private static rd32([BI)I
    .locals 2

    .line 115
    aget-byte v0, p0, p1

    and-int/lit16 v0, v0, 0xff

    add-int/lit8 v1, p1, 0x1

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    shl-int/lit8 v1, v1, 0x8

    or-int/2addr v0, v1

    add-int/lit8 v1, p1, 0x2

    aget-byte v1, p0, v1

    and-int/lit16 v1, v1, 0xff

    shl-int/lit8 v1, v1, 0x10

    or-int/2addr v0, v1

    add-int/lit8 p1, p1, 0x3

    aget-byte p0, p0, p1

    and-int/lit16 p0, p0, 0xff

    shl-int/lit8 p0, p0, 0x18

    or-int/2addr p0, v0

    return p0
.end method

.method public static readAll(Ljava/io/InputStream;)[B
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/Exception;
        }
    .end annotation

    .line 121
    new-instance v0, Ljava/io/ByteArrayOutputStream;

    invoke-direct {v0}, Ljava/io/ByteArrayOutputStream;-><init>()V

    .line 122
    const/16 v1, 0x2000

    new-array v1, v1, [B

    .line 124
    :goto_0
    invoke-virtual {p0, v1}, Ljava/io/InputStream;->read([B)I

    move-result v2

    if-lez v2, :cond_0

    const/4 v3, 0x0

    invoke-virtual {v0, v1, v3, v2}, Ljava/io/ByteArrayOutputStream;->write([BII)V

    goto :goto_0

    .line 125
    :cond_0
    invoke-virtual {p0}, Ljava/io/InputStream;->close()V

    .line 126
    invoke-virtual {v0}, Ljava/io/ByteArrayOutputStream;->toByteArray()[B

    move-result-object p0

    return-object p0
.end method

.method public static s([I)Ljava/lang/String;
    .locals 5

    .line 49
    array-length v0, p0

    new-array v0, v0, [C

    .line 50
    const/4 v1, 0x0

    :goto_0
    array-length v2, p0

    if-ge v1, v2, :cond_0

    .line 51
    array-length v2, p0

    add-int/lit8 v2, v2, -0x1

    sub-int/2addr v2, v1

    aget v2, p0, v2

    mul-int/lit8 v3, v1, 0xd

    add-int/lit16 v3, v3, 0xc2

    const v4, 0xffff

    and-int/2addr v3, v4

    xor-int/2addr v2, v3

    int-to-char v2, v2

    aput-char v2, v0, v1

    .line 50
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 53
    :cond_0
    new-instance p0, Ljava/lang/String;

    invoke-direct {p0, v0}, Ljava/lang/String;-><init>([C)V

    return-object p0
.end method
