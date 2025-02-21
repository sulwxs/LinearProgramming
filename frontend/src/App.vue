<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import LinearProgrammingForm from './components/LinearProgrammingForm.vue'
import uplaod from "@/components/upload.vue";
import MatrixView from "@/components/MatrixView.vue";
import test from "@/components/test.vue";
import GraphDeaggble from "@/components/GraphDeaggble.vue";
</script>

<template>
  <header>
<!--    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />-->

<!--    <div class="wrapper">-->
<!--      <HelloWorld msg="线性规划求解器" />-->
<!--    </div>-->
<!--    <MatrixView>></MatrixView>-->
    <GraphDeaggble></GraphDeaggble>
  </header>

  <main>
    <LinearProgrammingForm />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
