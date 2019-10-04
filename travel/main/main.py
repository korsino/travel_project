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

def check_data_username(data_username,username):
    sum=0
    for i in data_username:
        if username == i['username']:
            sum = sum + 1
        else:
            sum = sum + 0
    return sum

def check_data_email(data_email,email):
    sum=0
    for i in data_email:
        if email == i['email']:
            sum = sum + 1
        else:
            sum = sum + 0
    return sum

def check_data_phone(data_phone,phone):
    sum=0
    for i in data_phone:
        if phone == i['phone']:
            sum = sum + 1
        else:
            sum = sum + 0
    return sum


def check_date(D_Start, D_End, DT_Start, DT_End):
    if D_Start > D_End or D_Start > DT_Start or D_Start > DT_End or D_End > DT_Start or D_End > DT_End or DT_Start > DT_End:
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
    mydb1 = connectsql()
    mycursor1 = mydb1.cursor(dictionary=True)
    sql1 = "SELECT * FROM user"
    mycursor1.execute(sql1)
    myresult1 = mycursor1.fetchall()
    mydb1.commit()
    mydb1.close()
    data = request.json
    username = data['username']
    passwd = data['passwd']
    name = data['name']
    birthday = data['birthday']
    email = data['email']
    phone = data['phone']
    address = data['address']
    # print myresult1
    # print check_data_email(myresult1,email)
    # print check_data_phone(myresult1,phone)
    # print check_data_username(myresult1,username)
    test_data = [username, passwd, name, address]
    if (check_data(test_data)>0):
        return "กรอกข้อมูลไม่ครบ"
    elif check_data_username(myresult1,username) > 0:
        return "มี username อยู่แล้ว"
    elif re.match('^([-_.a-zA-Z0-9]+)$',username) == None:
        return "ไม่สามารถใช้ภาษาไทย หรือ อักขระพิเศษได้"
    elif len(passwd) <= 8 or len(passwd) >= 16:
        return "ใส่รหัสผ่านมากกว่า 8 ตัว แต่ไม่เกิน 16 ตัว"
    elif re.match('^(?=\S{8,16}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',passwd) == None:
        return "รหัสผ่านควรมีตัวเลข ตัวอักษรตัวใหญ่อย่างน้อย 1 ตัว(A-Z) ตัวเล็กอย่างน้อย 1 ตัว(a-z) และมีอักขระพิเศษอย่างน้อย  1 ตัว (!@#$%^&*()_+|~-=\\`{}[]:\";'<>?,./)'"
    elif re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',email) == None:
        return "E-mail ไม่ถูกต้อง"
    elif check_data_email(myresult1,email) > 0:
        return "มี E-mail อยู่แล้ว"
    elif len(phone) != 10:
        return "ใส่หมายเลขโทรศัพให้ครบ 10 ตัว"
    elif re.match('^([-_.0-9]+)$', phone) == None:
        return "ใส่หมายเลขโทรศัพให้ครบ 10 ตัว"
    elif check_data_phone(myresult1,phone) > 0:
        return "มีเบอร์โทรศัพท์นี้อยู่แล้ว"
    else:
        try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "INSERT INTO user (id_user,username,passwd,name,birthday,email,phone,address ) VALUES (NULL,'{}','{}','{}','{}','{}','{}','{}');".format(username, passwd, name, birthday, email, phone, address)
            mycursor.execute(sql, )
            mydb.commit()
            mydb.close()
            return "สมัครสมาชิกสำเร็จ"
        except Exception as e:
            return "ผิด"

def select_user():
    mydb = connectsql()
    # data = request.json
    username = request.args['username']
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
    if len(phone) != 10:
        return "ใส่หมายเลขโทรศัพให้ครบ 10 ตัว"
    elif re.match('^([-_.0-9]+)$', phone) == None:
        return "ใส่หมายเลขโทรศัพให้ครบ 10 ตัว"
    elif re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) == None:
        return "E-mail ไม่ถูกต้อง"
    else:
        mycursor = mydb.cursor(dictionary=True)
        sql = "update user set  name= '{}',birthday= '{}',email= '{}',phone= '{}',address= '{}' where username = '{}';".format(name,birthday,email,phone,address,username)
        try:
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
            return "แก้ไขข้อมูลสำเร็จ"
        except Exception as e:
            print(e)
            # return Response(response=json.dumps({"meg": "ไมมีuser nameนี้"}), status=203)
            return Response(response=json.dumps({"meg": "don't havve this username"}), status=203)

def report_tour():
    mydb = connectsql()
    mydb1 = connectsql()
    data = request.json
    date_start = data['date']
    date_time_now = datetime.datetime.now()
    Y_ear = date_start.split("-")[0]
    M_onth = date_start.split("-")[1]
    D_ay =  date_start.split("-")[2]
    mycursor = mydb.cursor(dictionary=True)
    mycursor1 = mydb1.cursor(dictionary=True)
    # ปี : เดือน : วัน
    if Y_ear != "00" and M_onth != "00" and D_ay != "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE date(history.date_booking) = '{}' AND history.status='not paid';".format(date_start)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE date(history.date_booking) = '{}' AND history.status='paid';".format(date_start)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay" : myresult},{"paid": myresult1 }]))
    # ปี : วัน
    elif Y_ear != "00" and M_onth == "00" and D_ay != "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND DAY(date(history.date_booking)) = '{}' AND history.status='not paid';".format(Y_ear,D_ay)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND DAY(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear,D_ay)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # ปี : เดือน
    elif Y_ear != "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(Y_ear,M_onth)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear,M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # เดือน : วัน
    elif Y_ear != "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth,D_ay)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth,D_ay)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # ปี
    elif Y_ear != "00" and M_onth == "00" and D_ay == "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth,D_ay)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # เดือน
    elif Y_ear == "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # วัน
    elif Y_ear == "00" and M_onth == "00" and D_ay != "00":
        sql = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE DAY(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth)
        sql1 = "SELECT COUNT(status) as NUM_OF_RESERVE FROM history WHERE DAY(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    else:
        return "ผิด"
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
    # date_start_format = DStart
    # date_end_format = DEnd
    # date_travel_start_format = DTStart
    # date_travel_end_format = DTEnd

    DStart = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    DEnd = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    DTStart = datetime.datetime.strptime(date_travel_start, "%Y-%m-%d")
    DTEnd = datetime.datetime.strptime(date_travel_end, "%Y-%m-%d")
    try:
        if (check_data(test_data_1)):
            return "กรอกข้อมูลไม่ครบ"
        elif (check_date(DStart, DEnd, DTStart, DTEnd)):
            return "ข้อมูลวันท่องเที่ยวผิดพลาด โปรดตรวจสอบใหม่อีกครั้ง"
        elif re.match('^([0-9]+)$', price or people_max) == None:
            return "ระบุราคาเป็นตัวเลขเท่านั้น"
        elif re.match('^([A-Z]+)$', id_country) == None:
            return "กรุณากรอกเป็นภาษาอังกฤษ ตัวพิมพ์ใหญ่"
        elif len(id_country) != 2:
            return "กรอกข้อมูลไม่เกิน 2 ตัว"
        else:
            mycursor = mydb.cursor(dictionary=True)
            sql = "INSERT INTO tour (id_tour, name_tour, price, people_max, details, date_start, date_end, date_travel_start, date_travel_end, id_country) VALUES " \
                  "(NULL,'{}',{},{},'{}','{}','{}','{}','{}','{}');".format(name_tour,price,people_max,details,date_start,date_end,date_travel_start,date_travel_end,id_country)
            mycursor.execute(sql, )
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
    elif re.match('^([0-9]+)$', price or people_max) == None:
        return "ระบุราคาเป็นตัวเลขเท่านั้น"
    elif re.match('^([A-Z]+)$', id_country) == None:
        return "กรุณากรอกเป็นภาษาอังกฤษ ตัวพิมพ์ใหญ่"
    elif len(id_country) != 2:
        return "กรอกข้อมูลไม่เกิน 2 ตัว"
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
    dict_meg = {1: "เข้าสู่ระบบสำเร็จ", 2: "Username หรือ Password ผิดพลาด", 3: "Username หรือ Password ผิดพลาด", 4: "โปรดใส่รหัสผ่าน"};
    # print(username)
    try:
        mycursor.execute(text_command)
        passwd = mycursor.fetchone()
        # print(passwd)
        # print(str(passwd.get('passwd')) == str(password))
        if (str(passwd.get('passwd')) == str(password)):
            # show = "เข้าสู่ระบบสำเเร็จ"
            # status_code = 200
            sql = "SELECT type FROM user WHERE username = '{}'".format(username)
            mycursor.execute(sql)
            type_user = mycursor.fetchone()
            return jsonify({"msg":"เข้าสู่ระบบสำเร็จ, " + str(type_user.get('type'))})
        elif (str(password) == ""):
            # show = dict_meg.get(4)
            # status_code = 203
            return jsonify({"msg":"โปรดใส่รหัสผ่าน"})
        else:
            return jsonify({"msg":"Username หรือ Password ผิดพลาด"})
            # show = dict_meg.get(2)
            # status_code = 203
        # return Response(response=json.dumps({"meg": show}), status=status_code)
    except Exception as e:
        print(e)
        return jsonify({"msg":"Username หรือ Password ผิดพลาด"})
        # show = dict_meg.get(3)
        # return Response(response=json.dumps({"meg": show}), status=203)

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
    # data = request.json
    id_user = request.args['id_user']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT date_booking,user.name,tour.name_tour,price,details,date_travel_start,date_travel_end,country.value,history.status FROM history INNER JOIN tour on history.id_tour = tour.id_tour INNER JOIN user on history.id_user = user.id_user INNER JOIN country on tour.id_country = country.id_country WHERE history.id_user = {};".format(id_user)
        mycursor.execute(sql, )
        result = mycursor.fetchall()
        mydb.commit()
        mydb.close()
        return jsonify({"result" : result})
    except Exception as e:
        return "เรียกข้อมูลประวัติการจองทัวร์ไม่สำเร็จ"

def update_history():
    mydb = connectsql()
    data = request.json
    id_history = data['id_history']
    status = data['status']
    test_data_1 = [id_history, status]

    if (check_data(test_data_1) > 0):
        return "กรอกข้อมูลไม่ครบ"
    else:
        try:
            mycursor = mydb.cursor(dictionary=True)
            sql = "UPDATE `history` SET `status`='{}' WHERE `id_history`={};".format(status,id_history)
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
            return "แก้ไขข้อมูลสำเร็จ"
        except Exception as e:
            return str(e)

def edit_password():

    dict_meg = {1:"Success.",2:"Fail.",3:"Old password is wrong",4:"Don't have this username."};
    mydb = connectsql()
    data = request.json
    username = data['username']
    passwd = data['passwd']
    new_password = data['new_password']
    check_new_password = data['check_new_password']
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT passwd FROM user WHERE username = '{}';".format(username)
        mycursor.execute(sql)
        check_passwd = mycursor.fetchone()
        if re.match('^(?=\S{8,16}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', new_password) == None:
            return "รหัสผ่านควรมีตัวเลข ตัวอักษรตัวใหญ่อย่างน้อย 1 ตัว(A-Z) ตัวเล็กอย่างน้อย 1 ตัว(a-z) และมีอักขระพิเศษอย่างน้อย  1 ตัว (!@#$%^&*()_+|~-=\\`{}[]:\";'<>?,./)'"
        elif new_password != check_new_password:
            return "รหัสผ่านใหม่ไม่ตรงกัน"
        else:
            dict = {'username': username, 'passwd': passwd, 'new_password': new_password}
            for i in dict:
                if (dict.get(i) == ""):
                    return Response(response=json.dumps({"meg": "{} is empty".format(i)}), status=203)
                    print new_password + "1"
                elif (passwd == check_passwd.get('passwd')):
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

def report_tour():
    mydb = connectsql()
    mydb1 = connectsql()
    # data = request.json
    date_start = request.args['date']
    date_time_now = datetime.datetime.now()
    Y_ear = date_start.split("-")[0]
    M_onth = date_start.split("-")[1]
    D_ay =  date_start.split("-")[2]
    mycursor = mydb.cursor(dictionary=True)
    mycursor1 = mydb1.cursor(dictionary=True)
    # ปี : เดือน : วัน
    if Y_ear != "00" and M_onth != "00" and D_ay != "00":
        sql = "SELECT COUNT(status) FROM history WHERE date(history.date_booking) = '{}' AND history.status='not paid';".format(date_start)
        sql1 = "SELECT COUNT(status) FROM history WHERE date(history.date_booking) = '{}' AND history.status='paid';".format(date_start)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay" : myresult},{"paid": myresult1 }]))
    # ปี : วัน
    elif Y_ear != "00" and M_onth == "00" and D_ay != "00":
        sql = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND DAY(date(history.date_booking)) = '{}' AND history.status='not paid';".format(Y_ear,D_ay)
        sql1 = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND DAY(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear,D_ay)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # ปี : เดือน
    elif Y_ear != "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(Y_ear,M_onth)
        sql1 = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear,M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # เดือน : วัน
    elif Y_ear != "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth,D_ay)
        sql1 = "SELECT COUNT(status) FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth,D_ay)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # ปี
    elif Y_ear != "00" and M_onth == "00" and D_ay == "00":
        sql = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth,D_ay)
        sql1 = "SELECT COUNT(status) FROM history WHERE YEAR(date(history.date_booking)) = '{}' AND history.status='paid';".format(Y_ear)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # เดือน
    elif Y_ear == "00" and M_onth != "00" and D_ay == "00":
        sql = "SELECT COUNT(status) FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth)
        sql1 = "SELECT COUNT(status) FROM history WHERE MONTH(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    # วัน
    elif Y_ear == "00" and M_onth == "00" and D_ay != "00":
        sql = "SELECT COUNT(status) FROM history WHERE DAY(date(history.date_booking)) = '{}' AND history.status='not paid';".format(M_onth)
        sql1 = "SELECT COUNT(status) FROM history WHERE DAY(date(history.date_booking)) = '{}' AND history.status='paid';".format(M_onth)
        mycursor.execute(sql)
        mycursor1.execute(sql1)
        myresult = mycursor.fetchall()
        myresult1 = mycursor1.fetchall()
        mydb.commit()
        mydb.close()
        mydb1.commit()
        mydb1.close()
        return jsonify(([{"not pay": myresult}, {"paid": myresult1}]))
    else:
        return "ผิด"