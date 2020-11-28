<template>
    <div class="big-round-btn">
        <slot></slot>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .big-round-btn{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: #00A3A3;
        font-family: Nunito;
        font-style: normal;
        font-weight: bold;
        font-size: 14px;
        line-height: 19px;
        display: flex;
        align-items: center;
        text-align: center;
        letter-spacing: 0.0125em;
        text-transform: uppercase;
        color: white;
        border: 2px solid white;
        position: relative;
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
