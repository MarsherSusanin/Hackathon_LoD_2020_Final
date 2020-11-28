<template>
    <div class="quiz-btn">
        <slot></slot>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .quiz-btn{
        height: 48px;
        border: 1px solid #00A3A3;
        box-sizing: border-box;
        border-radius: 24px;
        color: #00A3A3;
        width: 100%;
        margin: 10px 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-family: Nunito;
        font-style: normal;
        font-weight: bold;
        font-size: 14px;
        line-height: 19px;
        position: relative;
    }

    .quiz-btn:before{
        content: '';
        width: 25px;
        border-top: 2px solid #00A3A3;
        position: absolute;
        top: 23px;
        left: 25px;
    }

    .quiz-btn:after{
        content: '';
        width: 25px;
        border-top: 2px solid #00A3A3;
        position: absolute;
        top: 23px;
        right: 25px;
    }

    .quiz-btn:hover{
        background-color: rgba(0, 163, 163, 0.5);
        cursor: pointer;
    }
</style>
