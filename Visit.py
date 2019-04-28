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
    query = "DROP TABLE IF EXISTS Visit"
    cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS Visit (
    환자번호 INTEGER, 
    방문유형 CHAR(1),
    입원일 DATE,
    퇴원일 DATE, 
    입원경로 VARCHAR,
    퇴원결과 VARCHAR,
    퇴원장소 VARCHAR)"""
    cur.execute(query)
    conn.commit()

def readCSV() :
    f = open('D:/Yoon/Dongguk/03_20171206_환자방문정보.csv', 'r', encoding = 'UTF-8')
    rdr = csv.reader(f, delimiter = ',')
    data = []
    for row in rdr:
        data.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))  
    f.close()
    return data

def insertData(data) :
    global conn, cur
    query = "INSERT INTO Visit VALUES (?, ?, ?, ?, ?, ?, ?)"
    cur.executemany(query, data)
    conn.commit()

openDB()
createTable()
data = readCSV()
insertData(data)
cur.execute("SELECT * FROM Visit WHERE 퇴원장소 = '영안실'")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()

    