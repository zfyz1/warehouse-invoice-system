<template>
  <div>
    <el-button type="primary" @click="showDialog = true">
      选择客户
    </el-button>

<!--    选择客户弹窗-->
     <el-dialog v-model="showDialog" title="选择客户" width="600px">
       <div class="dialog-body">
        <!-- 左侧：分类 -->
          <div class="left">
            <div class="category-item"
                 @click="customerType = 'personal'"
                 :class="{ active: customerType === 'personal' }">个人</div>
            <div class="category-item"
                 @click="customerType = 'company'"
                 :class="{ active: customerType === 'company'}">企业</div>

          </div>
         <!-- 右侧：客户列表 -->
          <div class="right">
            <div
            v-for="customer in filteredCustomerList"
            :key="customer.customer_id"
            class="customer-item">
              <div>{{customer.customer_id}} {{customer.customer_name}}</div>


            </div>

          </div>
        </div>
      <template #footer>
      <el-button @click="showDialog = false">取消</el-button>
      <el-button type="primary" @click="showDialog = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref,onMounted,computed } from 'vue'
import { ElMessage } from 'element-plus'
import {getCustomerList} from "../../api/customer.js";

const customerType = ref('personal')
const showDialog = ref(false)
const customerList = ref([])
const selectedCustomer = ref(null)  //选择客户（状态）

// 连接数据库获取数据top
const loadCustomers = async () =>{
  const res = await getCustomerList();
  console.log(res.data);
  customerList.value = res.data.data
}
onMounted(() => {
  loadCustomers();
});
// 连接数据库获取数据down

const filteredCustomerList = computed(() =>{
  return customerList.value.filter(customer => customer.customer_type === customerType.value)
})

</script>







<style scoped>
.dialog-body {
  display: flex;
  height: 400px;
}

.left {
  width: 120px;
  border-right: 1px solid #eee;
  padding-right: 10px;
}

.category-title {
  font-weight: bold;
  padding: 10px 0;
  color: #909399;
  font-size: 12px;
}

.category-item {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
}

.category-item:hover {
  background-color: #f5f7fa;
}

.category-item.active {
  background-color: #409eff;
  color: white;
}

.right {
  flex: 1;
  padding-left: 10px;
  overflow-y: auto;
}

.customer-item {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  border-bottom: 1px solid #eee;
}

.customer-item:hover {
  background-color: #f5f7fa;
}

.customer-item.active{
  background-color: #409eff;
  color: white;
}
</style>