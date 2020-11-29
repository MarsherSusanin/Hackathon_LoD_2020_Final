<template>
  <div class="home">
    <Header>{{ new Date().getDate() }} Ноября 2020</Header>
    <div class="wrapper">
    <Info>
      {{ $store.state.user.name }} {{ $store.state.user.middlename }}, не забывайте ежедневно контролировать свои показатели. Внесите в систему необходимую информацию.
    </Info>
    <img class="illustration" src="/img/icons/home_base.svg" />
    <BigRoundBtn v-on:clicked="$router.push({name: 'Diary'})">Внести показатели</BigRoundBtn>
    <TabBar/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue'
import TabBar from '@/components/TabBar.vue'
import Info from '@/components/Info.vue'
import BigRoundBtn from '@/components/BigRoundBtn.vue'

export default {
  name: 'Home',
  components: {
    Header,
    TabBar,
    BigRoundBtn,
    Info
  },
  mounted () {
    if (!this.$store.state.session_id) {
      this.$router.replace({ name: 'Login' })
    }
  }
}
</script>

<style lang="scss">
  .home{
    padding: 0;
    padding-top: 0;
    padding-bottom: 110px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .illustration{
    margin: 20px;
  }
</style>
