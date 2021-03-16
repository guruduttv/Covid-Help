
from django.contrib import messages
from django.db import connection
from django.shortcuts import render

from .models import At_Risk

from .models import Hospitals
from .models import Locations
from .models import Hospital_phones
import random

from .models import Totalcases
from .models import District
from .models import State_wise
from .models import Self_assess
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from .forms import selfassessment
import smtplib, ssl

import requests
urban=[560063,560107,560007,560092,560024,560045,560064,560047,560073,560043,560001,560002,560009,560001,560091,560079,560046,562157,
560049,560063,560092,560089,560093,560040,560090,560073,560025,560064,562162,560036,560077,560037,560071,560016,560001,560077,560005,560065,
560051,560104,560024,560091,560088,560089,560001,560048,560043,560008,560038,560010,560094,560006,560064,560013, 560021,560087,560024,560008,
560014,560015,560043,560046,560075,560079,560009,560089,560043,560079,560092,560077,560036,560016,560037,560058,560001,
560084,562162,560023,560048,560086,560001,560003,560055,560037,560033,560054,560054,560025,560072,560073,560017,
560096,560073,560075,560032,560003,560057,560058,560058,560032,560094,560010,560010,560064,560001,560016,560037,
560025,560080,560092,560012,560020,560089,560090,560064,560042,560054,560021,560084,560003,560090,560006,560045,
560001,560097,560040,560040,560017,560049,560091,560003,560086,560064,560022,560022]

try:
    url="https://www.covidbeds.org/"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title
    links = soup.find_all('a', href=True)
    f = soup.find_all('h3')
    y = str(f[0])
    Num = re.compile(r'\d* hospitals')
    mo = Num.search(y)
    m1 = mo.group()
    mo1 = re.compile(r'\d\d*')  # extracting number of hospitals
    mo2 = mo1.search(m1)
    no = int(mo2.group())
    data = []
    allrows = soup.find_all("tr")
    pincode = []
    pincodes = []
    phonenumbers = []
    for rows in allrows:
        row_list = rows.find_all("td")
        datarow = []
        for i in range(len(row_list)):
            datarow.append(row_list[i].text)
            if i == 2:
                if row_list[i]:
                    ph = []
                    t = row_list[i].text
                    t.strip()
                    str = t.split("/")
                    for i in range(len(str)):
                        str[i].lstrip()
                        str[i].rstrip()
                        text = str[i].strip()
                        if " " not in text:
                            ph.append(int(text))
                        else:
                            t = text.split()
                            y = ''.join(t)
                            ph.append(y)
                    phonenumbers.append(ph)

            if i == 3:
                pin = row_list[i].text
                pin1 = re.search(r'56[0-9][0-9][0-9][0-9]', pin)
                if pin1 == None:
                    continue
                else:
                    pincode.append(int(pin1.group()))
        data.append(datarow)
    dest = []
    for i in range(0, len(pincode)):
        if (pincode[i] in urban):
            p = Locations(pincode=pincode[i], zone="Urban")
        else:
            p = Locations(pincode=pincode[i], zone="Rural")
        p.save()
    for i in range(1, no + 1):
        st = "Full" if data[i][1] == "Full" else "Available"

        t = Hospitals(hosp_id=i, name=data[i][0], address=data[i][3], pincodes=Locations(pincode=pincode[i - 1]),
                     status=st)

        t.save()

    for j in range(len(phonenumbers)):
        t = phonenumbers[j][0]

        ph = Hospital_phones(sl_no=j + 1, h_id=Hospitals(hosp_id=(j + 1)), phno=t)
        ph.save()

except:
    pass
t=Hospitals.objects.all()

beds =[]
hosp_id =[]
name=[]
address=[]
status =[]
pincodes=[]
for i in t:

    # print(i.hosp_id,i.name,i.address,i.status,i.pincodes)
    hosp_id.append(i.hosp_id)
    name.append(i.name)
    address.append(i.address)
    status.append(i.status)
    pin1 = re.search(r'56[0-9][0-9][0-9][0-9]', i.address)
    # print(int(pin1.group()))
    pincodes.append(int(pin1.group()))

condition=True

while(condition):
    try:
        result = requests.get("https://api.rootnet.in/covid19-in/stats/latest")
        Global=result.json()['data']['summary']
        Regional=result.json()['data']['regional']
        condition=False
    except:
            condition=True

glob = Totalcases.objects.all()
glob.delete()
global_obj = Totalcases(total_case=Global["total"], total_discharged=Global["discharged"],
                           total_deaths=Global["deaths"])
glob = Totalcases.objects.all()

global_obj.save()
for i in Regional:
    regional_obj = State_wise(state=i["loc"],state_discharged=i["confirmedCasesIndian"] + i["confirmedCasesForeign"],
                            state_case=i["discharged"], state_deaths=i["deaths"])
    regional_obj.save()
condition = True
res = At_Risk.objects.all()
res.delete();
res = Self_assess.objects.all()
res.delete()

while (condition):
    try:
        result = requests.get("https://api.covid19india.org/state_district_wise.json")
        district = result.json()['Karnataka']['districtData']
        condition = False
    except:
        condition = True
    for i, k in district.items():
        regional_obj = District(district_name=i, total_cases=k['confirmed'], active_cases=k['active'],cured=k['recovered'], death=k['deceased'])
        regional_obj.save()

def index(request):
    glob = Totalcases.objects.all()

    reg = State_wise.objects.all()
    return render(request, "in.html",{"glob":glob,"reg":reg})

def selfs(request):
    if request.method=="POST":
        fm=selfassessment(request.POST)
        if fm.is_valid():
            ag=fm.cleaned_data['age']
            sy=fm.cleaned_data['sym']
            di = fm.cleaned_data['dis']
            trav = fm.cleaned_data['travel']
            app = fm.cleaned_data['apply']
            # mail = fm.cleaned_data['email']
            ph=fm.cleaned_data['phno']
            if ag > 0 and sy == 'None of these' and di == 'None of these' and trav == 'No' and app == "None of these":
                # res1 = Self_ass(phno=ph,email=mail,age=ag, symptoms=sy, disease=di, travelled=trav, applies=app, result="Low")
                # res1.save()
                obj, created = Self_assess.objects.update_or_create(
                    phno=ph,
                    defaults={'phno':ph,'age':ag, 'symptoms':sy, 'disease':di, 'travelled':trav, 'applies':app, 'result':"Low"}
                    # defaults={'phno':ph,'email':mail,'age':ag, 'symptoms':sy, 'disease':di, 'travelled':trav, 'applies':app, 'result':"Low"}
                )

            if ag > 0 and ((sy != 'None of these' or sy == 'More than one of above symptoms') or (
                    di != 'None of these' or di == 'More than one of above mentioned diseases') or trav== 'Yes' and app != "None of these"):
                # res1 = Self_ass(phno=ph, email=mail, age=ag, symptoms=sy, disease=di, travelled=trav, applies=app,
                #                    result="High")
                # res1.save()
                obj, created = Self_assess.objects.update_or_create(
                    phno=ph,
                    defaults={ 'phno':ph, 'age': ag, 'symptoms': sy, 'disease': di, 'travelled': trav,
                              'applies': app, 'result': "High"}
                )
            messages.success(request, 'Form submission successful')

            return result(request)
    else:
        fm=selfassessment()
    return render(request, "self.html", {"fm":fm})
def result(request):
    res = Self_assess.objects.all()


    res1=res[len(res)-1]

    if res1.age > 0 and res1.symptoms == 'None of these' and res1.disease == 'None of these' and res1.travelled == 'No' and res1.applies == "None of these":
        messages.success(request,
                         "Your infection risk is low.We recommend that you stay at home to avoid any chances of exposure to the novel Coronavirus. ")
    elif res1.age>0 and ((res1.symptoms != 'None of these' or res1.symptoms == 'More than one of above symptoms') or  (res1.disease != 'None' or res1.disease == 'More than one of above mentioned diseases') or  res1.travelled == 'Yes' or res1.applies != "None of these"):

        messages.success(request,
                         'If the information you have provided is accurate, it indicates that you are either unwell or at risk.It is advised to isolate yourself for 14 days or get medical help immediately(call 1075 ) .')


    res = At_Risk.objects.all()
    l=len(res)
    # print (l)
    # if l!=0:
    #     res=res[l-1]
    #     t =  res.phno + ", " + res.symptom+"," +res.disease+","+res.travel+","+res.apply+ "\n"
    #     from twilio.rest import Client
    #     account_sid = 'AC6bcce05356a6db2afafbc22be6f7f171'
    #     auth_token = 'cdd0b06d2a8eec2c8d145a43dd057331'
    #     client = Client(account_sid, auth_token)
    #     message = client.messages.create(
    #     from_='whatsapp:+14155238886',
    #     body=t,
    #     to='whatsapp:+919480703113'
    #     )
    #     print(message.sid)
    return  render(request, "result.html",{"res1":res1})

def karnataka(request):
    reg = State_wise.objects.all()
    reg=reg[15]
    dis = District.objects.all()
    return render(request, "karnataka.html", {"reg":reg,"dis":dis})



def district(request):
    dis = District.objects.all()
    return render(request, "district.html", { "dis": dis})

def covid(request):
    return render(request, "COVID.html")

def banghosp(request):
    # query = 'select hosp_id, name, address, pincodes_id, status, zone, phno,beds from c_hospitals, c_locations, c_hospital_phones where pincodes_id = pincode and h_id_id = hosp_id ORDER BY hosp_id ASC;'
    # all = Hospital.objects.raw(query)
    with connection.cursor() as cursor:
        cursor.execute('call HOSP()')
        result = cursor.fetchall()
    a = []
    for i in list(result):
        s = []
        for j in i:
            s.append(j)
        a.append(s)
    return render(request, "banghosp.html",{"a":a})
def bangurban(request):

    with connection.cursor() as cursor:
        cursor.execute('call Urban()')
        result=cursor.fetchall()
    a=[]
    for i in list(result):
        s=[]
        for j in i:

            s.append(j)
        a.append(s)
    return render(request, "bangurban.html",{"a":a})
def bangrural(request):
    with connection.cursor() as cursor:
        cursor.execute('call Rural()')
        result=cursor.fetchall()
    a=[]
    for i in list(result):
        s=[]
        for j in i:

            s.append(j)
        a.append(s)
    return render(request, "bangrural.html",{"a":a})

def more(request):
    return render(request, "more.html")
