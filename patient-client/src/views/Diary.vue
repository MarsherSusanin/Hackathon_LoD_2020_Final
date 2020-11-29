<template>
  <div class="page dairy">
      <Header>
        Шаг: <span class="sub">{{ step }} из {{ diary.length }}</span>
        <h4>{{ diary[step - 1].title }}</h4>
        <p class="sub">{{ diary[step - 1].description }}</p>
      </Header>
      <div class="wrapper">
      <input type="text" v-for="(item, index) in diary[step - 1].form" :key="index" :placeholder="item.title" v-model="item.value">

      <TabBarDiary v-on:next="next" v-on:back="back" :isNext="allowNext" />
      </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import TabBarDiary from '@/components/TabBarDiary.vue'

export default {
  components: {
    Header,
    TabBarDiary
  },
  data () {
    return {
      step: 1,
      diary: [
        {
          title: 'Давление',
          description: 'Краткая справка почему так важно заполнять этот показатель и за что он отвечает',
          form: [
            { title: 'Систолическое', value: '' },
            { title: 'Диастолическое', value: '' }
          ]
        },
        {
          title: 'ЧСС',
          description: 'Краткая справка почему так важно заполнять этот показатель и за что он отвечает',
          form: [
            { title: 'ЧСС', value: '' }
          ]
        }
      ]
    }
  },
  computed: {
    allowNext () {
      return this.diary[this.step - 1].form.reduce((acc, { value }) => acc && value, true)
    }
  },
  methods: {
    next () {
      if (this.allowNext) {
        if (this.step === this.diary.length) {
          this.$router.push('Home')
        } else {
          this.step++
        }
      }
    },

    back () {
      if (this.step > 1) {
        this.step--
      } else {
        this.$router.push('Home')
      }
    }
  }
}
</script>

<style lang="scss">

</style>
