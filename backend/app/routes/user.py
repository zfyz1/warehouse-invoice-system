from flask import Blueprint, request, jsonify

user_bp = Blueprint("user", __name__)

# 模拟用户数据（后面会换数据库）
users = [
    {"id": 1, "username": "admin", "password": "admin123"}
]

@user_bp.route("/login",methods=["post"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({
                "code": 200,
                "message": "login success",
                "data": {
                    "user_id" : user["id"]
                }
            })
        else:
            return jsonify({
                "code": 400,
                "message": "invalid usename or password",
                "data": None
            })
