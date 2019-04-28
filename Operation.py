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
    query = "DROP TABLE IF EXISTS Operation"
    cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS Operation (
    환자번호 INTEGER, 
    방문유형 CHAR(1),
    방문일 DATE,
    EDI코드 VARCHAR,
    수술일 DATE)"""
    cur.execute(query)
    conn.commit()

def readCSV() :
    f = open('D:/Yoon/Dongguk/05_20171211_수술정보.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(f, delimiter = ',')
    data = []
    for row in rdr:
        data.append((row[0],row[1],row[2],row[3],row[4]))  
    f.close()
    return data

def insertData(data) :
    global conn, cur
    query = "INSERT INTO Operation VALUES (?, ?, ?, ?, ?)"
    cur.executemany(query, data)
    conn.commit()

openDB()
# createTable()
# data = readCSV()
# insertData(data)
cur.execute("SELECT * FROM Operation")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

    