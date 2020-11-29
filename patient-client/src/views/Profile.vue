<template>
  <div class="profile">
    <Header>
      Иванов <br>
      Иван <br>
      Иванович
    </Header>
    <div class="wrapper">
    <h2>Общая информация:</h2>
    <Bio/>
    <h2>Адрес проживания:</h2>
    <p class="adress">620735, г.Алапаевск ул.Братьев Карамазовых д. 4 кв. 32</p>
    <h2>Группа риска:</h2>
    <Risk>Ишимическая болезнь</Risk>
    <Risk>Тромбоз</Risk>
    <TabBar/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue'
import TabBar from '@/components/TabBar.vue'
import Bio from '@/components/Bio.vue'
import Risk from '@/components/Risk.vue'

export default {
  name: 'Profile',
  components: {
    Header,
    TabBar,
    Bio,
    Risk
  }
}
</script>

<style lang="scss">
  .profile{
    padding: 0;
    padding-top: 0;
    padding-bottom: 110px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    h2{
      font-family: Nunito;
      font-style: normal;
      font-weight: normal;
      font-size: 16px;
      line-height: 22px;
      text-align: left;
      align-self: normal;
      margin-top: 20px;
    }

    .adress{
      font-family: Nunito;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 19px;
      text-align: left;
      align-self: normal;
      margin-top: 0;
    }
  }
</style>
