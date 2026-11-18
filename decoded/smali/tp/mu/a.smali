.class public Ltp/mu/a;
.super Landroid/app/Application;
.source "a.java"


# instance fields
.field private o:Landroid/app/Application;


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 13
    invoke-direct {p0}, Landroid/app/Application;-><init>()V

    return-void
.end method


# virtual methods
.method protected attachBaseContext(Landroid/content/Context;)V
    .locals 7

    .line 18
    invoke-super {p0, p1}, Landroid/app/Application;->attachBaseContext(Landroid/content/Context;)V

    .line 20
    :try_start_0
    invoke-virtual {p0}, Ltp/mu/a;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v0

    .line 21
    invoke-static {p0, v0}, Ltp/mu/b;->e(Landroid/content/Context;Ljava/lang/ClassLoader;)Ljava/lang/ClassLoader;

    move-result-object v0

    .line 22
    invoke-static {}, Ltp/mu/k;->o()Ljava/lang/String;

    move-result-object v1

    .line 23
    if-eqz v1, :cond_1

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v2

    if-nez v2, :cond_0

    goto :goto_0

    .line 28
    :cond_0
    const/4 v2, 0x1

    invoke-static {v1, v2, v0}, Ljava/lang/Class;->forName(Ljava/lang/String;ZLjava/lang/ClassLoader;)Ljava/lang/Class;

    move-result-object v0

    .line 29
    invoke-virtual {v0}, Ljava/lang/Class;->newInstance()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/app/Application;

    .line 31
    const-class v1, Landroid/app/Application;

    const-string v3, "attach"

    new-array v4, v2, [Ljava/lang/Class;

    const-class v5, Landroid/content/Context;

    const/4 v6, 0x0

    aput-object v5, v4, v6

    .line 32
    invoke-virtual {v1, v3, v4}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v1

    .line 33
    invoke-virtual {v1, v2}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 34
    filled-new-array {p1}, [Ljava/lang/Object;

    move-result-object p1

    invoke-virtual {v1, v0, p1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    .line 35
    iput-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 39
    nop

    .line 40
    return-void

    .line 26
    :cond_1
    :goto_0
    return-void

    .line 36
    :catchall_0
    move-exception p1

    .line 37
    const-string v0, "zr"

    const-string v1, "payload init failed"

    invoke-static {v0, v1, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 38
    new-instance v0, Ljava/lang/RuntimeException;

    invoke-direct {v0, p1}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/Throwable;)V

    throw v0
.end method

.method public onConfigurationChanged(Landroid/content/res/Configuration;)V
    .locals 1

    .line 84
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    if-eqz v0, :cond_0

    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-virtual {v0, p1}, Landroid/app/Application;->onConfigurationChanged(Landroid/content/res/Configuration;)V

    goto :goto_0

    .line 85
    :cond_0
    invoke-super {p0, p1}, Landroid/app/Application;->onConfigurationChanged(Landroid/content/res/Configuration;)V

    .line 86
    :goto_0
    return-void
.end method

.method public onCreate()V
    .locals 4

    .line 44
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    if-nez v0, :cond_0

    .line 45
    invoke-super {p0}, Landroid/app/Application;->onCreate()V

    .line 46
    return-void

    .line 49
    :cond_0
    :try_start_0
    invoke-virtual {p0}, Ltp/mu/a;->getBaseContext()Landroid/content/Context;

    move-result-object v0

    const-string v1, "mPackageInfo"

    invoke-static {v0, v1}, Ltp/mu/b;->g(Ljava/lang/Object;Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v0

    .line 50
    if-eqz v0, :cond_1

    .line 51
    const-string v1, "mApplication"

    iget-object v2, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-static {v0, v1, v2}, Ltp/mu/b;->s(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;)V

    .line 53
    :cond_1
    const-string v0, "android.app.ActivityThread"

    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 54
    const-string v1, "currentActivityThread"

    const/4 v2, 0x0

    new-array v3, v2, [Ljava/lang/Class;

    invoke-virtual {v0, v1, v3}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    new-array v1, v2, [Ljava/lang/Object;

    const/4 v2, 0x0

    invoke-virtual {v0, v2, v1}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    .line 55
    if-eqz v0, :cond_2

    .line 56
    const-string v1, "mInitialApplication"

    iget-object v2, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-static {v0, v1, v2}, Ltp/mu/b;->s(Ljava/lang/Object;Ljava/lang/String;Ljava/lang/Object;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    .line 60
    :cond_2
    goto :goto_0

    .line 58
    :catchall_0
    move-exception v0

    .line 59
    const-string v1, "zr"

    const-string v2, "app swap skipped"

    invoke-static {v1, v2, v0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    .line 61
    :goto_0
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->onCreate()V

    .line 62
    return-void
.end method

.method public onLowMemory()V
    .locals 1

    .line 72
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    if-eqz v0, :cond_0

    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->onLowMemory()V

    goto :goto_0

    .line 73
    :cond_0
    invoke-super {p0}, Landroid/app/Application;->onLowMemory()V

    .line 74
    :goto_0
    return-void
.end method

.method public onTerminate()V
    .locals 1

    .line 66
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    if-eqz v0, :cond_0

    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->onTerminate()V

    goto :goto_0

    .line 67
    :cond_0
    invoke-super {p0}, Landroid/app/Application;->onTerminate()V

    .line 68
    :goto_0
    return-void
.end method

.method public onTrimMemory(I)V
    .locals 1

    .line 78
    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    if-eqz v0, :cond_0

    iget-object v0, p0, Ltp/mu/a;->o:Landroid/app/Application;

    invoke-virtual {v0, p1}, Landroid/app/Application;->onTrimMemory(I)V

    goto :goto_0

    .line 79
    :cond_0
    invoke-super {p0, p1}, Landroid/app/Application;->onTrimMemory(I)V

    .line 80
    :goto_0
    return-void
.end method
