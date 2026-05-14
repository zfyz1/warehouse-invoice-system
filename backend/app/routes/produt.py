from flask import Blueprint, request, jsonify
from db.utils import execute_sql
product_bp = Blueprint('product', __name__)


@product_bp.route('/add', methods=['POST'])
def add_product():
    try:
        data = request.json

        sql = """
        INSERT INTO product
        (product_id, product_name, product_spec, product_ref_price, product_unit)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_sql(sql,(data.get("product_id"),
                                data.get("product_name"),
                                data.get("product_spec"),
                                data.get("product_ref_price"),
                                data.get("product_unit"),))

        return jsonify({
            "code": 200,
            "message": "商品添加成功"
        })
    except  Exception as e:
        return jsonify({
            "code": 500,
            "message": "商品添加失败",
            "error": str(e)
        })

@product_bp.route('/getList', methods=['GET'])
def get_product_list():
    try:
        sql = "select * from product"

        data = execute_sql(sql,fetch=True)
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

