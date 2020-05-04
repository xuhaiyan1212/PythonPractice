import pyodbc

class SQLServerHelp:

    def __init__(self, conn_str):
        print("Connection initialize")
        self.conn = pyodbc.connect(conn_str)
        self.csr = self.conn.cursor()

    def __del__(self):
        print("Connection close!")
        self.conn.close()

    def select_return_all_rows(self, query):
        return self.csr.execute(query).fetchall()

    def select_return_top_one_row(self, query):
        return self.csr.execute(query).fetchone()

    def update_sql(self, query):
        self.csr.execute(query)
        self.csr.commit()

    def update_sql_return_rowcount(self, query):
        self.csr.execute(query)
        self.csr.commit()
        return self.csr.rowcount

    def execute_store_procedure_return(self, query):
        return self.csr.execute(query).fetchall()

