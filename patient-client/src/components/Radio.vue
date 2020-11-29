<template>
  <div class="radio">
      <div class="radio_item" v-for="(item, index) in list" :key="index">
          <div v-on:click="$emit('activate', index)" class="button" v-bind:class="{'active': item.active}"></div>
          <h4>{{ item.title }}</h4>
      </div>
  </div>
</template>

<script>
export default {
  props: ['list']
}
</script>

<style lang="scss">
    .radio_item{
        width: calc(90% - 60px);
        height: 48px;
        display: flex;
        justify-content: space-between;
        padding: 5px 30px;
        align-items: center;
        /* Outline */
        background: #C5C5C5;
        opacity: 0.5;
        border-radius: 8px;
        margin: 10px auto;

        .button{
            /* White */
            background: #FFFFFF;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            /* Halftone Black */
            border: 1px solid rgba(34, 34, 34, 0.5);
            box-sizing: border-box;
            position: relative;
        }

        .button.active:after{
            content: '';
            position: absolute;
            left: 12%;
            top: 12%;
            background: #00A3A3;
            width: 30px;
            height: 30px;
            border-radius: 50%;
        }
    }
</style>
