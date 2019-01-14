

SELECT 
1 AS "C1", 
"D"."plugin_key" AS "plugin_key", 
"D"."plugin_name" AS "plugin_name"
FROM  "privgroup_plugin" AS "C"
LEFT OUTER JOIN "plugin_info" AS "D" ON "C"."plugin_id" = "D"."id"
WHERE "C"."privgroup_id" = @p__linq__0
```Linq
var _qry = context.privgroup_plugin
                .GroupJoin(context.plugin_info, a => a.plugin_id, b => b.id, (a, b) => new { a, b })
                .Where(m => m.a.privgroup_id == localUser.priv_group.Value)
                .SelectMany(
                    temp => temp.b.DefaultIfEmpty(),
                    (temp, p) =>
                    new PluginInfoModel
                    {
                        PluginKey = p.plugin_key,
                        PluginName = p.plugin_name
                    });
```