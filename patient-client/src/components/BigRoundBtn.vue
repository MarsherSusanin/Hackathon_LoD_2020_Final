<template>
    <div @click="$emit('clicked')" class="big-round-btn" v-bind:class="{'big-round-btn--inactive': isInactive}">
        <slot></slot>
    </div>
</template>

<script>
export default {
  props: ['isInactive']
}
</script>

<style lang="scss">
    .big-round-btn{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: #00A3A3;
        font-style: normal;
        font-weight: bold;
        display: flex;
        align-items: center;
        text-align: center;
        text-transform: uppercase;
        color: white;
        border: 2px solid white;
        position: relative;
        margin: 30px auto;
        cursor: pointer;

        &--inactive{
            background: #c5c5c5;
        }
    }

    .big-round-btn::before {
        content: '';
        width: 123px;
        height: 123px;
        display: block;
        position: absolute;
        top: -7px;
        bottom: 0;
        left: -7px;
        right: 0;
        border-radius: 50%;
        border: 6px solid #00A3A3;
        box-shadow: 0px 0px 4px 2px rgba(0, 163, 163, 0.15);
    }

</style>
