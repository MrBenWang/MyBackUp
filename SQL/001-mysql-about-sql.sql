-- 查询表字段
SELECT 
    TABLE_NAME, COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, IS_NULLABLE, COLUMN_COMMENT
FROM 
    information_schema.COLUMNS
WHERE 
    TABLE_SCHEMA = '数据库名' AND COLUMN_NAME LIKE '%type%'


-- 查询mysql 执行的语句
SHOW VARIABLES LIKE "general_log%";
-- # Variable_name, Value
-- general_log, OFF
-- general_log_file, CNPC0231-CD.log

-- 启用日志记录功能，需要提前创建 mysql.log 这个空文件
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = 'c:/mysql.log';

-- BareTail 查看日志的工具
http://www.baremetalsoft.com/baretail/

