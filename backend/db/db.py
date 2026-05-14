import pymysql

def get_conn():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password= "550954",
        database="manrui_invoice_system",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )