# 一些fb的bug

- Firebird升级脚本包含多个sql，的bug

```sql
ALTER TABLE "MyTable" ADD "foo" int default null;
ALTER TABLE "MyTable" ADD "bar" int default null;
```

在同一个sql里面执行上面两句的时候，会出现bug。
It seems that FirebirdConnectionManager.cs has a regular expression which is not splitting the script correctly:https://github.com/DbUp/DbUp/issues/159

- FireBird 在vs的插件 FirebirdClient Data Provider 问题。

在下面两个路径里面，存在多个相同的 FirebirdClient 节点
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\machine.config
C:\Windows\Microsoft.NET\Framework\v4.0.30319\Config\machine.config