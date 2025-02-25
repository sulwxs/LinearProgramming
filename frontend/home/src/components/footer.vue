<!-- components/Footer.vue -->
<template>
  <el-footer class="footer">
    <el-row type="flex" justify="center">
      <el-col :span="8">
        <p>Contact Us: contact@myproduct.com</p>
        <p>Follow us on social media</p>
      </el-col>
    </el-row>
  </el-footer>
</template>

<script>
export default {
  name: "Footer"
}
</script>

<style scoped>
.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 20px;
}
</style>
