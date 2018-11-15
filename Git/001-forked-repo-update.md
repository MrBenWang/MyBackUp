# 从 Forked 的仓库，更新代码

1. git remote -v  // 查询远程仓库信息  

``` git
$ git remote -v
origin  https://github.com/MrBenWang/hugo-theme-jane.git (fetch)
origin  https://github.com/MrBenWang/hugo-theme-jane.git (push)
update_git       https://github.com/xianmin/hugo-theme-jane.git (fetch)
update_git       https://github.com/xianmin/hugo-theme-jane.git (push)
```

2. git remote add update_git git@github.com:xxx/xxx.git  // 添加远程仓库 链接，名为 update_git  

3. git fetch update_git  // 从原仓库更新同步代码  

``` git
$ git fetch update_git
remote: Enumerating objects: 544, done.
remote: Counting objects: 100% (544/544), done.
remote: Compressing objects: 100% (228/228), done.
remote: Total 544 (delta 279), reused 513 (delta 253), pack-reused 0
Receiving objects: 100% (544/544), 268.26 KiB | 271.00 KiB/s, done.
Resolving deltas: 100% (279/279), completed with 18 local objects.
From https://github.com/xianmin/hugo-theme-jane
   250c0bc..b4a0105  develop        -> update_git/develop
   a6bd217..df6f51d  gh-pages       -> update_git/gh-pages
   b10f58e..20ffe4e  master         -> update_git/master
 * [new branch]      use-hugo-pipes -> update_git/use-hugo-pipes
 * [new tag]         2.0.0          -> 2.0.0
```

4. git merge update_git/master  // 合并代码，遇到冲突 自己处理  
