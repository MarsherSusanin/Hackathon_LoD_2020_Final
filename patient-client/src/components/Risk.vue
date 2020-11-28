<template>
    <div class="risk">
        <div class="title">
            <h3><slot></slot></h3>
            <button>Что Это?</button>
        </div>
        <div class="counter">
            <p class="sub">Риск</p>
            <p class="rating">7</p>
            <p class="sub">из 10</p>
        </div>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .risk{
        margin-bottom: 10px;
        background: #FFFFFF;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        display: flex;
        justify-content: space-between;
        width: 100%;
        font-family: Nunito;
        font-style: normal;
        font-weight: normal;
        text-align: left;

        button{
            width: 100px;
            height: 32px;
            left: 10px;
            top: 58px;
            margin-left: 10px;
            margin-top: 15px;

            /* Indian Red */
            background: #D95F5F;
            border-radius: 6px;
            border: none;
            color: white;
            cursor: pointer;
            text-transform: uppercase;
        }

        h3{
            text-align: left;
            align-self: normal;
            margin: 10px;
            font-weight: normal;
            font-size: 16px;
            line-height: 22px;
        }

        .counter{
            width: 100px;
            height: 100px;
            background: #F09292;
            border-radius: 16px;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            .sub{
                font-size: 10px;
                margin: 0;
            }

            .rating{
                font-size: 40px;
                margin: 0;
            }
        }
    }
</style>
