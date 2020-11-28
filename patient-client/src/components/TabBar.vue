<template>
    <div class="tab-bar">
        <router-link to="/home" active-class="active" class="tab-bar__item tab-bar__item--left">
            <img src="/img/icons/clock_icon.svg" alt="">
            <p>Замеры</p>
        </router-link>
        <router-link to="/quiz" active-class="active" class="tab-bar__item tab-bar__item--center">
            <img src="/img/icons/quiz_icon.svg" alt="">
            <p>Анкета</p>
        </router-link>
        <router-link to="/profile" active-class="active" class="tab-bar__item tab-bar__item--right">
            <img src="/img/icons/profile_icon.svg" alt="">
            <p>Профиль</p>
        </router-link>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .tab-bar{
        display: flex;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 64px;
        box-shadow: 0px -4px 8px rgba(0, 0, 0, 0.06);
        background: white;
    }

    .tab-bar__item{
        border-radius: 6px;
        width: calc(100% / 3);
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-decoration: none;
        color: #222222;
    }

    .tab-bar__item--left{
        border-radius: 0 6px 6px 0;
    }

    .tab-bar__item--right{
        border-radius: 6px 0 0 6px;
    }

    .tab-bar__item.active{
        background-color: #00A3A3;
        color: white;
    }

    .tab-bar__item p{
        margin: 0 5px;
        font-family: Nunito;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
    }

    .tab-bar__item img{
        width: 16px;
    }

    .tab-bar__item.active img{
        filter: invert(100%);
    }
</style>
