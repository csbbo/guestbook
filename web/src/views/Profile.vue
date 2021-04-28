<template>
  <div class="profile">
      profile
  </div>
</template>

<script>
import { GetUser } from "@/common/api"
export default {
  name: 'Profile',
  created() {
      this.getuser()
  },
  methods: {
      getuser() {
          GetUser().then(resp => {
              console.log(resp)
          })
      }
  }
}
</script>

<style scoped>

</style>
