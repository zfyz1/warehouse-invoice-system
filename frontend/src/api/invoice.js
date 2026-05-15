// src/api/invoice.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api"
});

export function createInvoice(data) {
  return api.post("/invoice/create", data);
}

export function getInvoiceList(params) {
  return api.get("/invoice/get", { params });
}

export function deleteInvoice(invoiceId) {
  return api.delete("/invoice/delete", { data: { invoice_id: invoiceId } });
}

export function updateInvoice(data) {
  return api.post("/invoice/update", data);
}