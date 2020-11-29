#!flask/bin/python
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import uuid
import time
from datetime import datetime, timedelta
# Подключаем библиотеку для работы с базами данных PostgreSQL:
import psycopg2
from catboost import CatBoostRegressor

#from flask_swagger_ui import get_swaggerui_blueprint

flask_app = Flask(__name__)

app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "MIS Heart", 
		  description = "Медицинская информационная система Сердце",
      validate=True)

### swagger specific ###
#SWAGGER_URL = '/swagger'
#API_URL = '/static/swagger.json'
#SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#    SWAGGER_URL,
#    API_URL,
#    config={
#        'app_name': "MIS Heart"
#    }
#)
#app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
      
#app.UseSwagger();
#app.SwaggerEndpoint("/swagger/OpenAPISpec/swagger.json", "Demo API");


#name_space = app.namespace('api/1.0', description='Main APIs / Version APIs')
name_space_authdoc = app.namespace('api/1.0/authdoc', description='API / Версия API / API-авторизации для доктора')
name_space_authpatient = app.namespace('api/1.0/authpatient', description='API / Версия API / API-авторизации для пациента')
name_space_regdoc = app.namespace('api/1.0/regdoc', description='API / Версия API / API-регистрации нового доктора')
name_space_docregpatient_info = app.namespace('api/1.0/docregpatientinfo', description='API / Версия API / API-регистрации доктором нового пациента')
name_space_docgetallpatients = app.namespace('api/1.0/docgetallpatients', description='API / Версия API / API-получения доктором списка всех пациентов')
name_space_docgetpatient_info = app.namespace('api/1.0/docgetpatientinfo', description='API / Версия API / API-получения доктором основных данных пациента')
name_space_patientgetpatient_info = app.namespace('api/1.0/patientgetpatientinfo', description='API / Версия API / API-получения пациентом основных данных пациента')
name_space_docgetpatient_anamnesis = app.namespace('api/1.0/docgetpatientanamnesis', description='API / Версия API / API-получения доктором анамнеза жизни пациента')
name_space_patientgetpatient_anamnesis = app.namespace('api/1.0/patientgetpatientanamnesis', description='API / Версия API / API-получения пациентом анамнеза жизни пациента')
name_space_docaddpatient_anamnesis = app.namespace('api/1.0/docaddpatientanamnesis', description='API / Версия API / API-добавления доктором анамнеза жизни пациента')
name_space_patientaddpatient_anamnesis = app.namespace('api/1.0/patientaddpatientanamnesis', description='API / Версия API / API-добавления пациентом анамнеза жизни пациента')
name_space_docgetpatient_predict = app.namespace('api/1.0/docgetpatientpredict', description='API / Версия API / API-предсказания доктором состояния пациента')
name_space_patientgetpatient_predict = app.namespace('api/1.0/patientgetpatientpredict', description='API / Версия API / API-предсказания пациентом состояния пациента')
name_space_patientaddpatient_druganamnesis =  app.namespace('api/1.0/patientaddpatientdruganamnesis', description='API / Версия API / API-добавления пациентом анамнеза приема лекарств пациентом')
name_space_patientaddpatient_injuryanamnesis =  app.namespace('api/1.0/patientaddpatientinjuryanamnesis', description='API / Версия API / API-добавления пациентом анамнеза травм пациентом')
name_space_patientaddpatient_smokinganamnesis =  app.namespace('api/1.0/patientaddpatientsmokinganamnesis', description='API / Версия API / API-добавления пациентом анамнеза курения пациента')
name_space_patientaddpatient_alcoholanamnesis =  app.namespace('api/1.0/patientaddpatientalcoholanamnesis', description='API / Версия API / API-добавления пациентом анамнеза Алкоголя пациента')

#model = app.model('Name Model', {'name': fields.String(required = True, description="Name of the person", help="Name cannot be blank.")})
model_regdoc = app.model('Регистрация нового Доктора', {'password': fields.String(required = True, description="Пароль доктора", help="Поле Пароль доктора не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя доктора", help="Поле Имя пользователя доктора не может быть пустым."),
                                'middlename': fields.String(required = True, description="Отчество доктора", help="Поле Отчество доктора не может быть пустым."),
                                'name': fields.String(required = True, description="Имя доктора", help="Поле Имя доктрора не может быть пустым."),
                                'surname': fields.String(required = True, description="Фамилия доктора", help="Поле Фамилия доктора не может быть пустым.")})

model_authdoc = app.model('Авторизация Доктора', {'password': fields.String(required = True, description="Пароль доктора", help="Поле Пароль доктора не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя доктора", help="Поле Имя пользователя доктора не может быть пустым.")})

model_authpatient = app.model('Авторизация Пациента', {'password': fields.String(required = True, description="Пароль доктора", help="Поле Пароль доктора не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя доктора", help="Поле Имя пользователя доктора не может быть пустым.")})

model_docregpatient_info = app.model('Добавление доктором нового пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'policy_oms': fields.String(required = True, description="Полис ОМС пациента", help="Поле Полис ОМС не может быть пустым."),
                                'birthday': fields.String(required = True, description="День рождения пациента", help="Поле День рождения не может быть пустым."),
                                'middlename': fields.String(required = True, description="Отчество пациента", help="Поле Отчество не может быть пустым."),
                                'name': fields.String(required = True, description="Имя пациента", help="Поле Имя не может быть пустым."),
                                'surname': fields.String(required = True, description="Фамилия пациента", help="Поле Фамилия не может быть пустым."),
                                'login': fields.String(required = True, description="Имя пользователя пациента", help="Поле Имя пользователя не может быть пустым."),
                                'password': fields.String(required = True, description="Пароль пациента", help="Поле Пароль не может быть пустым."),
                                'sex': fields.String(required = True, description="Пол пациента (0 - мужской, 1 - женский)", help="Поле Пол не может быть пустым.")})

model_docgetallpatients = app.model('Получение доктором списка всех пациентов',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым.")})


model_docgetpatient_info = app.model('Получение доктором основных данных пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})

model_patientgetpatient_info = app.model('Получение пациентом основных данных пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})


model_docgetpatient_anamnesis = app.model('Получение доктором анамнеза жизни пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})

model_patientgetpatient_anamnesis = app.model('Получение пациентом анамнеза жизни пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})


model_docaddpatient_anamnesis = app.model('Добавление доктором анамнеза жизни пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'live_place': fields.String(required = True, description="Место жизни пациента", help="Поле Место жизни пациента не может быть пустым."),
                                'work_place': fields.String(required = True, description="Место работы пациента", help="Поле Место работы пациента не может быть пустым."),
                                'typelive_place': fields.String(required = True, description="Тип места жизни пациента (1 - город, 2 - село)", help="Поле Тип места жизни пациента не может быть пустым."),
                                'education': fields.String(required = True, description="Образование пациента (2 - начальная школа, 3 - средняя школа, 4 - профессиональное училище, 5 - ВУЗ)", help="Поле Образование пациента не может быть пустым."),
                                'work_status': fields.String(required = True, description="Статус работы пациента (1 - работаю, 2 - не работаю)", help="Поле Статус работы пациента не может быть пустым."),
                                'pensioner': fields.String(required = True, description="Пенсионер (0 - Нет, 1 - Да)", help="Поле Пенсионер пациента не может быть пустым."),
                                'weight': fields.String(required = True, description="Вес пациента (в килограммах)", help="Поле Вес пациента не может быть пустым."),
                                'growth': fields.String(required = True, description="Рост пациента (в метрах)", help="Поле Рост пациента не может быть пустым.")})

model_patientaddpatient_anamnesis = app.model('Добавление пациентом анамнеза жизни пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'live_place': fields.String(required = True, description="Место жизни пациента", help="Поле Место жизни пациента не может быть пустым."),
                                'work_place': fields.String(required = True, description="Место работы пациента", help="Поле Место работы пациента не может быть пустым."),
                                'typelive_place': fields.String(required = True, description="Тип места жизни пациента (1 - город, 2 - село)", help="Поле Тип места жизни пациента не может быть пустым."),
                                'education': fields.String(required = True, description="Образование пациента (2 - начальная школа, 3 - средняя школа, 4 - профессиональное училище, 5 - ВУЗ)", help="Поле Образование пациента не может быть пустым."),
                                'work_status': fields.String(required = True, description="Статус работы пациента (1 - работаю, 2 - не работаю)", help="Поле Статус работы пациента не может быть пустым."),
                                'pensioner': fields.String(required = True, description="Пенсионер (0 - Нет, 1 - Да)", help="Поле Пенсионер пациента не может быть пустым."),
                                'weight': fields.String(required = True, description="Вес пациента (в килограммах)", help="Поле Вес пациента не может быть пустым."),
                                'growth': fields.String(required = True, description="Рост пациента (в метрах)", help="Поле Рост пациента не может быть пустым.")})
                                
model_patientaddpatient_druganamnesis = app.model('Добавление пациентом анамнеза приема лекарств пациентом',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'drug_regular': fields.String(required = True, description="Регулярный прием лекарств пациентом (0 - нет, 1 - да)", help="Поле Регулярный прием лекарств пациентом не может быть пустым."),
                                'drug_pressure': fields.String(required = True, description="Прием пациентом лекарств для давления (0 - нет, 1 - да)", help="Поле Прием пациентом лекарств для давления не может быть пустым."),
                                'drug_cholesterol': fields.String(required = True, description="Прием пациентом лекарств для нормализации холестерина (0 - нет, 1 - да)", help="Поле Прием пациентом лекарств для нормализации холестерина не может быть пустым."),
                                'drug_stroke': fields.String(required = True, description="Прием пациентом лекарств от инсульта (0 - нет, 1 - да)", help="Поле Прием пациентом лекарств от инсульта не может быть пустым."),
                                'drug_diabetes': fields.String(required = True, description="Прием пациентом лекарств от диабета (0 - нет, 1 - да)", help="Поле Прием пациентом лекарств от диабета не может быть пустым.")})

model_patientaddpatient_injuryanamnesis = app.model('Добавление пациентом анамнеза травм пациентом',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'year_injury': fields.String(required = True, description="Наличие травм у пациента за последний год (0 - нет, 1 - да)", help="Поле Наличие травм у пациента за последний год не может быть пустым."),
                                'year_fracture': fields.String(required = True, description="Наличие переломов у пациента за последний год (0 - нет, 1 - да)", help="Поле Наличие переломов у пациента за последний год не может быть пустым."),
                                'count_fracture': fields.String(required = True, description="Количество переломов у пациента за последний год", help="Поле Количество переломов у пациента за последний год не может быть пустым.")})

model_patientaddpatient_smokinganamnesis = app.model('Добавление пациентом анамнеза курения пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'status_smoking': fields.String(required = True, description="Статус курения пациента (0 - Никогда не курил(а), 1 - Бросил(а), 2 - Курит)", help="Поле Статус курения пациента не может быть пустым."),
                                'year_smoking': fields.String(required = True, description="Возраст курения пациента (со скольки лет начал курить, 0 - если никогда не курил(а)", help="Поле Возраст курения пациента не может быть пустым."),
                                'count_smoking': fields.String(required = True, description="Количество сигарет в день (0 - если никогда не курил(а)", help="Поле Количество сигарет в день не может быть пустым."),
                                'passive_smoking': fields.String(required = True, description="Пассивное курение (0 - нет, 1 - да)", help="Поле Пассивное курение не может быть пустым.")})

model_patientaddpatient_alcoholanamnesis = app.model('Добавление пациентом анамнеза курения пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым."),
                                'status_alcohol': fields.String(required = True, description="Статус выпивания алкоголя пациента (0 - Никогда не употреблял(а), 1 - ранее употреблял(а), 2 - употребляю в настоящее время)", help="Поле Статус выпивания алкоголя пациента не может быть пустым."),
                                'year_alcohol': fields.String(required = True, description="Возраст выпивания пациента (со скольки лет начал пить, 0 - если никогда не пил(а)", help="Поле Возраст выпивания пациента не может быть пустым."),
                                'vodka_size': fields.String(required = True, description="Размер стопки водки", help="Поле Размер стопки водки не может быть пустым."),
                                'vodka_regular': fields.String(required = True, description="Регулярность выпивания водки (0 - никогда, 1 - каждый месяц, 2 - каждую неделю, 3 - каждый день)", help="Поле Регулярность выпивания водки не может быть пустым."),
                                'vodka_count': fields.String(required = True, description="Количество стопок водки", help="Поле Количество стопок водки не может быть пустым."),
                                'vodka_year': fields.String(required = True, description="Сколько лет пьет водку", help="Поле Сколько лет пьет водку не может быть пустым."),
                                'vodka_otkazyear': fields.String(required = True, description="Сколько лет не пьет водку", help="Поле Сколько лет не пьет водку не может быть пустым."),
                                'vino_size': fields.String(required = True, description="Размер стопки вина", help="Поле Размер стопки вина не может быть пустым."),
                                'vino_regular': fields.String(required = True, description="Регулярность выпивания вина (0 - никогда, 1 - каждый месяц, 2 - каждую неделю, 3 - каждый день)", help="Поле Регулярность выпивания вина не может быть пустым."),
                                'vino_count': fields.String(required = True, description="Количество стопок вина", help="Поле Количество стопок вина не может быть пустым."),
                                'vino_year': fields.String(required = True, description="Сколько лет пьет вино", help="Поле Сколько лет пьет вино не может быть пустым."),
                                'vino_otkazyear': fields.String(required = True, description="Сколько лет не пьет вино", help="Поле Сколько лет не пьет вино не может быть пустым."),
                                'pivo_size': fields.String(required = True, description="Размер стопки пива", help="Поле Размер стопки пива не может быть пустым."),
                                'pivo_regular': fields.String(required = True, description="Регулярность выпивания пива (0 - никогда, 1 - каждый месяц, 2 - каждую неделю, 3 - каждый день)", help="Поле Регулярность выпивания пива не может быть пустым."),
                                'pivo_count': fields.String(required = True, description="Количество стопок пива", help="Поле Количество стопок пива не может быть пустым."),
                                'pivo_year': fields.String(required = True, description="Сколько лет пьет пиво", help="Поле Сколько лет пьет пиво не может быть пустым."),
                                'pivo_otkazyear': fields.String(required = True, description="Сколько лет не пьет пиво", help="Поле Сколько лет не пьет пиво не может быть пустым."),
                                'samogon_size': fields.String(required = True, description="Размер стопки самогона", help="Поле Размер стопки самогона не может быть пустым."),
                                'samogon_regular': fields.String(required = True, description="Регулярность выпивания самогона (0 - никогда, 1 - каждый месяц, 2 - каждую неделю, 3 - каждый день)", help="Поле Регулярность выпивания самогона не может быть пустым."),
                                'samogon_count': fields.String(required = True, description="Количество стопок самогона", help="Поле Количество стопок самогона не может быть пустым."),
                                'samogon_year': fields.String(required = True, description="Сколько лет пьет самогон", help="Поле Сколько лет пьет самогон не может быть пустым."),
                                'samogon_otkazyear': fields.String(required = True, description="Сколько лет не пьет самогон", help="Поле Сколько лет не пьет самогон не может быть пустым."),
                                'krvino_regular': fields.String(required = True, description="Регулярность выпивания красного вина (0 - никогда, 1 - каждый месяц, 2 - каждую неделю, 3 - каждый день)", help="Поле Регулярность выпивания красного вина не может быть пустым."),
                                'krvino_count': fields.String(required = True, description="Количество стопок красного вина", help="Поле Количество стопок красного вина не может быть пустым."),
                                'krvino_year': fields.String(required = True, description="Сколько лет пьет красное вино", help="Поле Сколько лет пьет красное вино не может быть пустым."),
                                'krvino_otkazyear': fields.String(required = True, description="Сколько лет не пьет красное вино", help="Поле Сколько лет не пьет красное вино не может быть пустым.")})


model_docgetpatient_predict = app.model('Получение доктором предсказание состояния пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'doctor_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})

model_patientgetpatient_predict = app.model('Получение пациентом предсказание собственного состояния',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID пациента", help="Поле ID пациента не может быть пустым.")})

xdbname='heartdb'
xuser='alex'
xpassword='911alex'
xhost='localhost'

#list_of_names = {}
auths = []
auth1 = {}
patient1 = {}

##Функция генерации уникальных идентификаторов:
def newidentificator():
    return str(uuid.uuid4())

def predict(patient_data):
    clf = CatBoostRegressor()
    #test = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
    # больше примеров тут test_data.csv
    diseas=[]
    for model in ['arterial_hypertension.dump', 'ONMK.dump', 'stenokardiya.dump', 'ssnedost.dump', 'other_heart_disease.dump']:
        clf.load_model(model)
        #pred=clf.predict(test, prediction_type='Probability')
        pred=clf.predict(patient_data, prediction_type='Probability')
        #print('Вероятность {}: {:.4f}'.format(model, pred[1]))
        s ='{:.4f}'.format(pred[1]) 
        diseas_pred = { model : s }
        diseas.append(diseas_pred)
    return diseas    

def is_login(login):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM users WHERE (login='"+login+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0] 

def ispatient_login(login):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM patient_info WHERE (login='"+login+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0] 


def is_doctor(uuid):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM users WHERE (user_id='"+uuid+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0]

def is_patient(uuid):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM patient_info WHERE (patient_id='"+uuid+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0]

def is_patientvalid_session_id(patient):
    #print(patient['doctor_id'])
    #print(patient['session_id'])
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT insystemtimeminutes,lastlogindatetime FROM patient_info WHERE (patient_id='"+patient['patient_id']+"' AND session_id='"+patient['session_id']+"')")
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()       
    b = ''
    #print("1")
    if len(results) > 0:
        for row in results:
            #print("2")
            a_k =str(row[0]).split()
            a_k = ''.join(a_k)
            a_s = str(row[1]).split()
            a_s = ''.join(a_s)
            #print(a_k)
            #print(a_s)            
            a_d = time.mktime(time.strptime(a_s, '%d.%m.%Y%H:%M:%S'))
            now = datetime.now()
            now_d = time.mktime(time.strptime(now.strftime('%d.%m.%Y%H:%M:%S'), '%d.%m.%Y%H:%M:%S'))
            k = (now_d-a_d)/60
            k = k - int(a_k)
            b = str(k)
            #print(k)
            #if k > 0:
            #    b = 'wrong lasttime'
            #else:
            #    b = 'ok'
    else:
        b = ''
    return b    


def is_docvalid_session_id(patient):
    #print(patient['doctor_id'])
    #print(patient['session_id'])
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT insystemtimeminutes,lastlogindatetime FROM users WHERE (user_id='"+patient['doctor_id']+"' AND session_id='"+patient['session_id']+"')")
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()       
    b = ''
    #print("1")
    if len(results) > 0:
        for row in results:
            #print("2")
            a_k =str(row[0]).split()
            a_k = ''.join(a_k)
            a_s = str(row[1]).split()
            a_s = ''.join(a_s)
            #print(a_k)
            #print(a_s)            
            a_d = time.mktime(time.strptime(a_s, '%d.%m.%Y%H:%M:%S'))
            now = datetime.now()
            now_d = time.mktime(time.strptime(now.strftime('%d.%m.%Y%H:%M:%S'), '%d.%m.%Y%H:%M:%S'))
            k = (now_d-a_d)/60
            k = k - int(a_k)
            b = str(k)
            #print(k)
            #if k > 0:
            #    b = 'wrong lasttime'
            #else:
            #    b = 'ok'
    else:
        b = ''
    return b    

def is_patient_info(patient):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #print(login)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    cur.execute("SELECT COUNT(*) FROM patient_info WHERE (patient_id='"+patient['patient_id']+"')")
    results = cur.fetchall()
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    #if len(results) > 0:
    for row in results:
        return row[0] 

def insert_new_user_into_db(person):
    now = datetime.now()
    a_d = newidentificator()
    a_d2 = newidentificator()
    a_st = "720"
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO users(surname, name, middlename, user_id, session_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+a_d2+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()

def insert_new_patient_info_into_db(patient):
    now = datetime.now()
    a_d = newidentificator()
    a_d2 = newidentificator()
    a_st = "720"
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO patient_info(surname, name, middlename, patient_id, doctor_id, birthday, policyoms, createdatetime, login, password, sex, lastlogindatetime, insystemtimeminutes, session_id) VALUES('"+patient['surname']+"','"+patient['name']+"','"+patient['middlename']+"','"+a_d+"','"+patient['doctor_id']+"','"+patient['birthday']+"','"+patient['policy_oms']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+patient['login']+"','"+patient['password']+"','"+patient['sex']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"','"+a_d2+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()

def insert_patient_anamnesis_into_db(patient):
    now = datetime.now()
    a_d = newidentificator()
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO patient_anamnesis(patient_id, doctor_id, patientanamnesis_id, liveplace, workplace, createdatetime, typeliveplace, education, workstatus, pensioner, weight, growth) VALUES('"+patient['patient_id']+"','"+patient['doctor_id']+"','"+a_d+"','"+patient['live_place']+"','"+patient['work_place']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+patient['typelive_place']+"','"+patient['education']+"','"+patient['work_status']+"','"+patient['pensioner']+"','"+patient['weight']+"','"+patient['growth']+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()
    patient['patientanamnesis_id'] = a_d
    return patient

def insert_patient_druganamnesis_into_db(patient):
    now = datetime.now()
    a_d = newidentificator()
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO patient_drugs(patient_id, patientanamnesis_id, drug_regular, drug_pressure, drug_cholesterol, drug_stroke, drug_diabetes, createdatetime) VALUES('"+patient['patient_id']+"','"+a_d+"','"+patient['drug_regular']+"','"+patient['drug_pressure']+"','"+patient['drug_cholesterol']+"','"+patient['drug_stroke']+"','"+patient['drug_diabetes']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()
    patient['patientanamnesis_id'] = a_d
    return patient

def insert_patient_injuryanamnesis_into_db(patient):
    now = datetime.now()
    a_d = newidentificator()
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO patient_injurys(patient_id, patientanamnesis_id, year_injury, year_fracture, count_fracture, createdatetime) VALUES('"+patient['patient_id']+"','"+a_d+"','"+patient['year_injury']+"','"+patient['year_fracture']+"','"+patient['count_fracture']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()
    patient['patientanamnesis_id'] = a_d
    return patient

def insert_patient_smokinganamnesis_into_db(patient):
    now = datetime.now()
    a_d = newidentificator()
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #print(person['surname'])
    cur.execute("INSERT INTO patient_smoking(patient_id, patientanamnesis_id, status_smoking, year_smoking, count_smoking, passive_smoking, createdatetime) VALUES('"+patient['patient_id']+"','"+a_d+"','"+patient['status_smoking']+"','"+patient['year_smoking']+"','"+patient['count_smoking']+"','"+patient['passive_smoking']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"')")
    #print(person['surname'])
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()
    patient['patientanamnesis_id'] = a_d
    return patient

def get_patient_druganamnesis_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patientanamnesis_id, drug_regular, drug_pressure, drug_cholesterol, drug_stroke, drug_diabetes, createdatetime FROM patient_drugs WHERE(patient_id='"+patient['patient_id']+"') ORDER BY createdatetime DESC LIMIT 1") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        #patients = []
        patient1 = {}
        for row in results:
            #patient1 = {}
            s = str(row[0]).split() #Фамилия
            patient1['patientanamnesis_id'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient1['drug_regular'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient1['drug_pressure'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient1['drug_cholesterol'] = ' '.join(s)
            s = str(row[4]).split() #Отчество
            patient1['drug_stroke'] = ' '.join(s)
            s = str(row[5]).split() #Отчество
            patient1['drug_diabetes'] = ' '.join(s)
            s = str(row[6]).split() #Отчество
            patient1['createdatetime'] = ' '.join(s)
            #patients.append(patient1)
        #return patients
        return patient1

def get_patient_injuryanamnesis_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patientanamnesis_id, year_injury, year_fracture, count_fracture, createdatetime FROM patient_injurys WHERE(patient_id='"+patient['patient_id']+"') ORDER BY createdatetime DESC LIMIT 1") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        #patients = []
        patient1 = {}
        for row in results:
            #patient1 = {}
            s = str(row[0]).split() #Фамилия
            patient1['patientanamnesis_id'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient1['year_injury'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient1['year_fracture'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient1['count_fracture'] = ' '.join(s)
            s = str(row[4]).split() #Отчество
            patient1['createdatetime'] = ' '.join(s)
            #patients.append(patient1)
        #return patients
        return patient1

def get_patient_smokinganamnesis_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patientanamnesis_id, status_smoking, year_smoking, count_smoking, passive_smoking, createdatetime FROM patient_smoking WHERE(patient_id='"+patient['patient_id']+"') ORDER BY createdatetime DESC LIMIT 1") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        #patients = []
        patient1 = {}
        for row in results:
            #patient1 = {}
            s = str(row[0]).split() #Фамилия
            patient1['patientanamnesis_id'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient1['status_smoking'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient1['year_smoking'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient1['count_smoking'] = ' '.join(s)
            s = str(row[4]).split() #Отчество
            patient1['passive_smoking'] = ' '.join(s)
            s = str(row[5]).split() #Отчество
            patient1['createdatetime'] = ' '.join(s)
            #patients.append(patient1)
        #return patients
        return patient1


def get_user_info_from_db(person):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT surname, name, middlename, user_id, session_id, lastlogindatetime, insystemtimeminutes FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        person={}
        for row in results:
            s = str(row[0]).split() #Фамилия
            person['surname'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            person['name'] = ' '.join(s)
            s = str(row[2]).split() #Отчество
            person['middlename'] = ' '.join(s)
            s = str(row[3]).split() #uuid
            person['doctor_id'] = ' '.join(s)
            s = str(row[4]).split() #uuid
            person['session_id'] = ' '.join(s)
            s = str(row[5]).split() #lastlogindatetime
            person['lastlogindatetime'] = ' '.join(s)
            s = str(row[6]).split() #insystemtimeminutes
            person['insystemtimeminutes'] = ' '.join(s) 
        return person

def get_patient_info_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patient_id, doctor_id, policyoms, createdatetime, session_id, lastlogindatetime, insystemtimeminutes, sex  FROM patient_info WHERE (surname='"+patient['surname']+"' AND name='"+patient['name']+"' AND middlename='"+patient['middlename']+"' AND birthday='"+patient['birthday']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        for row in results:
            s = str(row[0]).split() #Фамилия
            patient['patient_id'] = ' '.join(s)
            s = str(row[1]).split() #Фамилия
            patient['patientdoctor_id'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient['policy_oms'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient['createdatetime'] = ' '.join(s)
            s = str(row[4]).split() #uuid
            patient['session_id'] = ' '.join(s)
            s = str(row[5]).split() #lastlogindatetime
            patient['lastlogindatetime'] = ' '.join(s)
            s = str(row[6]).split() #insystemtimeminutes
            patient['insystemtimeminutes'] = ' '.join(s)
            s = str(row[7]).split() #insystemtimeminutes
            patient['sex'] = ' '.join(s) 
        return patient

def get_patient_info_from_patient_id_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT surname, name, middlename, birthday, doctor_id, policyoms, createdatetime, session_id, lastlogindatetime, insystemtimeminutes, sex  FROM patient_info WHERE (patient_id='"+patient['patient_id']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        for row in results:
            s = str(row[0]).split() #Фамилия
            patient['surname'] = ' '.join(s)
            s = str(row[1]).split() #Фамилия
            patient['name'] = ' '.join(s)
            s = str(row[2]).split() #Фамилия
            patient['middlename'] = ' '.join(s)
            s = str(row[3]).split() #Фамилия
            patient['birthday'] = ' '.join(s)
            s = str(row[4]).split() #Фамилия
            patient['patientdoctor_id'] = ' '.join(s)
            s = str(row[5]).split() #Имя
            patient['policy_oms'] = ' '.join(s)
            s = str(row[6]).split() #Отчество
            patient['createdatetime'] = ' '.join(s)
            s = str(row[7]).split() #uuid
            patient['session_id'] = ' '.join(s)
            s = str(row[8]).split() #lastlogindatetime
            patient['lastlogindatetime'] = ' '.join(s)
            s = str(row[9]).split() #insystemtimeminutes
            patient['insystemtimeminutes'] = ' '.join(s)
            s = str(row[10]).split() #insystemtimeminutes
            patient['sex'] = ' '.join(s) 
        return patient

def get_patient_info_from_login_and_password_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patient_id, doctor_id, policyoms, createdatetime, session_id, lastlogindatetime, insystemtimeminutes, sex, surname, name, middlename, birthday  FROM patient_info WHERE (login='"+patient['login']+"' AND password='"+patient['password']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        for row in results:
            s = str(row[0]).split() #Фамилия
            patient['patient_id'] = ' '.join(s)
            s = str(row[1]).split() #Фамилия
            patient['patientdoctor_id'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient['policy_oms'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient['createdatetime'] = ' '.join(s)
            s = str(row[4]).split() #uuid
            patient['session_id'] = ' '.join(s)
            s = str(row[5]).split() #lastlogindatetime
            patient['lastlogindatetime'] = ' '.join(s)
            s = str(row[6]).split() #insystemtimeminutes
            patient['insystemtimeminutes'] = ' '.join(s)
            s = str(row[7]).split() #insystemtimeminutes
            patient['sex'] = ' '.join(s)
            s = str(row[8]).split() #surname
            patient['surname'] = ' '.join(s)
            s = str(row[9]).split() #name
            patient['name'] = ' '.join(s)
            s = str(row[10]).split() #middlename
            patient['middlename'] = ' '.join(s) 
            s = str(row[11]).split() #middlename
            patient['birthday'] = ' '.join(s) 
        return patient


def get_all_patients_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patient_id, surname, name, middlename, birthday FROM patient_info") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        patients = []
        for row in results:
            patient1 = {}
            s = str(row[0]).split() #Фамилия
            patient1['patient_id'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient1['surname'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient1['name'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient1['middlename'] = ' '.join(s)
            s = str(row[4]).split() #Отчество
            patient1['birthday'] = ' '.join(s)
            patients.append(patient1)
        return patients

def get_patient_anamnesis_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT liveplace, workplace, createdatetime, doctor_id, patientanamnesis_id, typeliveplace, education, workstatus, pensioner, weight, growth FROM patient_anamnesis WHERE (patient_id='"+patient['patient_id']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        patients = []
        for row in results:
            patient1 = {}
            s = str(row[0]).split() #Фамилия
            patient1['live_place'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient1['work_place'] = ' '.join(s)
            s = str(row[2]).split() #Имя
            patient1['createdatetime'] = ' '.join(s)
            s = str(row[3]).split() #Отчество
            patient1['patientdoctor_id'] = ' '.join(s)
            s = str(row[4]).split() #Отчество
            patient1['patientanamnesis_id'] = ' '.join(s)
            s = str(row[5]).split() #Отчество
            patient1['typelive_place'] = ' '.join(s)
            s = str(row[6]).split() #Отчество
            patient1['education'] = ' '.join(s)
            s = str(row[7]).split() #Отчество
            patient1['work_status'] = ' '.join(s)
            s = str(row[8]).split() #Отчество
            patient1['pensioner'] = ' '.join(s)
            s = str(row[9]).split() #Отчество
            patient1['weight'] = ' '.join(s)
            s = str(row[10]).split() #Отчество
            patient1['growth'] = ' '.join(s)
            patients.append(patient1)
        return patients



def get_doctor_fio_from_doctor_id(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT surname, name, middlename FROM users WHERE (user_id='"+patient['patientdoctor_id']+"')") 
    results = cur.fetchall()
    #Закрытие курсора
    cur.close()
    #Фиксация изменений
    #con.commit()
    #Закрытие соединения
    con.close()
    if len(results) > 0:
        for row in results:
            s = str(row[0]).split() #Фамилия
            patient['patientdoctor_surname'] = ' '.join(s)
            s = str(row[1]).split() #Имя
            patient['patientdoctor_name'] = ' '.join(s)
            s = str(row[2]).split() #Отчество
            patient['patientdoctor_middlename'] = ' '.join(s)
        return patient
        

def ishave_login(person):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    # Удаление пользователя:
    cur.execute("SELECT COUNT(*) FROM users WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")
    results = cur.fetchall()
    b = ''
    #if len(results) > 0:
    for row in results:
        if row[0] > 0:
            #return row[0]
            now = datetime.now()
            a_d = newidentificator()
            cur.execute("UPDATE users SET session_id = '"+a_d+"', lastlogindatetime = '"+now.strftime("%d.%m.%Y %H:%M:%S")+"' WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")           
            b='ok'
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()        
    return b

def ispatienthave_login(person):
    #select count(*) from (select * from foo) as x;
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    # Удаление пользователя:
    cur.execute("SELECT COUNT(*) FROM patient_info WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")
    results = cur.fetchall()
    b = ''
    #if len(results) > 0:
    for row in results:
        if row[0] > 0:
            #return row[0]
            now = datetime.now()
            a_d = newidentificator()
            cur.execute("UPDATE patient_info SET session_id = '"+a_d+"', lastlogindatetime = '"+now.strftime("%d.%m.%Y %H:%M:%S")+"' WHERE (login='"+person['login']+"' AND password='"+person['password']+"')")           
            b='ok'
    cur.close()
    #Фиксация изменений
    con.commit()
    #Закрытие соединения
    con.close()        
    return b

@name_space_patientgetpatient_predict.route("/")
class PatientGetPatientPredict(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientgetpatient_predict)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    disease = predict(patient_data)
                    return disease
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientgetpatient_predict.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientgetpatient_predict.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docgetpatient_predict.route("/")
class DocGetPatientPredict(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docgetpatient_predict)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    patient_data = [1,68,0,1,1,1,1,0,0,0,0,0,0,0,0,1,2,18,50,1,3,50,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1]
                    disease = predict(patient_data)
                    return disease
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_docgetpatient_predict.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docgetpatient_predict.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_patientgetpatient_anamnesis.route("/")
class PatientGetPatientAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientgetpatient_anamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patients = get_patient_anamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientgetpatient_anamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientgetpatient_anamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docgetpatient_anamnesis.route("/")
class DocGetPatientAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docgetpatient_anamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    patients = get_patient_anamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_docgetpatient_anamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docgetpatient_anamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docgetallpatients.route("/")
class DocGetAllPatients(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docgetallpatients)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    patients = get_all_patients_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_docgetallpatients.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docgetallpatients.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space_patientgetpatient_info.route("/")
class PatientGetPatientInfo(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientgetpatient_info)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    if is_patient_info(patient1) == 1:
                        patient1 = get_patient_info_from_patient_id_from_db(patient1)
                        patient1 = get_doctor_fio_from_doctor_id(patient1)
                    else:
                        patient1 = {
                            "status" : "Пациента с такими именем, фамилией, отчеством и датой рождения нет в Базе данных",
                            "surname" : patient1["surname"],
                            "name" : patient1["name"],
                            "middlename" : patient1["middlename"],
                            "birthday" : patient1["birthday"]
                        }
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
            return patient1
        except KeyError as e:
            name_space_patientgetpatient_info.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientgetpatient_info.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docgetpatient_info.route("/")
class DocGetPatientInfo(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docgetpatient_info)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    if is_patient_info(patient1) == 1:
                        patient1 = get_patient_info_from_patient_id_from_db(patient1)
                        patient1 = get_doctor_fio_from_doctor_id(patient1)
                    else:
                        patient1 = {
                            "status" : "Пациента с такими именем, фамилией, отчеством и датой рождения нет в Базе данных",
                            "surname" : patient1["surname"],
                            "name" : patient1["name"],
                            "middlename" : patient1["middlename"],
                            "birthday" : patient1["birthday"]
                        }
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
            return patient1
        except KeyError as e:
            name_space_docgetpatient_info.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docgetpatient_info.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space_patientaddpatient_druganamnesis.route("/") 
class PatientAddPatientDrugAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientaddpatient_druganamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patient1["doctor_id"] = ""
                    patient1 = insert_patient_druganamnesis_into_db(patient1)
                    patients = get_patient_druganamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientaddpatient_druganamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientaddpatient_druganamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space_patientaddpatient_injuryanamnesis.route("/") 
class PatientAddPatientInjuryAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientaddpatient_injuryanamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patient1["doctor_id"] = ""
                    patient1 = insert_patient_injuryanamnesis_into_db(patient1)
                    patients = get_patient_injuryanamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientaddpatient_injuryanamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientaddpatient_injuryanamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space_patientaddpatient_smokinganamnesis.route("/") 
class PatientAddPatientSmokingAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientaddpatient_smokinganamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patient1["doctor_id"] = ""
                    patient1 = insert_patient_smokinganamnesis_into_db(patient1)
                    patients = get_patient_smokinganamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientaddpatient_smokinganamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientaddpatient_smokinganamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_patientaddpatient_anamnesis.route("/") 
class PatientAddPatientAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_patientaddpatient_anamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_patient(patient1['patient_id']) == 1:
                if float(is_patientvalid_session_id(patient1)) < 0:
                    patient1["doctor_id"] = ""
                    patient1 = insert_patient_anamnesis_into_db(patient1)
                    patients = get_patient_anamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Имени пользователя и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Пациент с указанным идентификатором не зарегистрован в Базе данных",
                    "patient_id" : patient1["patient_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_patientaddpatient_anamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_patientaddpatient_anamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docaddpatient_anamnesis.route("/") 
class DocAddPatientAnamnesis(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docaddpatient_anamnesis)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    patient1 = insert_patient_anamnesis_into_db(patient1)
                    patients = get_patient_anamnesis_from_db(patient1)
                    return patients
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }
                    return patient1    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
                return patient1
        except KeyError as e:
            name_space_docaddpatient_anamnesis.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docaddpatient_anamnesis.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_docregpatient_info.route("/")
class DocRegisterNewPatientInfo(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_docregpatient_info)
    def post(self):
        try:
            patient1 = app.payload #request.form['data']
            if is_doctor(patient1['doctor_id']) == 1:
                if float(is_docvalid_session_id(patient1)) < 0:
                    if is_patient_info(patient1) == 0:
                        if ispatient_login(patient1["login"]) == 0:
                            insert_new_patient_info_into_db(patient1)
                            patient1 = get_patient_info_from_db(patient1)
                            patient1 = get_doctor_fio_from_doctor_id(patient1)
                        else:
                            patient1 = {
                                "status" : "Пациент с таким Именем пользователя уже есть в Базе Данных",
                                "login" : patient1["login"]
                            }
                    else:
                        patient1 = {
                            "status" : "Пациент с такими именем, фамилией, отчеством и датой рождения уже есть в Базе данных",
                            "surname" : patient1["surname"],
                            "name" : patient1["name"],
                            "middlename" : patient1["middlename"],
                            "birthday" : patient1["birthday"]
                        }
                else:
                    patient1 = {
                    "status" : "Время сессии истекло, войдите в систему заново по своему Логину и Паролю.",
                    "session_id" : patient1["session_id"]
                    }    
            else:
                patient1 = {
                    "status" : "Доктор с указанным идентификатором не зарегистрован в Базе данных",
                    "doctor_id" : patient1["doctor_id"]
                }    
            return patient1
        except KeyError as e:
            name_space_docregpatient_info.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_docregpatient_info.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_regdoc.route("/")
class RegisterNewDoctor(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_regdoc)
    def post(self):
        try:
            auth1 = app.payload #request.form['data'] 
            if is_login(auth1["login"]) == 0:
                insert_new_user_into_db(auth1)
                person = get_user_info_from_db(auth1)
            else:
                person = {
                    "status" : "Доктор с таким Именем пользователя уже есть в Базе данных",
                    "login" : auth1["login"]
                }
            return person
        except KeyError as e:
            name_space_regdoc.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_regdoc.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")


@name_space_authdoc.route("/")
class AuthorizeDoctor(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_authdoc)
    def post(self):
        try:
            auth1 = app.payload #request.form['data']
            if ishave_login(auth1) != 'ok':
                return {
                    "status" : "Такого пользователя нет в системе" 
                }
            else:
                person = get_user_info_from_db(auth1)
                person["status"] = "Вы успешно вошли в систему"
                return person
                 
        except KeyError as e:
            name_space_authdoc.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_authdoc.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

@name_space_authpatient.route("/")
class AuthorizePatient(Resource):
    @app.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    @app.expect(model_authpatient)
    def post(self):
        try:
            auth1 = app.payload #request.form['data']
            if ispatienthave_login(auth1) != 'ok':
                return {
                    "status" : "Такого пациента нет в системе" 
                }
            else:
                #person = get_user_info_from_db(auth1)
                #person["status"] = "Вы успешно вошли в систему"
                patient1 = get_patient_info_from_login_and_password_from_db(auth1)
                patient1 = get_doctor_fio_from_doctor_id(patient1)
                return patient1
                 
        except KeyError as e:
            name_space_authpatient.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space_authpatient.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

if __name__ == '__main__':
        #app.run(debug=True)    
        flask_app.run(host="0.0.0.0", port="80")
