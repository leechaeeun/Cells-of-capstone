import csv
import sqlite3

conn = None
cur = None

def openDB() :
    global conn, cur
    database = "CellsOfCapstone.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()

def createTable() :
    # 생성된 테이블 삭제
    # query = "DROP TABLE IF EXISTS Patient"
    # cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS Patient (
    환자번호 INTEGER, 
    방문유형 CHAR(1), 
    진료일 DATE, 
    생년월일 DATE,
    성별 CHAR(1),
    진료과 VARCHAR,
    진료과명 VARCHAR)"""
    cur.execute(query)
    conn.commit()

def readCSV1() :
    file = open('D:/Yoon/Dongguk/01_20171205_환자정보_1.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(file)
    data = []
    for row in rdr:
        data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    file.close()
    return data

def readCSV2() :
    file = open('D:/Yoon/Dongguk/01_20171205_환자정보_2.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(file)
    data = []
    for row in rdr:
        data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    file.close()
    return data

def readCSV3() :
    file = open('D:/Yoon/Dongguk/01_20171205_환자정보_3.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(file)
    data = []
    for row in rdr:
        data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    file.close()
    return data

def insertData(data) :
    global conn, cur
    query = "INSERT INTO Patient VALUES (?, ?, ?, ?, ?, ?, ?)"
    cur.executemany(query, data)
    conn.commit()

openDB()
createTable()
data = readCSV1()
insertData(data)
data = readCSV2()
insertData(data)
data = readCSV3()
insertData(data)
cur.execute("SELECT * FROM Patient WHERE 진료과명 = '외과'")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

    