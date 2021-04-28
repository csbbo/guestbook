<template>
  <div class="message">
      <h1>{{message.title}}</h1>
      <p>{{message.content}}</p>
      <hr/>
      <p>{{comments}}</p>
  </div>
</template>

<script>
import { GetMessage, QueryComment } from "@/common/api"
export default {
    name: 'Message',
    data() {
        return {
            message: {
                title: '',
                content: '',
            },
            comments: [],
        }
    },
    created() {

        this.get_message_commend()
    },
  methods: {
      get_message_commend() {
        const message_id = this.$route.params.mid
        GetMessage({id: message_id}).then(resp => {
            if (resp.err != null){
                alert(resp.msg)
            } else {
                console.log(resp.data)
                this.message = resp.data.message
                QueryComment({mid: message_id}).then(sub_resp => {
                    if (sub_resp.err != null){
                        alert(sub_resp.msg)
                    } else {
                        console.log(sub_resp.data)
                        console.log('get message and commend success!')
                        this.comments = sub_resp.data.comments
                    }
                })
            }
        })
      }
  }
}
</script>

<style scoped>

</style>
