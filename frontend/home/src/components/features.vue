<!-- components/Features.vue -->
<template>
  <el-section class="features">
    <el-row gutter="20" type="flex" justify="center">
      <el-col :span="6" v-for="(feature, index) in features" :key="index">
        <el-card :body-style="{ padding: '20px' }">
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </el-card>
      </el-col>
    </el-row>
  </el-section>
</template>

<script>
export default {
  data() {
    return {
      features: [
        { title: 'Feature 1', description: 'This is a description of feature 1.' },
        { title: 'Feature 2', description: 'This is a description of feature 2.' },
        { title: 'Feature 3', description: 'This is a description of feature 3.' }
      ]
    }
  }
}
</script>

<style scoped>
.features {
  padding: 50px 0;
  background-color: #f8f8f8;
}
</style>
