<template>
    <div class="tab-bar-diary">
        <button v-on:click="$emit('back')" class="back">Назад</button>

        <button v-on:click="$emit('next')" class="next" v-bind:class="{'disabled': !isNext}">Далее</button>
    </div>
</template>

<script>
export default {
  props: ['isNext', 'isBack']
}
</script>

<style lang="scss">
    .tab-bar-diary{
        display: flex;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 64px;
        box-shadow: 0px -4px 8px rgba(0, 0, 0, 0.06);
        background: white;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    .tab-bar-diary button.next{
        width: 100px;
        height: 32px;
        background: #00A3A3;
        border-radius: 6px;
        border: none;
        color: white;
    }

    .tab-bar-diary button.next.disabled{
        background: #C5C5C5;
    }

    .tab-bar-diary button.back{
        width: 100px;
        height: 32px;
        background:#F5F5F5;;
        border-radius: 6px;
        border: none;
        color: #222222;
    }

</style>
