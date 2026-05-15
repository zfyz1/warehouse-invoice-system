<template>
  <div class="invoice-page">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title">销售单</span>
          <span class="invoice-no">单据号：{{ invoiceNo }}</span>
        </div>
      </template>

      <!-- 基本信息区域 -->
      <div class="basic-info">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="info-item">
              <div class="label">销售日期：</div>
              <div class="value">
                <el-date-picker
                  v-model="formData.date"
                  type="date"
                  placeholder="选择日期"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                  style="width: 100%"
                />
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="info-item">
              <div class="label">销售员：</div>
              <div class="value">
                <el-input v-model="formData.salesman" placeholder="请输入销售员" />
              </div>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <div class="info-item">
              <div class="label">选择客户：</div>
              <div class="value">
                <el-select
                  v-model="formData.customerId"
                  placeholder="请选择客户"
                  filterable
                  style="width: 100%"
                  @change="handleCustomerChange"
                >
                  <el-option
                    v-for="customer in customerList"
                    :key="customer.id"
                    :label="customer.name + ' - ' + customer.phone"
                    :value="customer.id"
                  />
                </el-select>
              </div>
              <el-button type="primary" link @click="showAddCustomer = true">
                新增客户
              </el-button>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 明细表格 -->
      <div class="detail-table">
        <div class="table-header">
          <span>销售明细</span>
          <el-button type="primary" size="small" @click="addRow">+ 增加明细</el-button>
        </div>

        <el-table :data="formData.details" border stripe>
          <el-table-column label="商品名称" width="250">
  <template #default="{ row }">
    <div style="display: flex; gap: 8px;">
      <el-input
        v-model="row.productName"
        placeholder="请选择商品"
        size="small"
        readonly
      />
      <el-button
        type="primary"
        size="small"
        @click="openProductDialog(row)"
      >
        选择
      </el-button>
    </div>
  </template>
</el-table-column>

          <el-table-column label="规格型号" width="150">
            <template #default="{ row }">
              <el-input v-model="row.spec" placeholder="规格" size="small" />
            </template>
          </el-table-column>

          <el-table-column label="单位" width="100">
            <template #default="{ row }">
              <el-input v-model="row.unit" placeholder="单位" size="small" />
            </template>
          </el-table-column>

          <el-table-column label="数量" width="120">
            <template #default="{ row }">
              <el-input-number
                v-model="row.quantity"
                :min="1"
                :max="99999"
                size="small"
                controls-position="right"
                style="width: 100%"
                @change="calculateRowAmount(row)"
              />
            </template>
          </el-table-column>

          <el-table-column label="单价" width="120">
            <template #default="{ row }">
              <el-input-number
                v-model="row.price"
                :min="0"
                :precision="2"
                size="small"
                controls-position="right"
                style="width: 100%"
                @change="calculateRowAmount(row)"
              />
            </template>
          </el-table-column>

          <el-table-column label="金额" width="120">
            <template #default="{ row }">
              <span class="amount">{{ row.amount.toFixed(2) }}</span>
            </template>
          </el-table-column>

          <el-table-column label="备注" min-width="150">
            <template #default="{ row }">
              <el-input v-model="row.remark" placeholder="备注" size="small" />
            </template>
          </el-table-column>

          <el-table-column label="操作" width="80" fixed="right">
            <template #default="{ $index }">
              <el-button
                type="danger"
                size="small"
                link
                @click="deleteRow($index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 汇总信息 -->
      <div class="summary">
        <div class="summary-item">
          <span class="label">总数量：</span>
          <span class="value">{{ totalQuantity }}</span>
        </div>
        <div class="summary-item">
          <span class="label">总金额：</span>
          <span class="value total-amount">¥ {{ totalAmount.toFixed(2) }}</span>
        </div>
      </div>
      <!-- 商品选择弹窗 -->
    <el-dialog v-model="showProductDialog" title="选择商品" width="600px">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索商品名称或规格"
        clearable
        style="margin-bottom: 15px"
      />
      <el-table :data="filteredProductList" border @row-click="selectProduct">
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="spec" label="规格" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="price" label="单价" width="120">
          <template #default="{ row }">
            ¥{{ row.price }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="selectProduct(row)">选择</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
      <!-- 备注和操作按钮 -->
      <div class="footer">
        <div class="remark">
          <span class="label">备注：</span>
          <el-input
            v-model="formData.remark"
            type="textarea"
            :rows="2"
            placeholder="请输入备注信息"
            style="width: 80%"
          />
        </div>

        <div class="actions">
          <el-button @click="resetForm">重置</el-button>
          <el-button type="primary" @click="submitForm">保存销售单</el-button>
          <el-button type="success" @click="printInvoice">打印</el-button>
        </div>
      </div>
    </el-card>

    <!-- 新增客户对话框 -->
    <el-dialog v-model="showAddCustomer" title="新增客户" width="500px">
      <el-form :model="newCustomer" label-width="80px">
        <el-form-item label="客户名称">
          <el-input v-model="newCustomer.name" placeholder="请输入客户名称" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="newCustomer.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="newCustomer.address" placeholder="请输入地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddCustomer = false">取消</el-button>
        <el-button type="primary" @click="addCustomer">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
// 生成单据号
const invoiceNo = ref('XS-' + new Date().getTime().toString().slice(-8))

// 客户列表
const customerList = ref([
  { id: 1, name: '张三', phone: '13800138001', address: '北京市朝阳区' },
  { id: 2, name: '李四', phone: '13800138002', address: '上海市浦东新区' },
  { id: 3, name: '王五', phone: '13800138003', address: '广州市天河区' }
])
// 商品列表（模拟数据库）
const productList = ref([
  { id: 1, name: '苹果 iPhone 15', spec: '128GB 蓝色', unit: '台', price: 5999 },
  { id: 2, name: '华为 Mate 60', spec: '256GB 黑色', unit: '台', price: 6999 },
  { id: 3, name: '小米 14 Pro', spec: '512GB 白色', unit: '台', price: 4999 },
  { id: 4, name: '联想笔记本', spec: '16GB 512GB', unit: '台', price: 5999 },
  { id: 5, name: '罗技鼠标', spec: '无线', unit: '个', price: 89 }
])

// 商品选择弹窗显示
const showProductDialog = ref(false)
const currentEditRow = ref(null) // 当前正在编辑的行
const searchKeyword = ref('')
const filteredProductList = computed(() => {
  if (!searchKeyword.value) return productList.value
  return productList.value.filter(p =>
    p.name.includes(searchKeyword.value) || p.spec.includes(searchKeyword.value)
  )
})

// 打开商品选择弹窗
const openProductDialog = (row) => {
  currentEditRow.value = row
  searchKeyword.value = ''
  showProductDialog.value = true
}

// 选择商品
const selectProduct = (product) => {
  if (currentEditRow.value) {
    currentEditRow.value.productName = product.name
    currentEditRow.value.spec = product.spec
    currentEditRow.value.unit = product.unit
    currentEditRow.value.price = product.price
    calculateRowAmount(currentEditRow.value)
  }
  showProductDialog.value = false
}
// 表单数据
const formData = reactive({
  date: new Date().toISOString().split('T')[0],
  salesman: '',
  customerId: '',
  customerName: '',
  details: [
    {
       id: Date.now(),
      productName: '',
      spec: '',
      unit: '',
      quantity: 1,
      price: 0,
      amount: 0,
      remark: ''
    }
  ],
  remark: ''
})

// 新增客户对话框
const showAddCustomer = ref(false)
const newCustomer = reactive({
  name: '',
  phone: '',
  address: ''
})

// 添加一行明细
const addRow = () => {
  formData.details.push({
    id: Date.now(),
    productName: '',
    spec: '',
    unit: '个',
    quantity: 1,
    price: 0,
    amount: 0,
    remark: ''
  })
}

// 删除一行明细
const deleteRow = (index) => {
  formData.details.splice(index, 1)
}

// 计算单行金额
const calculateRowAmount = (row) => {
  row.amount = (row.quantity || 0) * (row.price || 0)
}

// 计算总数量
const totalQuantity = computed(() => {
  return formData.details.reduce((sum, item) => sum + (item.quantity || 0), 0)
})

// 计算总金额
const totalAmount = computed(() => {
  return formData.details.reduce((sum, item) => sum + (item.amount || 0), 0)
})

// 选择客户
const handleCustomerChange = (customerId) => {
  const customer = customerList.value.find(c => c.id === customerId)
  if (customer) {
    formData.customerName = customer.name
  }
}

// 新增客户
const addCustomer = () => {
  if (!newCustomer.name) {
    ElMessage.warning('请输入客户名称')
    return
  }

  const newId = Math.max(...customerList.value.map(c => c.id), 0) + 1
  const customer = {
    id: newId,
    name: newCustomer.name,
    phone: newCustomer.phone,
    address: newCustomer.address
  }

  customerList.value.push(customer)
  formData.customerId = newId
  formData.customerName = newCustomer.name

  showAddCustomer.value = false
  newCustomer.name = ''
  newCustomer.phone = ''
  newCustomer.address = ''

  ElMessage.success('客户添加成功')
}

// 重置表单
const resetForm = () => {
  formData.date = new Date().toISOString().split('T')[0]
  formData.salesman = ''
  formData.customerId = ''
  formData.customerName = ''
  formData.details = []
  formData.remark = ''
  invoiceNo.value = 'XS-' + new Date().getTime().toString().slice(-8)
  ElMessage.info('已重置')
}

// 保存销售单
const submitForm = () => {
  if (!formData.customerId) {
    ElMessage.warning('请选择客户')
    return
  }

  if (formData.details.length === 0) {
    ElMessage.warning('请添加销售明细')
    return
  }

  const hasEmptyProduct = formData.details.some(item => !item.productName)
  if (hasEmptyProduct) {
    ElMessage.warning('请填写商品名称')
    return
  }

  const invoiceData = {
    invoiceNo: invoiceNo.value,
    ...formData,
    totalQuantity: totalQuantity.value,
    totalAmount: totalAmount.value
  }

  console.log('保存的销售单数据：', invoiceData)
  ElMessage.success('保存成功！')

  // 可选：保存后重置或跳转
  // resetForm()
}

// 打印功能
const printInvoice = () => {
  window.print()
}
</script>

<style scoped>
.invoice-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.box-card {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.title {
  font-size: 20px;
  color: #409eff;
}

.invoice-no {
  font-size: 14px;
  color: #909399;
  font-weight: normal;
}

.basic-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.info-item .label {
  width: 80px;
  font-weight: bold;
  color: #606266;
}

.info-item .value {
  flex: 1;
}

.detail-table {
  margin: 20px 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-weight: bold;
  font-size: 16px;
}

.amount {
  color: #f56c6c;
  font-weight: bold;
}

.summary {
  display: flex;
  justify-content: flex-end;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
  margin: 20px 0;
}

.summary-item {
  margin-left: 30px;
  font-size: 16px;
}

.summary-item .label {
  font-weight: bold;
}

.total-amount {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
}

.footer {
  margin-top: 20px;
}

.remark {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.remark .label {
  width: 60px;
  font-weight: bold;
  line-height: 32px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* 打印样式 */
@media print {
  .invoice-page {
    background-color: white;
    padding: 0;
  }

  .actions,
  .table-header .el-button,
  .el-table__append-wrapper,
  .el-dialog__wrapper {
    display: none !important;
  }
}
</style>