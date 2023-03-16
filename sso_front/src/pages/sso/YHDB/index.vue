<template>
  <div>
    <iframe id="YHDBiframe" :src="iframesrc" width="100%" height="1000"></iframe>
  </div>
</template>

<script>
export default {
  beforeRouteUpdate(to, from, next) {
    to.meta.title = to.query.title
    next()
  },
  name: 'editor',
  data() {
    return {
      token: '',
      iframesrc: '',
    }
  },
  mounted() {
    const src = this.$route.query
    this.token = sessionStorage.getItem('token')
    this.iframesrc = src.href + '&token=' + this.token
  },
  methods: {},
}
</script>

<style scoped>
.card-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.top-group{
  padding: 10px 0;
  text-align: left;
}

</style>