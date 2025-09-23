<template>
  <el-header class="nav">
    <div class="nav-left">
      <img class="logo" :src="logo" alt="logo"/>
      <span class="brand" style="margin-left: 10px">Echo Trace</span>
    </div>
    <el-menu mode="horizontal" background-color="transparent" text-color="#E6E8EB" active-text-color="#8be9fd"
             :default-active="$route.name">
      <el-menu-item index="Home" @click="$router.push('/')">Home</el-menu-item>
      <el-menu-item index="Services">Services</el-menu-item>
      <el-menu-item index="About">About us</el-menu-item>
      <el-menu-item index="Contact">Contact us</el-menu-item>
    </el-menu>
  </el-header>
</template>

<script>
export default {
  name: 'NavBar',
  props: {logo: {type: String, default: require('@/assets/logo.png')}}
}
</script>

<style scoped>
.nav {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #0A0A0A;
  border-bottom: 1px solid rgba(255, 255, 255, .06)
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 12px
}

.logo {
  width: 70px;
  height: 70px;
  object-fit: contain;
}

.brand {
  color: #fff;
  font-weight: 700;
  letter-spacing: .2px;
  font-size: 42px;
}
</style>
