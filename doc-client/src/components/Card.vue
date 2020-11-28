<template>
    <div class="card">
        <h2><slot name="header"></slot></h2>
        <slot></slot>
    </div>
</template>

<style lang="scss">
    .card{
        background: #FFFFFF;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.04);
        border-radius: 8px;
        padding: 20px;
        margin: 30px;
        flex-grow: 1;

        h2{
            font-size: 32px;
            line-height: 44px;
            position: relative;
        }

        h3{
            font-size: 24px;
            line-height: 33px;
        }

        dl{
            display: flex;
            margin: 15px 10px;

            dt{
                font-weight: bold;
                font-size: 20px;
                line-height: 27px;
            }

            dd{
                font-weight: normal;
                font-size: 20px;
                line-height: 27px;
            }
        }

        button{
            width: 138px;
            height: 40px;
            left: 53px;
            top: 770px;
            background: #00A3A3;
            border-radius: 8px;
            border: none;
            color: white;
            margin:  50px 0 30px 50px;
            cursor: pointer;
        }
    }
</style>
