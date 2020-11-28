<template>
    <div class="bio">
        <div class="bio__item">
            <h3>Пол</h3>
            <p>M</p>
        </div>
        <div class="delim"></div>
        <div class="bio__item">
            <h3>Возраст</h3>
            <p>42</p>
        </div>
        <div class="delim"></div>
        <div class="bio__item">
            <h3>Рост</h3>
            <p>174</p>
        </div>
        <div class="delim"></div>
        <div class="bio__item">
            <h3>Вес</h3>
            <p>82</p>
        </div>
    </div>
</template>

<script>
export default {
}
</script>

<style lang="scss">
    .bio{
        width: 100%;
        display: flex;
        justify-content: space-around;

        h3{
            color: #ccc;
            margin: 0;
            font-family: Nunito;
            font-style: normal;
            font-weight: normal;
            font-size: 14px;
            line-height: 19px;
        }

        p{
            font-family: Nunito;
            font-style: normal;
            font-weight: bold;
            font-size: 14px;
            line-height: 19px;
            margin: 5px;
        }

        .delim{
            width: 1px;
            height: 50px;
            background-color: #ccc;
        }
    }

    .bio__item{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
</style>
