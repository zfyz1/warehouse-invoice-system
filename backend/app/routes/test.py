from flask import Blueprint, jsonify
from db.db import get_conn
test_bp = Blueprint("test", __name__)

@test_bp.route("/test", methods=["GET"])
def test():
    return jsonify({
        "code": 200,
        "message": "backend is running",
        "data": None
    })

@test_bp.route("/test/db-test", methods=['GET'])
def db_test():
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "code":200,
            "message":"数据库连接成功",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "查询失败",
            "error": str(e)
        })