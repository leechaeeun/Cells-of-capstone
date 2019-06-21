from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from datetime import datetime
import simplejson
import sqlite3, json

# Crieate your views here.
@csrf_exempt
def result(request):
    target_drug  = request.POST.get('drugname')
    conn, cur = openDB("CellsOfCapstone.db")
    
    side_effects = []
    side_effect_json = open('MappingData.json').read()
    data = json.loads(side_effect_json)
    if target_drug in data.keys():
       if data[target_drug] != None:
          side_effects = data[target_drug].split(';')
   
    ## 입력받은 약품을 처방받은 환자 찾기
    medication = []
    id_list = []
    query = "SELECT DISTINCT 환자번호, 오더일, 오더명 FROM Medication WHERE 오더명 like '%"+target_drug+"%'"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        if not (row[0] in id_list):
            medication.append(row)
            id_list.append(row[0])

# 환자번호로 정보찾기
    # - 환자정보 읽어오기
    patient = []
    str_idlist = str(tuple(id_list))
    if len(id_list)==1:
        str_idlist = "("+str(id_list[0])+")"
    query = "SELECT DISTINCT 환자번호,strftime('%Y', 'now') - substr(생년월일, 1, 4) - (strftime('%m-%d', 'now') < substr(생년월일, 6)) As 나이, 성별 FROM Patient WHERE 환자번호 IN"+str_idlist
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        if row[1]>=65:
            patient.append(row)
        else:
            id_list.remove(row[0])

    # 이후의 진단이 있었는지, 진단 중에 부작용에 해당하는 것이 있었는지 확인
    diagnosis = []
    side_effect_cnt = 0
    str_idlist = str(tuple(id_list))
    if len(id_list) == 1:
        str_idlist = "(" + str(id_list[0]) + ")"
    query = "SELECT 환자번호, 진료일, 진단명 FROM Diagnosis WHERE 환자번호 IN "+str_idlist
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        # 해당 환자번호의 처방기록을 불러온다.
        prescription = medication[id_list.index(row[0])]
        if prescription[1] <= row[1]: # 해당 처방기록 이후에 진단된 정보인지 확인
            diagnosis.append(row)
            for effect in side_effects:
                if effect in row[2]:
                    side_effect_cnt = side_effect_cnt + 1
                    break

    if len(id_list)>0:
        avg_age = 0
        side_effect_per = (side_effect_cnt * 100 / len(id_list))
        if side_effect_per != 0:
            for info in patient:
                avg_age = avg_age + info[1]
            avg_age = avg_age/len(patient)
        result = {"drug":target_drug, "side_effect": side_effects, "eld_num":len(id_list), "side_num":side_effect_cnt, "side_per":round(side_effect_per, 2), "avg_age":round(avg_age, 2)}
    else:
        result = {"drug":target_drug, "side_effect": side_effects, "eld_num": 0, "side_num": 0, "side_per": 0.0, "avg_age":0}

    return render(request, 'sunin/result.html', result)

def openDB(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    return conn,cur

def cellsofcapstone_main(request):
    return render(request, 'sunin/cellsofcapstone_main.html',{})

def add_diagnosis(request):
    return render(request, 'sunin/add_diagnosis.html',)

def complete_diagnosis(request):
    conn, cur = openDB("CellsOfCapstone.db")
    ptid = request.POST.get('ptid')
    vtype = request.POST.get('vtype')
    ddate = request.POST.get('date')
    code = request.POST.get('code')
    diagnosis = request.POST.get('diagnosis')
    disease = request.POST.get('disease')

    query = "INSERT INTO Diagnosis VALUES (?,?,?,?,?,?,?)" 
    cur.execute(query,(ptid,vtype,ddate,str(datetime.now().strftime('%Y-%m-%d')),code,diagnosis,disease))

    return render(request, 'sunin/completediagnosis.html',{"ptid":ptid, "vtype":vtype, "ddate": ddate, "code":code, "diagnosis":diagnosis, "disease":disease})

def add_medication(request):
    return render(request, 'sunin/add_medication.html')

def complete_medication(request):
    conn, cur = openDB("CellsOfCapstone.db")

    ptid = request.POST.get('ptid')
    mdate = request.POST.get('mdate')
    ecode = request.POST.get('ecode')
    ocode = request.POST.get('ocode')
    oname = request.POST.get('oname')
    amount = request.POST.get('amount')
    unit = request.POST.get('unit')
    tnum = request.POST.get('tnum')
    period = request.POST.get('period')
    punit = request.POST.get('punit')
    
    query = "INSERT INTO Medication VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query,(ptid, mdate, ecode, ocode, oname, amount, unit, tnum, period, punit))
    
    context = {
        'ptid': ptid,
        'mdate': mdate,
        'ecode': ecode,
        'ocode': ocode,
        'oname': oname,
        'amount': amount,
        'unit': unit,
        'tnum': tnum,
        'period': period,
        'punit': punit
    }
    
    return render(request, 'sunin/completemedication.html', context)
