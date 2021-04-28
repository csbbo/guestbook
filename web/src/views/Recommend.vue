<template>
  <div class="recommend">
    <div class="infinite-list-wrapper" style="overflow:auto">
    <ul
      class="list"
      v-infinite-scroll="load"
      infinite-scroll-disabled="disabled">
      <router-link
        :to="{path: '/message/'+message.id}"
        tag="li" v-for="message, i in messages"
        :key="i"
        class="list-item">
        <div class="card">
            <h3>{{message.title}}</h3>
            <p>{{message.content}}</p>
        </div>
      </router-link>
<!--      <p v-if="loading">加载中...</p>-->
<!--      <p v-if="noMore">没有更多了</p>-->
    </ul>
    </div>
  </div>
</template>

<script>
import '@/less/recommend.less'
import { QueryMessage } from "@/common/api"
export default {
  name: 'Recommend',
  data () {
      return {
        count: 10,
        loading: false,
        messages: [],
      }
    },
    created() {
        this.get_message()
    },
    computed: {
      noMore () {
        return this.count > 20
      },
      disabled () {
        return this.loading || this.noMore
      }
    },
    methods: {
      load () {
        this.loading = true
        setTimeout(() => {
          this.count += 2
          this.loading = false
        }, 2000)
      },
      get_message() {
          QueryMessage().then(resp => {
              if (resp.err === null) {
                  console.log(resp)
                  this.messages = resp.data.messages
              }
              
          })
      }
    }
}
</script>
