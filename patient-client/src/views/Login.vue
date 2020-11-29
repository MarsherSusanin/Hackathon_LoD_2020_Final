<template>
  <div class="page login">
      <Header>Вход</Header>
      <div class="wrapper">
      <template v-if="isLoaded">
        <Loader />
      </template>
      <template v-else>
        <img src="/img/icons/login.svg" />
        <input type="text" placeholder="Логин" v-model="user">
        <input type="password" placeholder="Пароль" v-model="password">
        <BigRoundBtn v-on:clicked="auth()" :isInactive="!isFilled">Начать Заботиться О себе</BigRoundBtn>
      </template>
      </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import BigRoundBtn from '@/components/BigRoundBtn.vue'
import Loader from '@/components/Loader.vue'

export default {
  components: {
    Header,
    BigRoundBtn,
    Loader
  },
  data () {
    return {
      user: '',
      password: '',
      isLoaded: false
    }
  },
  computed: {
    isFilled () {
      return this.user && this.password
    }
  },
  methods: {
    auth () {
      this.isLoaded = true
      this.$store.dispatch('login', { login: this.user, password: this.password })
        .then(() => {
          this.$route.push('Home')
        })
        .catch(() => {
          this.isLoaded = false
        })
    }
  }
}
</script>

<style lang="scss">

</style>
