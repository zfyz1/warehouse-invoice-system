# 开票系统 API 设计文档（Invoice System）

---

## 一、项目说明

本系统为简化版开票管理系统，采用前后端分离架构。

后端提供 RESTful API，前端通过 HTTP 调用接口完成业务操作，包括：

- 用户登录
- 客户管理
- 商品管理
- 销售单创建
- 销售单查询与打印

---

## 二、接口设计目标

本接口设计用于：

1. 支撑前后端分离开发
2. 统一数据交互规范
3. 保证后续可扩展性
4. 降低前后端耦合

---

## 三、设计规范

### 3.1 RESTful 风格

| 方法 | 说明 |
|------|------|
| GET | 查询数据 |
| POST | 新增数据 |
| PUT | 修改数据 |
| DELETE | 删除数据 |

---

### 3.2 接口设计原则

- 一个接口只负责一个业务动作
- 接口必须语义清晰（见名知意）
- 所有写操作必须使用 POST/PUT/DELETE
- 查询接口统一使用 GET

---

### 3.3 统一返回格式

所有接口必须返回 JSON：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

---
# 字段说明
- code : 200-成功/400-失败/500-错误
- message : 提示信息
- data : 返回数据


---

## 4. 模块划分

系统包含以下模块：

- user（用户模块）
- customer（客户模块）
- product（商品模块）
- invoice（销售单模块）
- print（打印模块）

---

## 5. 用户模块（user）

### 5.1 登录接口

POST /api/user/login

请求：

```json
{
  "username": "admin",
  "password": "123456"
}
```
返回：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "user_id": 1,
    "username": "admin"
  }
}
```
### 5.2 用户列表
GET/api/user/list
### 5.3 新增用户
POST/api/user/add
### 5.4 修改用户
PUT /api/user/update
### 5.5 删除用户
DELETE /api/user/delete?id=1

## 6.客户模块（customer）
### 6.1 客户列表
GET /api/customer/list

### 6.2 新增客户

POST /api/customer/add

```json
{
  "name": "张三",
  "phone": "123456"
}
```
### 6.3 修改客户
PUT /api/customer/update
### 6.4 删除客户
DELETE /api/customer/delete?id=1

##  7. 商品模块（product）
### 7.1 商品列表

GET /api/product/list

### 7.2 新增商品

POST /api/product/add
```json
{
  "name": "鼠标",
  "spec": "无线"
}
```

### 7.3 修改商品

PUT /api/product/update

### 7.4 删除商品

DELETE /api/product/delete?id=1

## 8. 销售单模块（invoice）
### 8.1 创建销售单

POST /api/invoice/create

请求：
```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "product_name": "鼠标",
      "spec": "无线",
      "price": 100,
      "quantity": 2
    }
  ]
}
```

返回：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "invoice_id": 1001,
    "total_price": 200
  }
}
```

### 8.2 销售单列表

GET /api/invoice/list

### 8.3 销售单详情

GET /api/invoice/detail?id=1001

## 9. 打印模块（print）
### 9.1 打印数据接口

GET /api/invoice/print?id=1001

返回：
```json
{
  "invoice": {},
  "customer": {},
  "items": []
}
```

## 10. 设计约束
- 所有接口必须返回统一JSON结构
- 创建销售单必须为事务操作（invoice + invoice_item）
- 商品信息采用快照存储
- 所有列表接口预留分页扩展能力
## 11. 后续扩展方向
- JWT登录认证
- 用户角色权限系统
- 商品分类体系
- 客户等级体系
- 订单状态流转
- 分页与筛选功能