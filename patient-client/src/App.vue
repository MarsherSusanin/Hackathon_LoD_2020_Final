<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
    body{
      margin: 0;
      padding: 0;
      font-family: Nunito;
      font-style: normal;
      font-weight: normal;
      font-size: 16px;
      color: #222222;
    }

    .page {
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    input[type="text"], input[type="password"] {
      border: 1px solid rgba(34, 34, 34, 0.5);
      box-sizing: border-box;
      border-radius: 8px;
      height: 48px;
      margin: 10px;
      padding: 10px;
    }

    .wrapper {
      padding: 10px;
    }
</style>
