import openpyxl
import sqlite3 as db

conn = None
cur = None
def readexcelfile() :
    file = openpyxl.load_workbook("D:/Yoon/노인 약물 부작용.xlsx")
    sheet = file.worksheets[0]
    data = []
    for row in sheet.iter_rows(min_row = 2):
        data.append((row[0].value, row[1].value,row[2].value,row[3].value,row[4].value))
    return data

def settingdb() :
    global conn, cur
    databasefile = "CellsOfCapstone.db"
    conn = db.connect(databasefile)
    cur = conn.cursor()
    # 생성된 테이블 삭제
    query = "DROP TABLE IF EXISTS DrugSideEffect"
    cur.execute(query)
    # 테이블 생성
    query = """CREATE TABLE IF NOT EXISTS DrugSideEffect (
    약품명 VARCHAR PRIMARY_KEY NOT_NULL, 
    이론적해석 VARCHAR,
    추천 VARCHAR, 
    증거의질 VARCHAR, 
    권고의강점 VARCHAR)"""
    cur.execute(query)
    conn.commit()

def opendb() :
    global conn, cur
    databasefile = "CellsOfCapstone.db"
    conn = db.connect(databasefile)
    cur = conn.cursor()

def inserttodb(data) :
    global conn, cur
    query = "INSERT INTO DrugSideEffect (약품명,이론적해석,추천,증거의질,권고의강점) VALUES (?,?,?,?,?)"
    cur.executemany(query, data)
    conn.commit()

if __name__ == '__main__' :
    opendb()
    settingdb()
    data = readexcelfile()
    inserttodb(data)
    query = "SELECT * FROM DrugSideEffect "
    cur.execute(query)
    print(cur.fetchall())
    cur.close()
    conn.close()