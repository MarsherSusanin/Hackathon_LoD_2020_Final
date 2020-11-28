<template>
  <div class="quiz">
    <Header>Заполнено: <span class="sub">0 из 10</span></Header>
    <Info>
      UserName UserFatherName, чтобы предвосхитить возможные заболевания системы кровообращения, необходимо постепенно полностью заполнить анкету.
    </Info>
    <div class="btns">
      <QuizBtn>Вредные привычки</QuizBtn>
      <QuizBtn>Пищевые пристрастия</QuizBtn>
      <QuizBtn>Спорт</QuizBtn>
      <QuizBtn>Место жительства</QuizBtn>
      <QuizBtn>Работа</QuizBtn>
      <QuizBtn>Семья</QuizBtn>
    </div>
    <TabBar/>
  </div>
</template>

<script>
// @ is an alias to /src
import Header from '@/components/Header.vue'
import TabBar from '@/components/TabBar.vue'
import Info from '@/components/Info.vue'
import QuizBtn from '@/components/QuizBtn.vue'

export default {
  name: 'Quiz',
  components: {
    Header,
    TabBar,
    Info,
    QuizBtn
  }
}
</script>

<style lang="scss">
  .quiz{
    padding: 10px;
    padding-top: 60px;
    padding-bottom: 110px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .btns{
    margin-top: 20px;
    width: 100%;
  }
</style>
