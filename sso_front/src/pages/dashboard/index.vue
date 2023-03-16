<template>
  <div class="container">
    <h5>this is Home!</h5>
    <br />
    <clock :time="time" color="#FYHADCC" border="3px solid" size="400px" ></clock>
  </div>
</template>

<script>

import Clock from 'vue-clock2';
export default {
  name: "dashboard",
  components:{Clock},
  data() {
    return {
      time:"",
    };
  },
  mounted() {
    window.setInterval(() => {
      setTimeout(this.fun, 0)
    }, 1000)
  },
  methods: {
    fun() {
      let date = new Date()
      let h = date.getHours()
      h = h < 10 ? '0' + h : h
      let m = date.getMinutes()
      m = m < 10 ? '0' + m : m
      let s = date.getSeconds()
      s = s < 10 ? '0' + s : s
      this.time = h + ':' + m + ':' + s
    },
  },
};
</script>

<style scoped>
.card-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>