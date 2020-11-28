<template>
  <div class="home">
    <Header>27 Ноября 2020</Header>
    <Info>
      UserName UserFatherName, не забывайте ежедневно контролировать свои показатели. Внесите в систему необходимую информацию.
    </Info>
    <img class="illustration" src="/img/icons/home_base.svg" />
    <BigRoundBtn>Внести показатели</BigRoundBtn>
    <TabBar/>
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
  }
}
</script>

<style lang="scss">
  .home{
    padding: 10px;
    padding-top: 60px;
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
