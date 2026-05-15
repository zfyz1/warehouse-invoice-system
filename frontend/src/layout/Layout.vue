<template>
  <el-container class="layout-container">
    <!-- 左侧导航栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
      <div class="logo">{{ isCollapse ? '后台' : '后台管理系统' }}</div>
      <el-menu
        :default-active="$route.path"
        class="menu"
        :collapse="isCollapse"
        :collapse-transition="false"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/invoice_test">
          <el-icon><User /></el-icon>
          <span>销售单(test)</span>
        </el-menu-item>
        <el-menu-item index="/invoice">
          <el-icon><DataBoard /></el-icon>
          <span>销售单</span>
        </el-menu-item>

      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-container>
      <el-header class="header">
        <div class="collapse-btn" @click="toggleCollapse">
          <el-icon><Fold /></el-icon>
        </div>
        <div class="user-info">
          <el-dropdown>
            <span class="user-name">管理员</span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {DataBoard, User, ShoppingCart, Fold} from '@element-plus/icons-vue'

const router = useRouter()
const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const logout = () => {
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.aside {
  background-color: #304156;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #263445;
}

.menu {
  border-right: none;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
}

.user-name {
  cursor: pointer;
}

.main {
  background-color: #f0f2f6;
  padding: 20px;
}
</style>