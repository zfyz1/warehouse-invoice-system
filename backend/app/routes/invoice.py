from flask import Blueprint, request, jsonify
from db.utils import execute_sql
from datetime import datetime
import uuid

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/test', methods=['POST'])
def test():
    return "OK"
@invoice_bp.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        # 创建主表-------------------
        main_sql = """
                insert into invoice(
                invoice_id, customer_id, customer_name, total_price, remark)
                values (%s,%s,%s,%s,%s)
                """
        invoice_id = f"MR{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
        main_params = (
            invoice_id,
            data.get("customer_id"),
            data.get("customer_name"),
            data.get("total_price"),
            data.get("remark")
        )
        execute_sql(main_sql, main_params)
        item_sql = """
                insert into invoice_item(
                invoice_id, product_id, product_name, product_spec, price, quantity, subtotal)
                values(%s,%s,%s,%s,%s,%s,%s)
                """
        # 创建明细表
        for i,item in enumerate(data.get("item")):
            subtotal = item['price'] * item['quantity']
            item_param = (
                invoice_id,
                item['product_id'],
                item['product_name'],
                item['product_spec'],
                item['price'],
                item['quantity'],
                subtotal
            )
            execute_sql(item_sql,item_param)


        # -------------------
        return jsonify({
            "code": 200,
            "message": "销售单创建成功"
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "新增失败",
            "error": str(e)
        })

@invoice_bp.route('/get',methods=['GET'])
def get():
    return "功能未实现"
@invoice_bp.route('/delete', methods=['DELETE'])
def delete():
    return "功能未实现"
@invoice_bp.route('/update',methods=['POST'])
def update():
    return "功能未实现"