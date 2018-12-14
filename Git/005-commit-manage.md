# 管理相关的 提交

## 删除指定的 COMMIT

1. git log              ：找到要删除的提交 Id ( 简写为 Id-a) 之前一次 提交的 Id (简写为 Id-b)；
2. git rebase -i  Id-b  ：表示回退到之前的版本，并在之后会提交需要的所有提交。
3. 删除要删除的提交（skip 变成 drop 或者 删除想要删除的那一行），并保存退出。需要用到linux编辑器命令`:wq`
4. git push origin master --force   ：如果不强制更新，把提交的commit 继续拉下来。