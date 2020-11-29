<template>
  <div class="page dairy">
    <template v-if="!isStart">
      <Header>Заполнено: <span class="sub">{{ step }} из {{ diary.length }}</span></Header>
      <TestDesc v-on:allow="isStart = true" />
    </template>
    <template v-else>
      <Header>
        Шаг: <span class="sub">{{ step }} из {{ diary.length }}</span>
        <p class="sub">{{ diary[step - 1].question }}</p>
      </Header>
      <div class="wrapper">
      <Radio v-on:activate="check" :list="diary[step - 1].form" />

      <TabBarDiary v-on:next="next" v-on:back="back" :isNext="allowNext" />
      </div>
    </template>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import TabBarDiary from '@/components/TabBarDiary.vue'
import TestDesc from '@/components/TestDesc.vue'
import Radio from '@/components/Radio.vue'

export default {
  components: {
    Header,
    TabBarDiary,
    TestDesc,
    Radio
  },
  data () {
    return {
      isStart: false,
      step: 1,
      diary: [
        {
          question: 'Как часто вы занимаетесь такими вот интересными штуками?',
          form: [
            { title: 'Ни одной разули', active: false },
            { title: 'Пару разуль', active: false },
            { title: 'Много разуль', active: false }
          ]
        },
        {
          question: 'Как часто вы занимаетесь такими вот интересными штуками?',
          form: [
            { title: 'Ни одной разули', active: false },
            { title: 'Пару разуль', active: false },
            { title: 'Много разуль', active: false }
          ]
        }
      ]
    }
  },
  computed: {
    allowNext () {
      return this.diary[this.step - 1].form.reduce((acc, { active }) => acc || active, false)
    }
  },
  methods: {
    next () {
      if (this.allowNext) {
        if (this.step === this.diary.length) {
          this.$router.push('Quiz')
        } else {
          this.step++
        }
      }
    },

    back () {
      if (this.step > 1) {
        this.step--
      } else {
        this.$router.push('Quiz')
      }
    },

    check (index) {
      this.diary[this.step - 1].form.forEach((item) => { item.active = false })
      this.diary[this.step - 1].form[index].active = true
    }
  }
}
</script>

<style lang="scss">

</style>
