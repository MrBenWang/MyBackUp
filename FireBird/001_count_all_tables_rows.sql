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
