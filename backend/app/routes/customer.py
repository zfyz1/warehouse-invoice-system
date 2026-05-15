from flask import Blueprint, request, jsonify
from db.utils import execute_sql

customer_bp = Blueprint('customer', __name__)
@customer_bp.route('/test', methods=['POST'])
def test():
    return "OK"

@customer_bp.route('/add',methods=['POST'])
def add_customer():
    try:
        data = request.json
        fields = []
        values = []
        for key, value in data.items():
            fields.append(key)
            values.append(value)

        sql = f"""
        INSERT INTO customer
        ({','.join(fields)})
        VALUES ({','.join(['%s'] *len(values))})
        """

        execute_sql(sql, values)
        return jsonify({
            "code": 200,
            "message": "客户新增成功"
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "新增失败",
            "error": str(e)
        })

@customer_bp.route('/getList',methods=['GET'])
def get_List():
    try:
        sql = "SELECT * FROM customer WHERE is_deleted = 0"
        data = execute_sql(sql, fetch=True)
        return jsonify({
            "code": 200,
            "message": "查询成功",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "查询失败",
            "error": str(e)
        })

@customer_bp.route('/delete',methods=['DELETE'])
def delete_single():
    try:
        data = request.json
        customer_id = data.get("customer_id")
        if not customer_id:
            return jsonify({
                "code": 400,
                "message": "customer_id不能为空"
            })

        sql= """
        UPDATE customer
        SET is_deleted = 1
        WHERE customer_id = %s
        """

        execute_sql(sql, (customer_id))

        return jsonify({
            "code": 200,
            "message": "删除成功"
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "删除失败",
            "error": str(e)
        })

@customer_bp.route('/update',methods=['POST'])
def update_customer():
    try:
        data = request.json

        # =========================
        # 1️⃣ 提取主键
        # =========================
        customer_id = data.get("customer_id")

        if not customer_id:
            return jsonify({
                "code": 400,
                "message": "customer_id不能为空"
            })

        # =========================
        # 2️⃣ 动态拼接更新字段
        # =========================
        fields = []
        values = []

        for key, value in data.items():
            if key == "customer_id":
                continue
            fields.append(f"{key} = %s")
            values.append(value)

        # =========================
        # 3️⃣ 拼SQL
        # =========================
        sql = f"""
               UPDATE customer
               SET {','.join(fields)}
               WHERE customer_id = %s
               """

        values.append(customer_id)

        # =========================
        # 4️⃣ 执行
        # =========================
        execute_sql(sql, values)

        return jsonify({
            "code": 200,
            "message": "修改成功"
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "修改失败",
            "error": str(e)
        })