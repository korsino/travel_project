# -*- coding: utf-8 -*-
# from langdetect import detect_langs
import mysql.connector
import re
# import responses
from flask import *

#from yaml import load

def check_data(data):
    sum=0
    for i in data :
        if i == "":
            sum=sum+1
        else:
            sum=sum+0
    return sum

def connectsql():
        mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
        database='travel_db',
        user='root',
        password='',
        )
        return mydb
def register_user():
    mydb = connectsql()
    data = request.json
    username = data['username']
    passwd = data['passwd']
    name = data['name']
    birthday = data['birthday']
    email = data['email']
    phone = data['phone']
    address = data['address']
    test_data = [username, passwd, name, address]
    if (check_data(test_data)>0):
        return "กรอกข้อมูลไม่ครบ"
    elif len(passwd) <= 8 or len(passwd) >= 16:
        return "ใส่รหัสผ่านมากกว่า 8 ตัว แต่ไม่เกิน 16 ตัว"
    elif len(phone) != 10:
        return "ใส่หมายเลขโทรศัพให้ครบ 10 ตัว"
    elif re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',email) == None:
        return "E-mail ไม่ถูกต้อง"
    elif re.match('^([-_.a-zA-Z0-9]+)$',username) == None:
        return "ไม่สามารถใช้ภาษาไทยได้"
    elif re.match('^([-_.a-zA-Z0-9]+)$',passwd) == None:
        return "ไม่สามารถใช้ภาษาไทยได้"
    elif re.match('^(?=\S{8,16}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',passwd) == None:
        return "รหัสผ่านควรมีตัวเลข ตัวอักษรตัวใหญ่อย่างน้อย 1 ตัว ตัวเล็กอย่างน้อย 1 ตัว และมีอักขระพิเศษอย่างน้อย  1 ตัว (!@#$%^&*()_+|~-=\\`{}[]:\";'<>?,./)'"
    else:
        try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "INSERT INTO user (id_user,username,passwd,name,birthday,email,phone,address ) VALUES (NULL,'{}','{}','{}','{}','{}','{}','{}');".format(username, passwd, name, birthday, email, phone, address)
            mycursor.execute(sql, )
            print mycursor.rowcount, "record inserted."
            mydb.commit()
            mydb.close()
            return "สมัครสมาชิกสำเร็จ"
        except Exception as e:
            return "มี username อยู่แล้ว"

def select_user():
    mydb = connectsql()
    data = request.json
    username = data['username']
    mycursor = mydb.cursor(dictionary=True)
    text_command = "SELECT * FROM user WHERE username = '{}';".format(username)
    mycursor.execute(text_command)
    myresult = mycursor.fetchall()
    mydb.commit()
    mydb.close()
    list_sql={ username : myresult}
    return list_sql

def update_user():
    mydb = connectsql()
    data = request.json
    username = data['username']
    name = data['name']
    birthday = data['birthday']
    email = data['email']
    phone = data['phone']
    address = data['address']
    mycursor = mydb.cursor(dictionary=True)
    sql = "update user set  name= '{}',birthday= '{}',email= '{}',phone= '{}',address= '{}' where username = '{}';".format(name,birthday,email,phone,address,username)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    return "แก้ไขข้อมูลสำเร็จ"

def add_programtour():
    mydb = connectsql()
    data = request.json
    name_tour = data['name_tour']
    price = data['price']
    people_max = data['people_max']
    details = data['details']
    date_start = data['date_start']
    date_end = data['date_end']
    date_travel_start = data['date_travel_start']
    date_travel_end = data['date_travel_end']
    id_country = data['id_country']
    test_data_1 = [name_tour,price,people_max,details,date_start,date_end,date_travel_start,date_travel_end,id_country]
    try:
        if (check_data(test_data_1)):
            return "กรอกข้อมูลไม่ครบ"
        else:
            mycursor = mydb.cursor(dictionary=True)
            sql = "INSERT INTO tour (id_tour, name_tour, price, people_max, details, date_start, date_end, date_travel_start, date_travel_end, id_country) VALUES " \
                  "(NULL,'{}',{},{},'{}','{}','{}','{}','{}','{}');".format(name_tour,price,people_max,details,date_start,date_end,date_travel_start,date_travel_end,id_country)
            mycursor.execute(sql, )
            print mycursor.rowcount, "Record Inserted."
            mydb.commit()
            mydb.close()
            return "เพิ่มข้อมูลโปรแกรมทัวร์สำเร็จ"
    except Exception as e:
        return "เพิ่มข้อมูลโปรแกรมทัวร์ไม่สำเร็จ"

def select_programtour():
    mydb = connectsql()
    data = request.json
    id_tour = data['id_tour']
    try:
        if id_tour == None:
            return "กรุณา Login ก่อน"
        else:
            mycursor = mydb.cursor(dictionary=True)
            sql = "SELECT * FROM `tour` WHERE `id_tour` = {}".format(id_tour)
            mycursor.execute(sql, )
            A = mycursor.fetchall()
            list_all = {id_tour : A}
            mydb.commit()
            mydb.close()
            return list_all
    except Exception as e:
        return "เรียกข้อมูลโปรแกรมทัวร์ไม่สำเร็จ"


def put_programtour():
    mydb = connectsql()
    data = request.json
    id_tour = data['id_tour']
    name_tour = data['name_tour']
    price = data['price']
    people_max = data['people_max']
    details = data['details']
    date_start = data['date_start']
    date_end = data['date_end']
    date_travel_start = data['date_travel_start']
    date_travel_end = data['date_travel_end']
    id_country = data['id_country']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "UPDATE `tour` SET `name_tour`= '{}' ,`price`={},`people_max`={},`details`='{}',`date_start`='{}',`date_end`='{}',`date_travel_start`='{}',`date_travel_end`='{}',`id_country`='{}' WHERE `id_tour`= {};"\
            .format(name_tour,price,people_max,details,date_start,date_end,date_travel_start,date_travel_end,id_country,id_tour)
        mycursor.execute(sql, )
        print mycursor.rowcount, "Record Inserted."
        mydb.commit()
        mydb.close()
        return "แก้ไขข้อมูลโปรแกรมทัวร์สำเร็จ"
    except Exception as e:
        return "แก้ไขข้อมูลโปรแกรมทัวร์ไม่สำเร็จ"

def delete_programtour():
    mydb = connectsql()
    data = request.json
    id_tour = data['id_tour']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "DELETE FROM `tour` WHERE `id_tour` = {}".format(id_tour)
        mycursor.execute(sql, )
        mydb.commit()
        mydb.close()
        return "ลบข้อมูลโปรแกรมทัวร์สำเร็จ"
    except Exception as e:
        return "ลบข้อมูลโปรแกรมทัวร์ไม่สำเร็จ"
def login():
    mydb = connectsql()
    mycursor = mydb.cursor(dictionary=True)
    data = request.json
    username = data['username']
    password = data['passwd']
    text_command = "SELECT passwd FROM `user` WHERE username = '{}'".format(username)
    dict_meg = {1: "Success login.", 2: "Please login again.", 3: "Don't have this username.", 4: "Password is empty."};
    print(username)
    try:
        mycursor.execute(text_command)
        passwd = mycursor.fetchone()
        print(passwd)
        print(str(passwd.get('passwd')) == str(password))
        if (str(passwd.get('passwd')) == str(password)):
            show = dict_meg.get(1)
            status_code = 200
        elif (str(password) == ""):
            show = dict_meg.get(4)
            status_code = 203
        else:
            show = dict_meg.get(2)
            status_code = 203
        return Response(response=json.dumps({"meg": show}), status=status_code)
    except Exception as e:
        print(e)
        show = dict_meg.get(3)
        return Response(response=json.dumps({"meg": show}), status=203)
