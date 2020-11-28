<template>
  <div class="home">
    <Header>Информация о пациенте</Header>
    <Card>
      <template v-slot:header>
        Личная информация
      </template>
      <ul>
        <li>
          <h3>Общая</h3>
          <dl>
            <dt>ФИО:</dt>
            <dd>Иванов Иван Иванович</dd>
          </dl>
          <dl>
            <dt>Возраст:</dt>
            <dd>42</dd>
          </dl>
          <dl>
            <dt>Пол:</dt>
            <dd>Мужской</dd>
          </dl>
          <dl>
            <dt>Рост:</dt>
            <dd>176</dd>
          </dl>
          <dl>
            <dt>Вес:</dt>
            <dd>83</dd>
          </dl>
        </li>
        <li>
          <h3>Документы</h3>
          <dl>
            <dt>Полис ОМС:</dt>
            <dd>0000 0000 0000 0000</dd>
          </dl>
          <dl>
            <dt>СНИЛС:</dt>
            <dd>0000 0000 000</dd>
          </dl>
        </li>
        <li>
          <h3>Социальный статус</h3>
          <dl>
            <dt>Пенсионер:</dt>
            <dd>нет</dd>
          </dl>
          <dl>
            <dt>Род занятий:</dt>
            <dd>безработный</dd>
          </dl>
          <dl>
            <dt>Образование:</dt>
            <dd>высшее</dd>
          </dl>
          <dl>
            <dt>Место проживания:</dt>
            <dd>г.Саратов</dd>
          </dl>
          <dl>
            <dt>Адрес:</dt>
            <dd>ул. Братьев Карамазовых д.82</dd>
          </dl>
        </li>
      </ul>
      <button>Изменить</button>
    </Card>

    <div class="row">
      <Card>
        <template v-slot:header>
          Анализы
        </template>
        <table cellpadding="0">
          <tr>
            <th>Анализ</th>
            <th>Статус</th>
            <th>Действие</th>
          </tr>
          <tr>
            <td>Анализ 1</td>
            <td>Запрошен</td>
            <td></td>
          </tr>
          <tr>
            <td>Анализ 2</td>
            <td>Выполнен</td>
            <td></td>
          </tr>
          <tr>
            <td>Анализ 3</td>
            <td>Отсутствует</td>
            <td></td>
          </tr>
          <tr>
            <td>Анализ 4</td>
            <td>Отсутствует</td>
            <td></td>
          </tr>
        </table>
      </Card>

      <Card>
        <template v-slot:header>
          Осмотр
        </template>
      </Card>
    </div>

    <Card>
        <template v-slot:header>
          Группы риска
        </template>
      </Card>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Card from '@/components/Card.vue'

export default {
  name: 'Home',
  components: {
    Header,
    Card
  }
}
</script>

<style lang="scss">
  .row{
    display: flex;
    width: 100%;
  }

  table{
    width: 100%;
  }

  th{
    font-weight: normal;
    font-size: 10px;
    line-height: 14px;
  }

  tr:nth-child(even){
    background: #eee
  }

  td{
    font-weight: normal;
    font-size: 14px;
    line-height: 19px;
    margin: 0;
    padding: 0;
  }
</style>
