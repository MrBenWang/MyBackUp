# 分支管理

## 查看分支

1. git branch -r    # 查看所有远程分支
2. git branch -a    # 查看远程和本地所有分支
3. git branch       # 查看本地分支, 带* 的是当前分支
4. git branch -vv   # 查看本地分支和远程分支的映射关系

## 操作分支

1. git branch iss53     # 创建分支 iss53
2. git checkout iss53   # 切换到分支 iss53
3. git checkout -b iss53                # 等于 1 和 2 的操作
4. git branch -d iss53  # 删除分支 iss53
5. git branch --set-upstream-to origin/远程分支名  本地分支名   # 本地分支关联到远程分支

## 合并分支

1. git merge iss53      # 合并 iss53 分支 到 当前分支🦃

    ``` git  
    $ git checkout master
    Switched to branch 'master'
    $ git merge iss53
    Merge made by the 'recursive' strategy.
    index.html |    1 +
    1 file changed, 1 insertion(+)
    ```

2. git cherry-pick commitid     # '挑拣'提交，获取某一个分支的单笔提交，并作为一个新的提交引入到你当前分支上
    - git cherry-pick -n commitid  # 不自动合并，只把修改添加
    - git cherry-pick -e commitid  # 重新编辑提交信息

    ``` git
    $ git checkout branch2
    Switched to branch 'branch2'
    $ git log --oneline -3
    23d9422 [Description]:branch2 commit 3
    2555c6e [Description]:branch2 commit 2
    b82ba0f [Description]:branch2 commit 1
    $ git checkout branch1
    Switched to branch 'branch1'
    $ git log --oneline -3
    20fe2f9 commit second
    c51adbe commit first
    ae2bd14 commit 3th
    # 把 branch2 的 2555c6e 提交，合并到 branch1 上。 存在冲突需要自己解决，没有则自动提交。
    $ git cherry-pick 2555c6e
    error: could not apply 2555c6e... [Description]:branch2 commit 2
    hint: after resolving the conflicts, mark the corrected paths
    hint: with 'git add <paths>' or 'git rm <paths>'
    hint: and commit the result with 'git commit'

    ```