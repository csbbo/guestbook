<template>
  <div class="main">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        </el-menu>
        <div class="line"></div>
        <el-menu
        :default-active="activeIndex"
        router
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="/">首页</el-menu-item>
        <el-submenu index="2">
            <template #title>我的工作台</template>
            <el-menu-item index="2-1">选项1</el-menu-item>
            <el-menu-item index="2-2">选项2</el-menu-item>
            <el-menu-item index="2-3">选项3</el-menu-item>
            <el-submenu index="2-4">
            <template #title>选项4</template>
            <el-menu-item index="2-4-1">选项1</el-menu-item>
            <el-menu-item index="2-4-2">选项2</el-menu-item>
            <el-menu-item index="2-4-3">选项3</el-menu-item>
            </el-submenu>
        </el-submenu>
        <el-menu-item index="/login">登录</el-menu-item>
        <el-menu-item index="/regist">注册</el-menu-item>
    </el-menu>
  </div>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'Main',
}
</script>

<style scoped>

</style>
