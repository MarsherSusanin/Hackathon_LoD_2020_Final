<template>
    <header class="header">
        <h1><slot></slot></h1>
    </header>
</template>

<style lang="scss">
    .header{
        height: 60px;
        background: #00A3A3;
        box-shadow: 0px 4px 8px rgba(0, 163, 163, 0.18);

        h1{
            font-style: normal;
            font-weight: normal;
            font-size: 24px;
            line-height: 59px;
            color: white;
            text-align: center;
            margin: 0;
        }
    }
</style>
