<template>
  <div :class="{ hidden: hidden }" class="pagination-container">
    <el-pagination
      :background="background"
      :current-page.sync="currentPage"
      :page-sizes="pagesizes"
      :page-size.sync="pageSize"
      :pager-count="pagerCount"
      :layout="layout"
      :total="total"
      v-bind="$attrs"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    ></el-pagination>
  </div>
</template>

<script>
// import { scrollTo } from '@/utils/scroll-to'

export default {
  name: 'Pagination',
  data() {
    return {}
  },
  props: {
    /**
     * 总页数
     */
    total: {
      required: true,
      type: Number
    },
    /**
     * 默认当前页
     */
    page: {
      default: 1,
      type: Number
    },
    /**
     * 默认分页大小
     */
    limit: {
      type: Number,
      default: 5
    },
    /**
     * 分页大小
     */
    pagesizes: {
      type: Array,
      default() {
        return [10, 20, 30, 50, 100]
      }
    },
    /**
     * 移动端页码按钮的数量端默认值5
     */
    pagerCount: {
      type: Number,
      default: document.body.clientWidth < 992 ? 5 : 7
    },

    /**
     * 布局方式
     */
    layout: {
      type: String,
      default: 'total, sizes, prev, pager, next, jumper'
    },

    /**
     *是否显示背景
     */
    background: {
      type: Boolean,
      default: true
    },

    /**
     * 自动滚动
     */
    autoScroll: {
      type: Boolean,
      default: true
    },

    /**
     * 是否隐藏
     */
    hidden: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    /**
     * 当前页
     */
    currentPage: {
      get() {
        return this.page
      },
      set(val) {
        this.$emit('update:page', val)
      }
    },
    /**
     * 分页大小
     */
    pageSize: {
      get() {
        return this.limit
      },
      set(val) {
        this.$emit('update:limit', val)
      }
    }
  },
  methods: {
    handleSizeChange(val) {
      if (this.currentPage * val > this.total) {
        this.currentPage = 1
      }
      this.$emit('pagination', { page: this.currentPage, limit: val })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    },
    handleCurrentChange(val) {
      this.$emit('pagination', { page: val, limit: this.pageSize })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    }
  }
}
</script>
<style scoped>
.pagination-container {
  background: #fff;
  padding: 32px 16px;
}
.pagination-container.hidden {
  display: none;
}
</style>