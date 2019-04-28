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
    query = "DROP TABLE IF EXISTS Medication"
    cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS Medication (
    환자번호 INTEGER, 
    오더일 DATE, 
    EDI코드 INTEGER, 
    오더코드 VARCHAR,
    오더명 VARCHAR,
    투약수량 INTEGER,
    투약단위 VARCHAR,
    총투여횟수 INTEGER,
    투여기간 INTEGER,
    투여기간단위 INTEGER)"""
    cur.execute(query)
    conn.commit()

def readCSV() :
    f = open('D:/Yoon/Dongguk/02_201611-201612_투약정보.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(f, delimiter = ',')
    data = []
    for row in rdr:
        data.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))  
    f.close()
    return data

def insertData(data) :
    global conn, cur
    query = "INSERT INTO Medication VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.executemany(query, data)
    conn.commit()

openDB()
# createTable()
# data = readCSV()
# insertData(data)
cur.execute("SELECT * FROM Medication WHERE 환자번호 = 10001072")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

    