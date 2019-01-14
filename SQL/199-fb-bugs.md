# 一些fb的bug

- Firebird升级脚本包含多个sql，的bug

```sql
ALTER TABLE "MyTable" ADD "foo" int default null;
ALTER TABLE "MyTable" ADD "bar" int default null;
```

在同一个sql里面执行上面两句的时候，会出现bug。
It seems that FirebirdConnectionManager.cs has a regular expression which is not splitting the script correctly:https://github.com/DbUp/DbUp/issues/159