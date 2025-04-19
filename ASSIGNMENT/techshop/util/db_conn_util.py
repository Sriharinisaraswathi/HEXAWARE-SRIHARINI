import pyodbc

def get_connection(conn_string):
    try:
        return pyodbc.connect(conn_string)
    except Exception as e:
        raise Exception("Database connection failed: " + str(e))
