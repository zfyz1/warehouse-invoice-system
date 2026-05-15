import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api"
});

// 获取客户列表
export function getCustomerList() {
  return api.get("/customer/getList");
}