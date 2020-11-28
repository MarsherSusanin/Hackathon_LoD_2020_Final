<template>
    <div class='info'>
        <slot></slot>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .info{
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.06);
        font-family: Nunito;
        font-style: normal;
        font-weight: bold;
        font-size: 14px;
        line-height: 19px;
        text-align: center;
        letter-spacing: 0.001em;
    }
</style>
