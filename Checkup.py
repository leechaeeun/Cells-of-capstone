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
    query = "DROP TABLE IF EXISTS Checkup"
    cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS Checkup (
    환자번호 INTEGER, 
    방문유형 CHAR(1),
    방문일 DATE,
    검사명 VARCHAR,
    검체명1 VARCHAR,
    검체명2 VARCHAR,
    검사일시 DATETIME,
    검사결과 FLOAT,
    단위 VARCHAR,
    결과비교 CHAR(1),
    EDI코드 VARCHAR)"""
    cur.execute(query)
    conn.commit()

def readCSV() :
    f = open('D:/Yoon/Dongguk/07_20171211_검사정보.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(f, delimiter = ',')
    data = []
    for row in rdr:
        data.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))  
    f.close()
    return data

def insertData(data) :
    global conn, cur
    query = "INSERT INTO Checkup VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    cur.executemany(query, data)
    conn.commit()

openDB()
createTable()
data = readCSV()
insertData(data)
cur.execute("SELECT * FROM Checkup")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

    