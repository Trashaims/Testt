.class public Lcom/pubg/krmobile/Main;
.super Landroid/app/Activity;
.source "Main.java"

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    :try_start
    invoke-virtual {p0}, Landroid/app/Activity;->getPackageManager()Landroid/content/pm/PackageManager;
    move-result-object v0
    const-string v1, "com.pubg.imobile"
    invoke-virtual {v0, v1}, Landroid/content/pm/PackageManager;->getLaunchIntentForPackage(Ljava/lang/String;)Landroid/content/Intent;
    move-result-object v2
    if-nez v2, :try_end
    const/high16 v3, 0x10000000
    invoke-virtual {v2, v3}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
    invoke-virtual {p0, v2}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end
    goto :done
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :catch

    :catch
    move-exception v0

    :done
    invoke-virtual {p0}, Landroid/app/Activity;->finish()V
    return-void
.end method
