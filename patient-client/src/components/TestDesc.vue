<template>
  <div class="test-desc">
      <header>Пищевые пристрастия</header>
      <img class="illustration" src="/img/icons/food.svg" />
      <p>Очень важно честно внести данные о своём питании в анкету, поскольку выражение “ты – то, что ты ешь” существует не просто так.
        Заполните все карточки, чтобы точнее определить свой риск сердечно-сосудистых заболеваний</p>
      <button v-on:click="$emit('allow')">Заполнить</button>
  </div>
</template>

<script>
export default {
  components: {

  }

}
</script>

<style lang="scss">
    .test-desc{
        width: 90%;
        margin: 20px auto;
        background: #FFFFFF;

        /* Veridian Green */
        border: 1px solid #00A3A3;
        box-sizing: border-box;

        /* Tabulation Shadow */
        box-shadow: 0px 0px 8px 2px rgba(0, 163, 163, 0.15);
        border-radius: 24px;

        header{
            background: #00A3A3;
            border-radius: 16px 16px 0px 0px;
        }

        p{
            padding: 0 20px;
        }

        button{
            height: 48px;
            width: 90%;
            border: none;
            color: white;
            /* Indian Red */
            background: #D95F5F;
            border-radius: 24px;
            margin-bottom: 15px;
        }
    }
</style>
