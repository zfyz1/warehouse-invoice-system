from db.db import get_conn


def execute_sql(sql, params = None, fetch=False):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(sql, params or ())

        # 查询
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None

        return result

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()