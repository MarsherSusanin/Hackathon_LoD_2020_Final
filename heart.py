#!flask/bin/python
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import uuid
import time
from datetime import datetime, timedelta
# Подключаем библиотеку для работы с базами данных PostgreSQL:
import psycopg2

flask_app = Flask(__name__)

app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "MIS Heart", 
		  description = "Медицинская информационная система Сердце",
      validate=True)

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
                                'birthday': fields.String(required = True, description="День рождения пациента", help="Поле День рождения не может быть пустым."),
                                'middlename': fields.String(required = True, description="Отчество пациента", help="Поле Отчество не может быть пустым."),
                                'name': fields.String(required = True, description="Имя пациента", help="Поле Имя не может быть пустым."),
                                'surname': fields.String(required = True, description="Фамилия пациента", help="Поле Фамилия не может быть пустым.")})

model_patientgetpatient_info = app.model('Получение пациентом основных данных пациента',
                               {'session_id': fields.String(required = True, description="ID текущей сессии", help="Поле ID текущей сессии не может быть пустым."),
                                'patient_id': fields.String(required = True, description="ID доктора", help="Поле ID доктора не может быть пустым."),
                                'birthday': fields.String(required = True, description="День рождения пациента", help="Поле День рождения не может быть пустым."),
                                'middlename': fields.String(required = True, description="Отчество пациента", help="Поле Отчество не может быть пустым."),
                                'name': fields.String(required = True, description="Имя пациента", help="Поле Имя не может быть пустым."),
                                'surname': fields.String(required = True, description="Фамилия пациента", help="Поле Фамилия не может быть пустым.")})


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
    cur.execute("SELECT COUNT(*) FROM patient_info WHERE (surname='"+patient['surname']+"' AND name='"+patient['name']+"' AND middlename='"+patient['middlename']+"' AND birthday='"+patient['birthday']+"')")
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

def get_patient_info_from_login_and_password_from_db(patient):
    con = psycopg2.connect(dbname=xdbname, user=xuser, password=xpassword, host=xhost)
    #Применение курсоров
    cur = con.cursor()
    #Установка кодировки
    cur.execute("SET NAMES 'utf8'")
    cur.execute("START TRANSACTION")
    #cur.execute("INSERT INTO users(surname, name, middlename, user_id,  login, password, lastlogindatetime, insystemtimeminutes) VALUES('"+person['surname']+"','"+person['name']+"','"+person['middlename']+"','"+a_d+"','"+person['login']+"','"+person['password']+"','"+now.strftime("%d.%m.%Y %H:%M:%S")+"','"+a_st+"')")
    cur.execute("SELECT patient_id, doctor_id, policyoms, createdatetime, session_id, lastlogindatetime, insystemtimeminutes, sex, surname, name, middlename  FROM patient_info WHERE (login='"+patient['login']+"' AND password='"+patient['password']+"')") 
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
                        patient1 = get_patient_info_from_db(patient1)
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
                        patient1 = get_patient_info_from_db(patient1)
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
