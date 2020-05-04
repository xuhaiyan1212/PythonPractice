from SQLServerClass import SQLServerHelp

SQL_CONN = ("Trusted_Connection=yes;"
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-OIOAB85\SQLEXPRESS")

SQL_Query_All = "SELECT * FROM MyPractise.dbo.Hackers"

SQL_Query_Top_One = "SELECT count(1) as row_count FROM MyPractise.dbo.Hackers"

SQL_Query_Update = "Update  MyPractise.dbo.Hackers set name='Haiyan1' where hacker_id=5580"

SQL_SP_Return = "{call MyPractise.dbo.sp_get_all_hackers}"

sql_run = SQLServerHelp(SQL_CONN)

result_all = sql_run.select_return_all_rows(SQL_Query_All)
for row in result_all:
    print(row)

result_top_one = sql_run.select_return_top_one_row(SQL_Query_Top_One)
print(result_top_one[0])
print(result_top_one.row_count)

sql_run.update_sql(SQL_Query_Update)

result_rowcount = sql_run.update_sql_return_rowcount(SQL_Query_Update)
print(result_rowcount)

return_sp = sql_run.execute_store_procedure_return(SQL_SP_Return)
print("Here's the output of store procedure execution:")
print(return_sp)
