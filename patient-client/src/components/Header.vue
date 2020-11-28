<template>
    <header>
        <slot></slot>
    </header>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    header {
        background-color: #00A3A3;
        width: calc(100% - 20px);
        min-height: 28px;
        border-radius: 0 0 8px 8px;
        position: fixed;
        top: 0;
        left: 0;
        text-align: left;
        padding: 10px 10px;

        font-family: Nunito;
        font-style: normal;
        font-weight: bold;
        font-size: 20px;
        line-height: 27px;

        color: white;

        .sub{
            font-weight: normal;
        }
    }
</style>
