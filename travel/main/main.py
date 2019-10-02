# -*- coding: utf-8 -*-
# from langdetect import detect_langs
import mysql.connector
import re
from flask import *

import datetime


def check_data(data):
    sum=0
    for i in data :
        if i == "":
            sum=sum+1
        else:
            sum=sum+0
    return sum

def check_date(D_Start, D_End, DT_Start, DT_End):
    if D_Start > D_End or D_Start > DT_Start or D_Start > DT_End or D_End < DT_Start or D_End < DT_End or DT_Start > DT_End:
        A = "ข้อมูลวันท่องเที่ยวผิดพลาด โปรดตรวจสอบใหม่อีกครั้ง"
        return A
    else:
        return None

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
        return "ไม่สามารถใช้ภาษาไทย หรือ อักขระพิเศษได้"
    elif re.match('^(?=\S{8,16}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',passwd) == None:
        return "รหัสผ่านควรมีตัวเลข ตัวอักษรตัวใหญ่อย่างน้อย 1 ตัว(A-Z) ตัวเล็กอย่างน้อย 1 ตัว(a-z) และมีอักขระพิเศษอย่างน้อย  1 ตัว (!@#$%^&*()_+|~-=\\`{}[]:\";'<>?,./)'"
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

def selectall_user():
    mydb = connectsql()
    mycursor = mydb.cursor(dictionary=True)
    text_command = "SELECT * FROM user ;"
    mycursor.execute(text_command)
    myresult = mycursor.fetchall()
    mydb.commit()
    mydb.close()
    return {"user": myresult}

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
    try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "SELECT * FROM tour"
            mycursor.execute(sql, )
            A = mycursor.fetchall()
            mydb.commit()
            mydb.close()
            return jsonify({"Tour":A})
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
    test_data_1 = [name_tour, price, people_max, details, date_start, date_end, date_travel_start, date_travel_end,
                   id_country]

    # date_start_format = DStart
    # date_end_format = DEnd
    # date_travel_start_format = DTStart
    # date_travel_end_format = DTEnd

    DStart = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    DEnd = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    DTStart = datetime.datetime.strptime(date_travel_start, "%Y-%m-%d")
    DTEnd = datetime.datetime.strptime(date_travel_end, "%Y-%m-%d")

    if (check_data(test_data_1)):
        return "กรอกข้อมูลไม่ครบ"
    elif (check_date(DStart, DEnd, DTStart, DTEnd)):
        return "ข้อมูลวันท่องเที่ยวผิดพลาด โปรดตรวจสอบใหม่อีกครั้ง"
    else:
        try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "UPDATE `tour` SET `name_tour`= '{}' ,`price`={},`people_max`={},`details`='{}',`date_start`='{}',`date_end`='{}',`date_travel_start`='{}',`date_travel_end`='{}',`id_country`='{}' WHERE `id_tour`= {};"\
                .format(name_tour,price,people_max,details,date_start,date_end,date_travel_start,date_travel_end,id_country,id_tour)
            mycursor.execute(sql, )
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
    # print(username)
    try:
        mycursor.execute(text_command)
        passwd = mycursor.fetchone()
        # print(passwd)
        # print(str(passwd.get('passwd')) == str(password))
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

def add_history():
    mydb = connectsql()
    data = request.json
    id_user = data['id_user']
    id_tour = data['id_tour']
    status = data['status']
    test_data_1 = [id_user,id_tour,status]

    if (check_data(test_data_1)):
        return "กรอกข้อมูลไม่ครบ"
    else:
        try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "INSERT INTO `history`(`id_history`, `id_user`, `id_tour`, `date_booking`, `status`) VALUES (NULL,{},{},NULL,'{}');".format(id_user,id_tour,
                                                                                                                                                      status)
            mycursor.execute(sql, )
            mydb.commit()
            mydb.close()
            return "เพิ่มข้อมูลการจองทัวร์สำเร็จ"
        except Exception as e:
            return "เพิ่มข้อมูลการจองไม่สำเร็จ"

def select_history():
    mydb = connectsql()
    data = request.json
    id_user = data['id_user']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM history WHERE id_user = {};".format(id_user)
        mycursor.execute(sql, )
        result = mycursor.fetchall()
        mydb.commit()
        mydb.close()
        return jsonify({"result" : result})
    except Exception as e:
        return "เรียกข้อมูลประวัติการจองทัวร์ไม่สำเร็จ"

def edit_password():

    dict_meg = {1:"Success.",2:"Fail.",3:"Old password is wrong",4:"Don't have this username."};
    mydb = connectsql()
    data = request.json
    username = data['username']
    passwd = data['passwd']
    new_password = data['new_password']
    cheak_new_password = data['cheak_new_password']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT passwd FROM user WHERE username = '{}';".format(username)
        mycursor.execute(sql)
        cheak_passwd = mycursor.fetchone()
        if re.match('^(?=\S{8,16}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', new_password) == None:
            return "รหัสผ่านควรมีตัวเลข ตัวอักษรตัวใหญ่อย่างน้อย 1 ตัว(A-Z) ตัวเล็กอย่างน้อย 1 ตัว(a-z) และมีอักขระพิเศษอย่างน้อย  1 ตัว (!@#$%^&*()_+|~-=\\`{}[]:\";'<>?,./)'"
        elif new_password != cheak_new_password:
            return "รหัสผ่านใหม่ไม่ตรงกัน"
        else:
            dict = {'username': username, 'passwd': passwd, 'new_password': new_password}
            for i in dict:
                if (dict.get(i) == ""):
                    return Response(response=json.dumps({"meg": "{} is empty".format(i)}), status=203)
                    print new_password + "1"
                elif (passwd == cheak_passwd.get('passwd')):
                    sql_update = "UPDATE user SET passwd ='{}' WHERE username = '{}';".format(new_password, username)
                    mycursor.execute(sql_update)
                    mydb.commit()
                    return Response(response=json.dumps({"meg": dict_meg.get(1)}), status=200)
                else:
                    return Response(response=json.dumps({"meg": dict_meg.get(3)}), status=203)
                    print new_password + "3"
            mydb.close()

    except Exception as e:
        print(e)
        return Response(response=json.dumps({"meg": dict_meg.get(4)}), status=203)

