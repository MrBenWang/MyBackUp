mysql 5.6 生成 EFModel 的时候出错，是由于版本的问题。升级高版本即可，或者执行下面的语句：


set GLOBAL optimizer_switch='derived_merge=on'
'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on'

-- mysql 编码格式的替换
utf8mb4_0900_ai_ci 替换为 utf8_general_ci
utf8mb4 替换为 utf8

