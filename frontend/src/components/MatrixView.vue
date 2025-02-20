<template>
  <el-tabs tab-position="left" style="height: 200px" class="demo-tabs">
    <el-tab-pane label="矩阵选择" :free-select="false">
        <vue-excel-editor v-model="dataa">
    <vue-excel-column field="user" label="User ID" type="string" width="80px"/>
    <vue-excel-column field="name" label="Name" type="string" width="150px"/>
    <vue-excel-column field="phone" label="Contact" type="string" width="130px"/>
    <vue-excel-column field="gender" label="Gender" type="select" width="50px" :options="['F','M','U']"/>
    <vue-excel-column field="age" label="Age" type="number" width="70px"/>
    <vue-excel-column field="birth" label="Date Of Birth" type="date" width="80px"/>
  </vue-excel-editor>
    </el-tab-pane>
    <el-tab-pane label="文件导入">
      <upload></upload>
    </el-tab-pane>

  </el-tabs>

</template>


<script>
import {ref} from 'vue';
import upload from "@/components/upload.vue";

export default {
  components: {upload},

  setup() {
    const name = ref('app');
    const dataa=ref([]);
dataa.value=  [{user: 'hc', name: 'Harry Cole', phone: '1-415-2345678', gender: 'M', age: 25, birth: '1997-07-01'},
      {user: 'sm', name: 'Simon Minolta', phone: '1-123-7675682', gender: 'M', age: 20, birth: '1999-11-12'},
      {user: 'ra', name: 'Raymond Atom', phone: '1-456-9981212', gender: 'M', age: 19, birth: '2000-06-11'},
      {user: 'ag', name: 'Mary George', phone: '1-556-1245684', gender: 'F', age: 22, birth: '2002-08-01'},
      {user: 'kl', name: 'Kenny Linus', phone: '1-891-2345685', gender: 'M', age: 29, birth: '1990-09-01'}];

    return {name,dataa};
  },



};

</script>
