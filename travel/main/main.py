# -*- coding: utf-8 -*-
import mysql.connector
from flask import Flask, request

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
        port='3307',
        database='travel_db',
        user='root',
        password='123459876',
        )
        return mydb

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
