from DBHelper.SQLServerClass import SQLServerHelp

SQL_CONN = ("Trusted_Connection=yes;"
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-OIOAB85\SQLEXPRESS")

Query_Select_All = "SELECT * FROM MyPractise.dbo.Hackers"

Query_Top_One = "SELECT count(1) as row_count FROM MyPractise.dbo.Hackers"

Query_Update = "Update  MyPractise.dbo.Hackers set name='Haiyan1' where hacker_id=5580"

Query_SP_Return = "{call MyPractise.dbo.sp_get_all_hackers}"

#Initialize SQLServerHelp Class
sql_run = SQLServerHelp(SQL_CONN)

result_all = sql_run.select_return_all_rows(Query_Select_All)
for row in result_all:
    print(row)

result_top_one = sql_run.select_return_top_one_row(Query_Top_One)
print(result_top_one[0])
print(result_top_one.row_count)

sql_run.update_sql(Query_Update)

result_rowcount = sql_run.update_sql_return_rowcount(Query_Update)
print(result_rowcount)

return_sp = sql_run.execute_store_procedure_return(Query_SP_Return)
print("Here's the output of store procedure execution:")
print(return_sp)