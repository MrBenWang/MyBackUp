-- 101-fb-count-all-tables-rows

SET term !! ;
EXECUTE BLOCK 
RETURNS ( stm VARCHAR(120), cnt INTEGER )
AS
BEGIN
    FOR 
        SELECT CAST('select count(*) from "'||TRIM(my_sys.RDB$RELATION_NAME)||'"' AS VARCHAR(120))
        FROM RDB$RELATIONS AS my_sys
        WHERE (my_sys.RDB$SYSTEM_FLAG IS NULL OR my_sys.RDB$SYSTEM_FLAG = 0) AND my_sys.RDB$VIEW_BLR IS NULL
        ORDER BY 1
    INTO :stm
    DO
    BEGIN
        EXECUTE STATEMENT :stm INTO :cnt;
        SUSPEND;
    END
END

-- 获取所有表的，以及表的字段
SELECT 
    a.RDB$RELATION_NAME,
    b.RDB$FIELD_NAME,
    b.RDB$FIELD_ID,
    d.RDB$TYPE_NAME,
    c.RDB$FIELD_LENGTH,
    c.RDB$FIELD_SCALE
FROM RDB$RELATIONS AS a
    INNER JOIN RDB$RELATION_FIELDS AS b ON a.RDB$RELATION_NAME = b.RDB$RELATION_NAME
    INNER JOIN RDB$FIELDS AS c ON b.RDB$FIELD_SOURCE = c.RDB$FIELD_NAME
    INNER JOIN RDB$TYPES AS d ON c.RDB$FIELD_TYPE = d.RDB$TYPE
WHERE a.RDB$SYSTEM_FLAG = 0
    AND d.RDB$FIELD_NAME = 'RDB$FIELD_TYPE'
ORDER BY a.RDB$RELATION_NAME, b.RDB$FIELD_ID;

--查询所有的用户表
SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0 AND RDB$VIEW_BLR IS NULL;

-- 103-fb-show-fb-verson
select rdb$get_context('SYSTEM','ENGINE_VERSION') as "version" from RDB$DATABASE;