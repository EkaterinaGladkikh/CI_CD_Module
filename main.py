import pymssql
import pytest
import variables


conn = pymssql.connect(
    server=variables.server,
    user=variables.username,
    password=variables.password,
    database=variables.database_name,
    port=variables.port
    as_dict=False
)


class TestDB:
    @pytest.mark.parametrize("table", ['Person.Address', 'Production.Document', '[Production].[UnitMeasure]'])
    def test_count_rows(self, table):
        count_dict = {'Person.Address': 19614, 'Production.Document': 13, '[Production].[UnitMeasure]': 38}
        sql_query = f"""
        SELECT
            COUNT(*) AS count_number
        FROM 
        AdventureWorks2012.{table} AS a;
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()

        assert list(records)[0][0] == count_dict[table], f'The count of rows in {table} is not correct'

    def test_column_is_fk(self):
        sql_query = f"""
        SELECT kc.COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc 
        INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kc
            ON tc.CONSTRAINT_NAME = kc.CONSTRAINT_NAME
        WHERE tc.TABLE_SCHEMA = 'Person'
            AND tc.TABLE_NAME = 'Address'
            AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY';
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()

        assert list(records)[0][0] == 'StateProvinceID', 'The FK of the Person.Address table is not correct'

    def test_column_values_not_empty(self):
        sql_query = f"""
        SELECT 
            [UnitMeasureCode]
            ,[Name]
        FROM [AdventureWorks2012].[Production].[UnitMeasure]
        WHERE [UnitMeasureCode] = '';
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()

        assert len(records) == 0, '[UnitMeasure].[UnitMeasureCode] column contains empty values ("")'

    def test_column_datatypes(self):
        exp_result = [['UnitMeasureCode', 'nchar(3)'], ['Name', 'nvarchar(50)'], ['ModifiedDate', 'datetime']]
        sql_query = f"""
        SELECT
            [COLUMN_NAME]												AS "Column name"
            ,CONCAT([DATA_TYPE],
                IIF([CHARACTER_MAXIMUM_LENGTH] IS NULL, NULL,
                    CONCAT('(', [CHARACTER_MAXIMUM_LENGTH] ,')')))      AS "Data type"
        FROM [INFORMATION_SCHEMA].[COLUMNS]
        WHERE [TABLE_SCHEMA] = 'Production'
            AND [TABLE_NAME] = 'UnitMeasure';
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()
        records = [list(rows) for rows in records]

        assert records == exp_result, 'The columns in the [Production].[UnitMeasure] table have the wrong datatypes'

    def test_column_values_in_range(self):
        sql_query = f"""
        SELECT
            [DocumentNode]
        FROM [AdventureWorks2012].[Production].[Document]
        WHERE [Status] NOT IN (1,2,3);
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()

        assert len(records) == 0, '[Document].[Status] column contains values outside the range [1,3]'

    def test_column_max_min_values(self):
        exp_result = [[288, 0]]
        sql_query = f"""
        SELECT
            MAX([ChangeNumber])		AS Max_ChangeNumber
            ,MIN([ChangeNumber])	AS Min_ChangeNumber
        FROM [AdventureWorks2012].[Production].[Document];
        """

        cursor = conn.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()
        records = [list(rows) for rows in records]

        assert records == exp_result, 'Max and min values of the [Document].[ChangeNumber] column are not correct'
