<!-- components/HeroSection.vue -->
<template>
  <el-section class="hero">
    <el-row type="flex" justify="center" align="middle">
      <el-col :span="12">
        <h2>Welcome to My Product</h2>
        <p>This is the best product you'll ever use!</p>
        <el-button type="primary" size="large">Get Started</el-button>
      </el-col>
    </el-row>
  </el-section>
</template>

<script>
export default {
  name: "HeroSection"
}
</script>

<style scoped>
.hero {
  background-image: url('your-image-url.jpg');
  background-size: cover;
  background-position: center;
  padding: 100px 0;
  color: white;
  text-align: center;
}
</style>
