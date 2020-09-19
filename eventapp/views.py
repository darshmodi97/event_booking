from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from mysql.connector import Error
import mysql.connector
from django.core.mail import EmailMessage
import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from datetime import date, datetime, time, timedelta
import datetime


def index(request):
    happy_client(request)
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def gallery(request):
    return render(request,'gallery.html')

def show_events(request):
    return render(request,'events.html')

def register_landowner(request):
    return render(request,'register_for_land_owner.html')

def register_cateringowner(request):
    return render(request,'register_for_catering_owner.html')

def register_client(request):
    return render(request,'client_register.html')

def header_landowner(request):
    return render(request,'dashboard_of_landowner.html')

def header_caterer(request):
    return render(request,'catering_dashboard.html')

def header_client(request):
    return render(request,'client_dashboard.html')

def header_admin(request):
    return render(request,'admin_dashboard.html')

def giveconnect(request):
    conn = mysql.connector.connect(host='localhost', database='event_booking', user='root', password='root',auth_plugin='mysql_native_password')
    return conn

def client_dashboard(request):
    conn = giveconnect(request)
    cursor = conn.cursor()
    name = request.POST.get('Name')
    mobile =int(request.POST.get('mobile'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    cpassword = request.POST.get('cpassword')
    request.session['roll_id'] = 3
    if password == cpassword :
        query = " insert into login_table(username,password,roll_id) values ('%s','%s',3)" %(username,password)
        cursor.execute(query)
        login_id = int(cursor.lastrowid)
        print(login_id)

        request.session['login_id'] = login_id

        query1 = " insert into client_reg(client_name,mobile_number,login_id) values ('%s',%d,%d)" %(name,mobile,login_id)
        cursor.execute(query1)
        print("inserted")
        query2 = "select * from vanue_category"
        print("query2")
        cursor.execute(query2)
        print("executed")
        rows = cursor.fetchall()
        print("fetched")
        conn.commit()
        print("commited")
        request.session['client_id'] = cursor.lastrowid
        request.session['name'] = name
        happy_client(request)
    return render(request, "client_dashboard.html", {'data':rows,'name':name})

def catering_dashboard(request):

        conn = giveconnect(request)
        cursor = conn.cursor()
        name = request.POST.get('Name')
        mobile = int(request.POST.get('mobile'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        gstno = int(request.POST.get('gstno'))
        request.session['name'] = name
        request.session['roll_id'] = 2
        if password == cpassword :
            query = " insert into login_table(username,password,roll_id) values ('%s','%s',2)" %(username,password)
            cursor.execute(query)
            login_id = int(cursor.lastrowid)
            print(login_id)

            request.session['login_id'] = login_id

            query1 = " insert into catering_owner_reg(catering_owner_name,mobile_number,gst_no,login_id) values ('%s',%d,%d,%d)" %(name,mobile,gstno,login_id)
            cursor.execute(query1)
            cat_owner_id = cursor.lastrowid
            request.session['catering_owner_id'] = cat_owner_id
            if request.POST.get('spec1') == 'punjabi' :
                query2 ="INSERT INTO catering_category_mapping (catering_owner_id,catering_category_id) VALUES (%d,1);" %(cat_owner_id)
                cursor.execute(query2)

            if request.POST.get('spec2') == 'chinese' :
                query3 ="INSERT INTO catering_category_mapping (catering_owner_id,catering_category_id) VALUES (%d,2);" %(cat_owner_id)
                cursor.execute(query3)

            if request.POST.get('spec3') == 'gujarati' :
                query4 ="INSERT INTO catering_category_mapping (catering_owner_id,catering_category_id) VALUES (%d,3);" %(cat_owner_id)
                cursor.execute(query4)

            if request.POST.get('spec4') == 'italian' :
                query5 ="INSERT INTO catering_category_mapping (catering_owner_id,catering_category_id) VALUES (%d,4);" %(cat_owner_id)
                cursor.execute(query5)

            if request.POST.get('spec5') == 'maxican' :
                query6 ="INSERT INTO catering_category_mapping (catering_owner_id,catering_category_id) VALUES (%d,5);" %(cat_owner_id)
                cursor.execute(query6)

            conn.commit()
            happy_client(request)
            Name =request.session.get('name')
        return render(request,'catering_dashboard.html',{'name':Name})

def land_owner_dashboard(request):
    conn = giveconnect(request)
    cursor = conn.cursor()
    name = request.POST.get('Name')
    mobile = int(request.POST.get('mobile'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    cpassword = request.POST.get('cpassword')
    gstno = int(request.POST.get('gstno'))
    # request.session['roll_id'] = 1

    if password == cpassword:
        query = " insert into login_table(username,password,roll_id) values ('%s','%s',1)" % (username, password)
        cursor.execute(query)
        login_id = int(cursor.lastrowid)
        print(login_id)

        request.session['login_id'] =login_id

        query1 = " insert into land_owner_reg(land_owner_name,mobile_number,login_id,gst_no) values ('%s',%d,%d,%d)" \
                 % (name, mobile,login_id,gstno)
        cursor.execute(query1)
        request.session['land_owner_id'] = cursor.lastrowid
        conn.commit()
        happy_client(request)
        request.session['name'] = name
        return render(request,'dashboard_of_landowner.html')
    else:
        msg = "password and confirm password is not same "
        print(msg)
        return register_landowner(request)

def login(request):
    return render(request,'login.html')

def signin(request):
        conn = giveconnect(request)
        cursor = conn.cursor()
        username = request.POST.get('username')
        password = request.POST.get('pass')
        query1 = "select login_id,roll_id,username from login_table where username ='%s'" %(username)
        cursor.execute(query1)
        r1 = cursor.fetchone()
        print(r1)
        if r1:
            request.session['username'] = r1[2]
            print('session created')
            query = "select login_id,roll_id,username from login_table where username ='%s' and password ='%s'" %(username, password)
            cursor.execute(query)
            r = cursor.fetchone()
            print(r)
            if r :
                request.session['login_id'] =r[0]
                print(r[0])
                if r[1]==1 :
                    # request.session['roll_id'] = 1
                    query1 = "select land_owner_reg.land_owner_name,land_owner_reg.land_owner_id from land_owner_reg where login_id =%d" %(r[0])
                    cursor.execute(query1)
                    row =cursor.fetchone()

                    request.session['name']=row[0]
                    request.session['land_owner_id'] =row[1]
                    # happy_client(request)
                    print("in land owner")

                    return render(request, "dashboard_of_landowner.html")
                elif r[1]==2 :
                    query1 = "select catering_owner_name,catering_owner_id from catering_owner_reg where login_id =%d" %(r[0])
                    cursor.execute(query1)
                    row = cursor.fetchone()
                    # request.session['roll_id'] = 2
                    request.session['name'] = row[0]
                    request.session['catering_owner_id'] = row[1]
                    happy_client(request)
                    return render(request, 'catering_dashboard.html')
                elif r[1]==3 :
                    query1 = "select client_reg.client_name,client_reg.client_id from client_reg where login_id=%d" %(r[0])
                    cursor.execute(query1)
                    row = cursor.fetchone()
                    request.session['roll_id'] = r[1]
                    request.session['name'] = row[0]
                    request.session['client_id'] = row[1]
                    happy_client(request)
                    return render(request,'client_dashboard.html')
                elif r[1]:
                    name ='Admin'
                    request.session['name']=name
                    return render(request,'admin_dashboard.html')
            else:
                    msg='Invalid password ..'
                    return render(request, 'login.html', {'msg': msg})
        else :
            msg ="Invalid Username .."
            return render(request,'login.html',{'msg':msg} )

def logout(request):
    request.session.clear()
    return render(request,'login.html')

def forget(request):

    return render(request,'forget_password.html')

def sendmail(request):
    try:
        username =request.session.get('username')
        email = request.POST.get('email')
        print(email)

        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select username,password from login_table where username ='%s' " % (username)
        cursor.execute(query)
        row = cursor.fetchone()
        print("data from login table during send mail : ",row)
        subject = "Regarding your password ..."
        body = "We are here to Help you , we suggest you to use following password to log into your account for username :'%s' ." \
               "your password is : '%s' "%(row[0],row[1])
        print(body)
        msg = EmailMessage( subject, body,to=[email])
        print("to :",msg.to)
        msg.send()
        print(msg.body)
        return HttpResponse("Mail successfully sent")
    except:
        print("exception occured")
        return HttpResponse(" Failed to send mail ..")


def view_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        query = "select land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "login_table.username," \
                "land_owner_reg.gst_no," \
                "login_table.password " \
                "from login_table " \
                "join land_owner_reg on login_table.login_id = land_owner_reg.login_id " \
                "where login_table.login_id = %d;" % (lid)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        return render(request, 'view_landowner.html', {'data': rows})
    else :
        return render(request, 'login.html')

def edit_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        name = request.POST.get('Name')
        mobile = int(request.POST.get('mobile'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        gstno = int(request.POST.get('gstno'))
        query = "update land_owner_reg,login_table set land_owner_reg.land_owner_name = '%s' ," \
                "land_owner_reg.mobile_number=%d , " \
                "land_owner_reg.gst_no ='%s' ," \
                "login_table.username ='%s'," \
                " login_table.password ='%s'" \
                "where land_owner_reg.login_id=%d and login_table.login_id=%d;" %(name,mobile,gstno,username,password,lid,lid)
        cursor.execute(query)
        conn.commit()
        print('profile edited')
        return view_landowner(request)
    else:
        return render(request,'login.html')

def delete_landowner(request):
    conn = giveconnect(request)
    cursor = conn.cursor()
    lid = int(request.session.get('login_id'))
    query = "delete login_table ,land_owner_reg " \
            "from login_table ,land_owner_reg " \
            "where login_table.login_id =%d and land_owner_reg.login_id=%d;" % (lid,lid)
    cursor.execute(query)
    conn.commit()
    request.session.clear()
    return HttpResponse('Your Account is Deleted Successfully')

def view_client(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        query ="select client_reg.client_name,client_reg.mobile_number,login_table.username,login_table.password " \
               "from login_table " \
               "join client_reg on client_reg.login_id = login_table.login_id " \
               "where login_table.login_id=%d " %(lid)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        return render(request, 'view_client.html', {'data': rows})
    else :
        return render(request, 'login.html')

def edit_client(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        name = request.POST.get('Name')
        mobile = int(request.POST.get('mobile'))
        username = request.POST.get('username')
        password = request.POST.get('password')

        query = "update client_reg,login_table " \
                "set client_reg.client_name = '%s' ," \
                "client_reg.mobile_number=%d ," \
                "login_table.username ='%s' ," \
                "login_table.password ='%s' " \
                "where client_reg.login_id=%d and login_table.login_id=%d;" %(name,mobile,username,password,lid,lid)
        cursor.execute(query)
        conn.commit()
        print('profile edited')
        return view_client(request)
    else:
        return render(request,'login.html')

def delete_client(request):
    conn = giveconnect(request)
    cursor = conn.cursor()
    lid = int(request.session.get('login_id'))
    query = "delete login_table ,client_reg " \
            "from login_table ,client_reg " \
            "where login_table.login_id =%d and client_reg.login_id=%d;" % (lid,lid)
    cursor.execute(query)
    conn.commit()
    request.session.clear()
    return HttpResponse('Your Account is Deleted Successfully')

def view_catering(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "login_table.username," \
                "catering_owner_reg.gst_no," \
                "login_table.password " \
                "from login_table " \
                "join catering_owner_reg on catering_owner_reg.login_id = login_table.login_id " \
                "where login_table.login_id=%d" % (lid)
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        return render(request, 'view_caterer.html', {'data': rows})
    else:
        return render(request,'login.html')

def edit_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        lid = int(request.session.get('login_id'))
        print(lid)
        name = request.POST.get('Name')
        mobile = int(request.POST.get('mobile'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        gstno = int(request.POST.get('gstno'))
        query = "update catering_owner_reg,login_table " \
                "set catering_owner_reg.catering_owner_name = '%s' ," \
                "catering_owner_reg.mobile_number=%d , " \
                "catering_owner_reg.gst_no =%d ," \
                "login_table.username ='%s', " \
                "login_table.password ='%s' " \
                "where catering_owner_reg.login_id=%d and login_table.login_id=%d;" %(name,mobile,gstno,username,password,lid,lid)
        cursor.execute(query)
        conn.commit()
        print('profile edited')
        return view_catering(request)
    else:
        return render(request,'login.html')

def delete_caterer(request):
    conn = giveconnect(request)
    cursor = conn.cursor()
    lid = int(request.session.get('login_id'))
    query = "delete login_table ,catering_owner_reg " \
            "from login_table ,catering_owner_reg " \
            "where login_table.login_id =%d and catering_owner_reg.login_id=%d;" % (lid,lid)
    cursor.execute(query)
    conn.commit()
    request.session.clear()
    return HttpResponse('Your Account is Deleted Successfully')

def add_venue(request):
    return render(request,'add_venue.html')

def register_venue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        vanue_name = request.POST.get('name')
        address = request.POST.get('address')
        vanue_sqft = int(request.POST.get('sqft'))
        capacity = int(request.POST.get('capacity'))
        price = int(request.POST.get('price'))
        lid = int(request.session.get('login_id'))
        query =  "select land_owner_id from land_owner_reg where login_id=%d" %(lid)
        cursor.execute(query)
        row = cursor.fetchone()
        if row :
            query1 = "insert into vanue_table (vanue_name,address,sqft,capacity,land_owner_id,price_per_hour) " \
                    "values ('%s','%s',%d,%d,%d,%d) " %(vanue_name,address,vanue_sqft,capacity,row[0],price)
            cursor.execute(query1)
            vanue_id =int(cursor.lastrowid)
            if request.POST.get('birthday') == 'birthday':
                query2 = "insert into vanue_category_mapping(vanue_category_id,vanue_id) values (1,%d)" %(vanue_id)
                cursor.execute(query2)

            if request.POST.get('sangeet') == 'sangeet':
                query3 = "insert into vanue_category_mapping(vanue_category_id,vanue_id) values (2,%d)" % (vanue_id)
                cursor.execute(query3)

            if request.POST.get('wedding') == 'wedding':
                query4 = "insert into vanue_category_mapping(vanue_category_id,vanue_id) values (3,%d)" % (vanue_id)
                cursor.execute(query4)

            if request.POST.get('newyear') == 'newyearparty':
                query5 = "insert into vanue_category_mapping(vanue_category_id,vanue_id) values (4,%d)" % (vanue_id)
                cursor.execute(query5)

            if request.method == 'POST' and request.FILES.getlist('image'):
                print(request.FILES.getlist('image'))
                for upfile in request.FILES.getlist('image'):
                    onefile = upfile.name
                    print("file in loop ", onefile)
                    print("Files----", onefile)
                    v_name = request.POST.get('name')
                    fs = FileSystemStorage()
                    extension = onefile.split('.')  # split() will return list..
                    print("Extension=====", extension)
                    uploaded_file_name = v_name + "." + extension[1]  # extension is of class list ..
                    filename = fs.save(uploaded_file_name, upfile)
                    print("uploaded_file_name", filename)
                    uploaded_file_url = fs.url(filename)
                    print("uploaded_file_url", uploaded_file_url)

                    query = " INSERT INTO vanue_image_mapping (vanue_id,image_path) VALUES(%d,'%s') " % (
                    vanue_id, uploaded_file_url)
                    cursor.execute(query)
            conn.commit()
            msg= 'Venue Request sent to Admin  ..'
            return render(request,'add_venue.html',{'msg':msg})
        else:
            return HttpResponse('Error occured ...')

def get_events(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select * from vanue_table " \
                "join vanue_image_mapping on vanue_table.vanue_id = vanue_image_mapping.vanue_id " \
                "where vanue_table.status = 'Requested' "
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        return render(request, 'get_vanues.html', {'data':rows})
    else :
        return render(request, 'login.html')

def get_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select * from land_owner_reg where status ='Requested' "
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        return render(request,'get_landowners.html',{'data':rows})
    else :
        return render(request, 'login.html')

def get_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select * from catering_owner_reg where status = 'Requested'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_caterers.html',{'data':rows})
    else :
        return render(request, 'login.html')

def accept_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE land_owner_reg SET status = 'Accepted' WHERE land_owner_id = %d" %(id)
        cursor.execute(query)
        conn.commit()
        return get_landowner(request)
    else:
        return render(request, 'login.html')

def reject_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE land_owner_reg SET status = 'Rejected' WHERE land_owner_id = %d" % (id)
        cursor.execute(query)
        conn.commit()
        return get_landowner(request)
    else:
        return render(request, 'login.html')

def accept_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE catering_owner_reg SET status = 'Accepted' WHERE catering_owner_id = %d" %(id)
        cursor.execute(query)
        conn.commit()
        return get_caterer(request)
    else:
        return render(request, 'login.html')

def reject_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE catering_owner_reg SET status = 'Rejected' WHERE catering_owner_id = %d" % (id)
        cursor.execute(query)
        conn.commit()
        return get_caterer(request)
    else:
        return render(request, 'login.html')

def birthday_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query ="select vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 1 and land_owner_reg.status ='Accepted' and vanue_table.status ='Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'birthday_vanues.html',{'data':rows})
    else:
        return render(request,'login.html')

def wedding_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 3 and land_owner_reg.status ='Accepted' and vanue_table.status ='Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'wedding_vanues.html', {'data': rows})
    else:
        return render(request, 'login.html')

def sangeet_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 2 and land_owner_reg.status ='Accepted' and vanue_table.status ='Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'sangeet_vanues.html', {'data': rows})
    else:
        return render(request, 'login.html')

def newyear_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 4 and land_owner_reg.status ='Accepted' and vanue_table.status ='Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'newyear_vanues.html', {'data': rows})
    else:
        return render(request, 'login.html')

def client_birthday_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query ="select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 1 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'client_birthday_vanues.html',{'data':rows})
    else:
        return render(request,'login.html')

def vanue_booking(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.GET.get('id'))
        request.session['vanue_id'] = id
        query ="select vanue_table.vanue_name," \
               "vanue_table.address," \
               "vanue_table.sqft," \
               "vanue_table.capacity," \
               "vanue_table.price_per_hour," \
               "land_owner_reg.mobile_number " \
               "from vanue_table " \
               "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id  " \
               "where vanue_table.vanue_id =%d "%(id)
        cursor.execute(query)
        rows = cursor.fetchone()
        return render(request,'vanue_booking_form.html',{'data':rows})
    else:
        return render(request,'login.html')

def client_book_venue(request):
    print("called")
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        date = request.POST.get('date')
        print('date :',date)
        end_date = request.POST.get('enddate')
        print('End date:',end_date)
        start_time = request.POST.get('starttime')
        print('start time :',start_time)
        end_time = request.POST.get('endtime')
        print('end time :',end_time)
        request.session['date'] =date

        lid = int(request.session.get('login_id'))
        print("login id " ,lid)

        vanue_id =int(request.session.get('vanue_id'))
        print("Vanue id " ,vanue_id)

        query = "select client_reg.client_id from client_reg where login_id = %d;" %(lid)
        cursor.execute(query)
        rows = cursor.fetchone()
        print("Client id " , rows[0])
        q = "select date from vanue_booking where date = '%s' and vanue_id = %d" %(date,vanue_id)
        cursor.execute(q)
        row = cursor.fetchall()
        print("date ",row)
        if row:
            msg = "Vanue is not Available for that day .."
        else:

            query1 = "insert into vanue_booking(booked_by_client_id,vanue_id,date,start_time,end_time,end_date) " \
                     "values (%d,%d,'%s','%s','%s','%s')" % (rows[0], vanue_id, date, start_time, end_time,end_date)
            cursor.execute(query1)
            conn.commit()
            vanue_booked_id = cursor.lastrowid
            request.session['vanue_booked_id'] = vanue_booked_id
            msg = "Vanue Booked Successfully .."

        #     find number of hours ..
            end= (end_date.split('-'))

            # for days..
            year = int(end[0])
            month = int(end[1])
            day = int(end[2])

            start = (date.split('-'))
            # for days..
            year1 = int(start[0])
            month1 = int(start[1])
            day1 = int(start[2])

            et = (end_time.split(':'))
            # for time ..
            end_h = int(et[0])
            end_m = int(et[1])

            st = (start_time.split(':'))
            # for time ..
            start_h = int(st[0])
            start_m = int(st[1])

            a= datetime.datetime(year,month,day,end_h,end_m)
            b= datetime.datetime(year1,month1,day1,start_h,start_m)
            diff = a-b
            print(type(diff))
            print(diff)
            print(diff.days)
            print(diff.seconds)
            hours = (diff.days*24)+(diff.seconds /3600)

        # # select amount per hour from vanue where vanueid=vanue_id
            query2 = "select price_per_hour from vanue_table where vanue_id =%d;" % (vanue_id)
            cursor.execute(query2)
            price = cursor.fetchone()
            totalAmount = price[0]  * hours
            print("Total cost :",totalAmount)
        # send totalAmount in func param
            request.session['f'] = 1
            print(type(request.session.get('flag')))

            return payment(request,totalAmount)

        # return HttpResponse("Error Found..")
        return render(request, 'vanue_booking_form.html', {'msg': msg})
    else:
        return render(request,'login.html')

def client_wedding_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query ="select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 3 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'client_wedding_vanues.html',{'data':rows})
    else:
        return render(request,'login.html')

def client_sangeet_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query ="select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 2 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'client_sangeet_vanues.html',{'data':rows})
    else:
        return render(request,'login.html')

def client_newyear_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query ="select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 4 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' "
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'client_newyear_vanues.html',{'data':rows})
    else:
        return render(request,'login.html')

def booked_vanues(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.session.get('client_id'))
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "vanue_image_mapping.image_path," \
                "vanue_booking.end_date " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_booking.status = 'paid' and vanue_booking.booked_by_client_id = %d ;" %(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'booked_vanues.html', {'data': rows})
    else:
        return render(request, 'login.html')

def blocked_user(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select * from land_owner_reg where status = 'Rejected';"
        cursor.execute(query)
        rows = cursor.fetchall()
        query1 = "select * from catering_owner_reg where status = 'Rejected';"
        cursor.execute(query1)
        row = cursor.fetchall()
        return render(request,'blocked_user.html',{'data':rows,'data1':row})
    else:
        return render(request, 'login.html')

def Accept_landowner(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE land_owner_reg SET status = 'Accepted' WHERE land_owner_id = %d" %(id)
        cursor.execute(query)
        conn.commit()
        return blocked_user(request)
    else:
        return render(request, 'login.html')

def Accept_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE catering_owner_reg SET status = 'Accepted' WHERE catering_owner_id = %d" %(id)
        cursor.execute(query)
        conn.commit()
        return blocked_user(request)
    else:
        return render(request, 'login.html')

def admin_booked_vanues(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "vanue_image_mapping.image_path," \
                "client_reg.client_name " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "join client_reg on client_reg.client_id = vanue_booking.booked_by_client_id " \
                "WHERE vanue_booking.status = 'paid' and date > curdate();"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'admin_booked_vanues.html', {'data': rows})
    else:
        return render(request, 'login.html')

def accept_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE vanue_table SET status = 'Accepted' WHERE vanue_id = %d" %(id)
        cursor.execute(query)
        conn.commit()
        return get_events(request)
    else:
        return render(request, 'login.html')

def reject_vanue(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id= int(request.GET.get('id'))
        print(id)
        query = "UPDATE vanue_table SET status = 'Rejected' WHERE vanue_id = %d" % (id)
        cursor.execute(query)
        conn.commit()
        return get_events(request)
    else:
        return render(request, 'login.html')

def category_caterer(request):
        return render(request,'category_caterer.html')

def get_punjabi_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        category = "Punjabi"

        request.session['catering_category_id'] =1
        request.session['caterer_category'] = category

        query = "select catering_owner_reg.catering_owner_id,catering_owner_reg.catering_owner_name, catering_owner_reg.mobile_number,catering_owner_reg.gst_no " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "where catering_category_mapping.catering_category_id = 1 and catering_owner_reg.status ='Accepted';"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_punjabi_caterer.html',{'data':rows})
    else:
        return render(request, 'login.html')

def get_chinese_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        category = "Chinese"
        request.session['catering_category_id'] = 2
        request.session['caterer_category'] = category

        query = "select catering_owner_reg.catering_owner_id,catering_owner_reg.catering_owner_name, catering_owner_reg.mobile_number,catering_owner_reg.gst_no " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "where catering_category_mapping.catering_category_id = 2 and catering_owner_reg.status ='Accepted' ;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_chinese_caterer.html',{'data':rows})
    else:
        return render(request, 'login.html')

def get_gujarati_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        category = "Gujarati"
        request.session['catering_category_id'] = 3
        request.session['caterer_category'] = category

        query = "select catering_owner_reg.catering_owner_id,catering_owner_reg.catering_owner_name, catering_owner_reg.mobile_number,catering_owner_reg.gst_no " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "where catering_category_mapping.catering_category_id = 3 and catering_owner_reg.status ='Accepted' ;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_gujarati_caterer.html',{'data':rows})
    else:
        return render(request, 'login.html')

def get_italian_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        category = "Italian"
        request.session['catering_category_id'] = 4
        request.session['caterer_category'] = category

        query = "select catering_owner_reg.catering_owner_id,catering_owner_reg.catering_owner_name, catering_owner_reg.mobile_number,catering_owner_reg.gst_no " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "where catering_category_mapping.catering_category_id = 4 and catering_owner_reg.status ='Accepted' ;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_italian_caterer.html',{'data':rows})
    else:
        return render(request, 'login.html')

def get_maxican_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        category = "Maxican"
        request.session['catering_category_id'] = 5
        request.session['caterer_category'] = category

        query = "select catering_owner_reg.catering_owner_id,catering_owner_reg.catering_owner_name, catering_owner_reg.mobile_number,catering_owner_reg.gst_no " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "where catering_category_mapping.catering_category_id = 5 and catering_owner_reg.status ='Accepted' ;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'get_maxican_caterer.html',{'data':rows})
    else:
        return render(request, 'login.html')

def catering_booking(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        caterer_id = int(request.GET.get('id'))
        request.session['caterer_id'] =caterer_id
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "catering_owner_reg.gst_no," \
                "catering_category.price " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                "where catering_owner_reg.catering_owner_id = %d;" %(caterer_id)
        cursor.execute(query)
        rows = cursor.fetchone()
        return render(request,'catering_booking_form.html',{'data':rows})
    else:
        return render(request, 'login.html')


def checkdate(request):
    try:
        conn = giveconnect(request)
        cursor = conn.cursor()
        if request.session.get('login_id') is not None:
            preparation_date = request.POST.get('preparationdate')
            person = int(request.POST.get('person'))
            lid = int(request.session.get('login_id'))
            request.session['preparation_date'] = preparation_date
            caterer_id = request.session.get('caterer_id')
            category_id = int(request.session.get('catering_category_id'))
            print(category_id)
            query = "select client_reg.client_id from client_reg where login_id = %d;" % (lid)
            cursor.execute(query)
            rows = cursor.fetchone()
            print("Client id ", rows[0])
            qu = "select catering_cater_map_id from catering_category_mapping " \
                 "where catering_owner_id = %d and catering_category_id =%d" % (caterer_id, category_id)
            cursor.execute(qu)
            r = cursor.fetchone()

            request.session['catering_category_map_id'] = r[0]

            q = "select date from catering_booking where date = '%s' and catering_category_map_id = %d" % (
                preparation_date, r[0])
            cursor.execute(q)
            row = cursor.fetchall()
            print("date ", row)

            if row:
                reply = "Sorry, caterer is not Available for that day .."
                print("failure msg:", reply)
                return HttpResponse(reply)
            else:
                reply = "Caterer is Available for that day .."
                return HttpResponse(reply)

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



def client_book_caterer(request):
    try:
       conn = giveconnect(request)
       cursor = conn.cursor()
       if request.session.get('login_id') is not None:

            preparation_date = request.POST.get('preparationdate')
            print("preparation date : ",preparation_date)

            person = int(request.POST.get('person'))
            print("person : ", person)

            lid = int(request.session.get('login_id'))
            print("login id ", lid)

            request.session['preparation_date'] = preparation_date

            caterer_id = request.session.get('caterer_id')
            print("caterer id ", caterer_id)

            category_id = int(request.session.get('catering_category_id'))
            print(category_id)
            query = "select client_reg.client_id from client_reg where login_id = %d;" % (lid)
            cursor.execute(query)
            rows = cursor.fetchone()
            print("Client id ", rows[0])
            qu = "select catering_cater_map_id from catering_category_mapping " \
                 "where catering_owner_id = %d and catering_category_id =%d" % (caterer_id, category_id)
            cursor.execute(qu)
            r = cursor.fetchone()

            request.session['catering_category_map_id'] = r[0]



            query1 = "insert into catering_booking (booked_by_client_id,catering_category_map_id,date,number_of_person) " \
                     "values (%d,%d,'%s',%d)" % (rows[0], r[0], preparation_date, person)
            cursor.execute(query1)
            conn.commit()
            catering_booking_id = cursor.lastrowid
            request.session['catering_booking_id'] = catering_booking_id

            query2 = "select sum(tbl.amount), tbl.dd " \
                     "from (select (catering_booking.number_of_person * catering_category.price) as amount," \
                     " catering_booking.date as dd " \
                     "from catering_booking " \
                     "join catering_category_mapping on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                     "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                     "where catering_booking.booked_by_client_id =%d and catering_booking.status = 'pending' and catering_booking.date ='%s') as tbl " \
                     "group by tbl.dd" % (rows[0], preparation_date)
            cursor.execute(query2)
            r1 = cursor.fetchone()
            catering_cost = r1[0]
            request.session['f'] = 2
            print("done")
            return payment(request, 0, catering_cost)

       else:
            return render(request, 'login.html')

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def booked_caterer(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        client_id = int(request.session.get('client_id'))
        print(client_id)
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "catering_owner_reg.gst_no," \
                "login_table.login_id," \
                "catering_category.category_name " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "join catering_booking on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                "join login_table on login_table.login_id = catering_owner_reg.login_id " \
                "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                "where catering_booking.status = 'paid' and booked_by_client_id = %d ;" %(client_id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'booked_caterer.html', {'data': rows})
    else:
        return render(request, 'login.html')


def payment(request,totalAmount =None,catering_cost =None):
    print("payment", totalAmount)
    print(catering_cost)
    client_id = request.session.get('client_id')
    if totalAmount is not None and request.session.get('f') == 1:
        print("in first if")
        vanue_id = request.session.get('vanue_id')
        venue_cost = totalAmount
        vanue_booked_id = request.session.get('vanue_booked_id')
        return render(request, 'between.html',{'vanuecost':venue_cost,'surl':'http://127.0.0.1:8000/eventapp/Success?type=venue&vanue_booked_id='+str(vanue_booked_id)+'&client_id='+str(client_id)+'&vanue_id='+str(vanue_id),'furl':'http://127.0.0.1:8000/eventapp/Failure?type=venue&vanue_booked_id='+str(vanue_booked_id)+'&client_id='+str(client_id)})

    if catering_cost is not None and request.session.get('f') == 2:
        print("in second if")
        cat_cost = catering_cost
        print(cat_cost)
        caterer_id = request.session.get('caterer_id')
        catering_booking_id = request.session.get('catering_booking_id')
        return render(request,'between.html',{'catering_cost':cat_cost,'surl':'http://127.0.0.1:8000/eventapp/Success?type=caterer&catering_booking_id='+str(catering_booking_id)+'&client_id='+str(client_id)+'&caterer_id='+str(caterer_id),'furl':'http://127.0.0.1:8000/eventapp/Failure?type=caterer&catering_booking_id='+str(catering_booking_id)+'&client_id='+str(client_id)})

def Home(request):
    MERCHANT_KEY = "fB7GBa4Z"
    key = "fB7GBa4Z"
    SALT = "jsata1kQu6"
    PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
    action = ''
    posted = {}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = key
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action = PAYU_BASE_URL
    # xyz="https://test.payu.in/_payment"
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):
        return render(request, 'current_datetime.html', {"posted": posted, "hashh": hashh,
                                                                                    "MERCHANT_KEY": MERCHANT_KEY,
                                                                                    "txnid": txnid,
                                                                                    "hash_string": hash_string,
                                                                                    "action": action})
    else:
        return render(request,'current_datetime.html', {"posted": posted, "hashh": hashh,
                                                                                    "MERCHANT_KEY": MERCHANT_KEY,
                                                                                    "txnid": txnid,
                                                                                    "hash_string": hash_string,
                                                                                    "action": "."})


@csrf_protect
@csrf_exempt
def Success(request):
    from datetime import date, datetime
    conn = giveconnect(request)
    cursor = conn.cursor()
    amount =float(request.POST.get("amount"))
    current_date =date.today()
    today = current_date.strftime("%Y-%m-%d")  # for  Today's date..
    now = datetime.now()
    time = now.strftime("%H:%M")  # for current time..

    client_id = int(request.GET.get('client_id'))

    if request.GET.get('type') =='venue':
        vanue_id = int(request.GET.get('vanue_id'))
        print("vanue_id :",vanue_id)
        vanue_booked_id = int(request.GET.get('vanue_booked_id'))
        query = "UPDATE vanue_booking SET status = 'paid' WHERE v_book_id = %d;" %(vanue_booked_id)
        cursor.execute(query)
        print("Updated venue")


        query1 = "INSERT INTO payment (Client_id,Date,Time,Amount,Status,roll_id,booking_id) VALUES (%d, '%s', '%s', %d, 'paid',1, %d);" \
                 %(client_id,today,time,amount,vanue_booked_id)
        cursor.execute(query1)
        final_amount = amount - ((amount*30)/100)
        query2 = "INSERT INTO land_owner_payment (owner_id, vanue_id, amount, status, date, time,id_client_foreign  ) VALUES ((select land_owner_id from vanue_table where vanue_id = %d), %d,%d, 'paid', '%s', '%s',%d);" \
                 %(vanue_id,vanue_id,final_amount,today,time,client_id)
        cursor.execute(query2)
        conn.commit()

    if request.GET.get('type') =='caterer':
        catering_booking_id = int(request.GET.get('catering_booking_id'))
        caterer_id = int(request.GET.get('caterer_id'))
        print('caterer id :',caterer_id)
        query = "UPDATE catering_booking SET status = 'paid' WHERE catering_book_id = %d " \
                 %(catering_booking_id)
        cursor.execute(query)
        print("Updated caterer")

        query1 = "INSERT INTO payment (Client_id,Date,Time,Amount,Status,roll_id,booking_id) VALUES (%d, '%s', '%s', %d,'paid',2, %d);" \
                 % (client_id, today, time , amount, catering_booking_id)
        cursor.execute(query1)

        final_amount = amount - ((amount * 30) / 100)
        query2 = "INSERT INTO caterer_owner_payment (caterer_id, amount, status, date, time) VALUES (%d,%d, 'paid', '%s', '%s');" \
                 %(caterer_id,final_amount,today,time)
        cursor.execute(query2)
        conn.commit()

    print("success")
    c = {}
    c.update(csrf(request))
    print("THis is payuResponse", request.POST)
    status = request.POST["status"]
    firstname = request.POST["firstname"]

    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "jsata1kQu6"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        amount = request.POST.get("amount")
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render(request, 'sucess.html',{"txnid": txnid, "status": status, "amount": amount,"name":firstname,"email":email,"date":today,"time":time,"item":productinfo})

@csrf_protect
@csrf_exempt
def Failure(request):
    conn = giveconnect(request)
    cursor = conn.cursor()

    if request.GET.get('type') =='venue':
        vanue_booked_id = int(request.GET.get('vanue_booked_id'))
        query = "DELETE FROM vanue_booking WHERE v_book_id = %d" %(vanue_booked_id)
        cursor.execute(query)
        conn.commit()

    if request.GET.get('type') =='caterer':
        catering_booking_id = int(request.GET.get('catering_booking_id'))
        query = "DELETE FROM catering_booking WHERE catering_book_id = %d " %(catering_booking_id)
        cursor.execute(query)
        conn.commit()

    c = {}
    c.update(csrf(request))
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "jsata1kQu6"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render(request, "Failure.html", c)

def client_bookedvenue_history(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.session.get('client_id'))
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_booking.status = 'paid' and date < curdate() and vanue_booking.booked_by_client_id = %d;"%(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'booked_vanue_history.html',{'data' : rows} )
    else:
        return render(request, 'login.html')

def happy_client(request):
    conn = giveconnect(request)
    cursor = conn.cursor()

    # if request.session.get('roll_id') == 1 :   #landOwner
    #     query = "select count(client_id) from client_reg;"
    #     cursor.execute(query)
    #     row = cursor.fetchone()
    #     request.session['happy_client'] = row[0]
    #     query1="select count(Payment_id) from payment where roll_id = 1;"
    #     cursor.execute(query1)
    #     r1 = cursor.fetchone()
    #     request.session['payment_id'] = r1[0]
    #     query2 = "select sum(amount) from land_owner_payment ;"
    #     cursor.execute(query2)
    #     r2 = cursor.fetchone()
    #     print("earning :",r2[0])
    #     request.session['earning'] = r2[0]
    #     return 0
    # elif request.session.get('roll_id') == 2: #caterer
    #     query = "select count(client_id) from client_reg;"
    #     cursor.execute(query)
    #     row = cursor.fetchone()
    #     request.session['happy_client'] = row[0]
    #     query1 = "select count(Payment_id) from payment where roll_id = 2;"
    #     cursor.execute(query1)
    #     r1 = cursor.fetchone()
    #     request.session['payment_id'] = r1[0]
    #     query2 = "select sum(amount) from caterer_owner_payment;"
    #     cursor.execute(query2)
    #     r2 = cursor.fetchone()
    #     request.session['earning'] = r2[0]
    #     return 0
    if request.session.get('roll_id') == 3:  #client
        query = "select count(client_id) from client_reg;"
        cursor.execute(query)
        row = cursor.fetchone()
        request.session['happy_client'] = row[0]
        query1 = "select count(land_owner_id) from land_owner_reg ;"
        cursor.execute(query1)
        r1 = cursor.fetchone()
        request.session['land_owners'] = r1[0]
        query2 = "select count(catering_owner_id) from catering_owner_reg ;"
        cursor.execute(query2)
        r2 = cursor.fetchone()
        request.session['caterers'] = r2[0]
        return 0
    else: #admin
        query = "select count(client_id) from client_reg;"
        cursor.execute(query)
        row = cursor.fetchone()
        request.session['happy_client'] = row[0]
        query1 = "select count(Payment_id) from payment ;"
        cursor.execute(query1)
        r1 = cursor.fetchone()
        request.session['payment_id'] = r1[0]
        query2 = "select count(vanue_id) from vanue_table ;"
        cursor.execute(query2)
        r2 = cursor.fetchone()
        request.session['venues'] = r2[0]
        return 0

def land_upcoming_event(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = request.session.get('land_owner_id')
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "vanue_image_mapping.image_path," \
                "client_reg.client_name," \
                "vanue_booking.end_date " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "join client_reg on client_reg.client_id = vanue_booking.booked_by_client_id " \
                "where vanue_booking.status = 'paid' and date > curdate() and land_owner_reg.land_owner_id =%d" %(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'upcoming_events.html',{'data':rows})
    else:
        return render(request, 'login.html')


def land_bookedvenue_history(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.session.get('land_owner_id'))
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "client_reg.client_name," \
                "vanue_image_mapping.image_path," \
                "vanue_booking.end_date " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "join client_reg on client_reg.client_id = vanue_booking.booked_by_client_id " \
                "where vanue_booking.status = 'paid' and date < curdate() and land_owner_reg.land_owner_id =%d;" %(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'land_booked_vanues_history.html',{'data' : rows} )
    else:
        return render(request, 'login.html')

def land_birthday(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = request.session.get('land_owner_id')
        query = "select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 1 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' and land_owner_reg.land_owner_id =%d "%(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'land_birthday_venues.html',{'data':rows})
    else:
        return render(request,'login.html')

def land_wedding(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = request.session.get('land_owner_id')
        query = "select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 3 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' and land_owner_reg.land_owner_id =%d "%(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'land_wedding_venues.html',{'data':rows})
    else:
        return render(request,'login.html')

def land_sangeet(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = request.session.get('land_owner_id')
        query = "select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 2 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' and land_owner_reg.land_owner_id =%d "%(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'land_sangeet_venues.html',{'data':rows})
    else:
        return render(request,'login.html')

def land_party(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = request.session.get('land_owner_id')
        query = "select vanue_table.vanue_id," \
                "vanue_table.vanue_name," \
                "vanue_table.address," \
                "vanue_table.sqft," \
                "vanue_table.capacity," \
                "vanue_table.price_per_hour," \
                "vanue_image_mapping.image_path " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_category_mapping on vanue_table.vanue_id = vanue_category_mapping.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "where vanue_category_mapping.vanue_category_id = 4 and land_owner_reg.status ='Accepted' and vanue_table.status = 'Accepted' and land_owner_reg.land_owner_id =%d "%(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'land_party.html',{'data':rows})
    else:
        return render(request,'login.html')

def cater_confirmed(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.session.get('catering_owner_id'))
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "catering_owner_reg.gst_no," \
                "catering_category.category_name," \
                "client_reg.client_name," \
                "client_reg.mobile_number " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "join catering_booking on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                "join client_reg on client_reg.client_id = catering_booking.booked_by_client_id " \
                "where catering_booking.status = 'paid' and catering_owner_reg.catering_owner_id = %d;" %(id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'caterer_confirmed.html',{'data':rows})
    else:
        return render(request,'login.html')

def cater_history(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        id = int(request.session.get('catering_owner_id'))
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "catering_owner_reg.gst_no," \
                "catering_category.category_name ," \
                "client_reg.client_name," \
                "client_reg.mobile_number " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "join catering_booking on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                "join client_reg on client_reg.client_id = catering_booking.booked_by_client_id " \
                "where catering_booking.status = 'paid' and catering_owner_reg.catering_owner_id = %d and date < curdate() ;" % (id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'caterer_history.html',{'data':rows})
    else:
        return render(request, 'login.html')

def admin_booked_cater(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query  = "select catering_owner_reg.catering_owner_name," \
                 "catering_owner_reg.mobile_number," \
                 "catering_owner_reg.gst_no," \
                 "catering_category.category_name," \
                 "client_reg.client_name " \
                 "from catering_owner_reg " \
                 "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                 "join catering_booking on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                 "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                 "join client_reg on client_reg.client_id = catering_booking.booked_by_client_id  " \
                 "where catering_booking.status = 'paid';"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'admin_booked_caterer.html',{'data':rows})
    else:
        return render(request,'login.html')

def admin_cater_history(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number," \
                "catering_owner_reg.gst_no," \
                "catering_category.category_name ," \
                "client_reg.client_name," \
                "client_reg.mobile_number " \
                "from catering_owner_reg " \
                "join catering_category_mapping on catering_category_mapping.catering_owner_id = catering_owner_reg.catering_owner_id " \
                "join catering_booking on catering_booking.catering_category_map_id = catering_category_mapping.catering_cater_map_id " \
                "join catering_category on catering_category.catering_cat_id = catering_category_mapping.catering_category_id " \
                "join client_reg on client_reg.client_id = catering_booking.booked_by_client_id " \
                "where catering_booking.status = 'paid' and date < curdate() ;"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'admin_cater_history.html',{'data':rows})
    else:
        return render(request,'login.html')

def admin_vanue_history(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select vanue_table.vanue_name," \
                "vanue_table.address," \
                "land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number," \
                "vanue_booking.date," \
                "vanue_booking.start_time," \
                "vanue_booking.end_time," \
                "client_reg.client_name," \
                "vanue_image_mapping.image_path," \
                "vanue_booking.end_date " \
                "from vanue_table " \
                "join land_owner_reg on land_owner_reg.land_owner_id = vanue_table.land_owner_id " \
                "join vanue_booking on vanue_booking.vanue_id = vanue_table.vanue_id " \
                "join vanue_image_mapping on vanue_image_mapping.vanue_id = vanue_table.vanue_id " \
                "join client_reg on client_reg.client_id = vanue_booking.booked_by_client_id " \
                "where vanue_booking.status = 'paid' and date < curdate();"
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request,'admin_vanue_history.html',{'data':rows})
    else:
            return render(request,'login.html')

def admin_catering_payment(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()

        query = "select catering_owner_reg.catering_owner_name," \
                "catering_owner_reg.mobile_number as caterer_contact," \
                "caterer_owner_payment.date," \
                "caterer_owner_payment.time," \
                "caterer_owner_payment.amount " \
                "from caterer_owner_payment " \
                "join catering_owner_reg on catering_owner_reg.catering_owner_id = caterer_owner_payment.caterer_id " \
                "where caterer_owner_payment.status = 'paid';"
        cursor.execute(query)
        rows = cursor.fetchall()
        for  i in rows :
            x = float(i[4])
            amount = x - ((x*30)/100)
        return render(request,'admin_catering_payment.html',{'data':rows,'amount':amount})
    else:
            return render(request,'login.html')

def admin_vanue_payment(request):
    if request.session.get('login_id') is not None:
        conn = giveconnect(request)
        cursor = conn.cursor()

        query = "select land_owner_reg.land_owner_name," \
                "land_owner_reg.mobile_number as caterer_contact," \
                "land_owner_payment.date," \
                "land_owner_payment.time," \
                "land_owner_payment.amount " \
                "from land_owner_payment " \
                "join land_owner_reg on land_owner_reg.land_owner_id = land_owner_payment.owner_id " \
                "where land_owner_payment.status = 'paid';"
        cursor.execute(query)
        rows = cursor.fetchall()
        for i in rows:
            x = float(i[4])
            amount = x - ((x * 30) / 100)
        return render(request, 'admin_venue_payment.html', {'data': rows, 'amount': amount})

def landowner_payment(request):
    if request.session.get('login_id') is not None:
        login_id = int(request.session.get('login_id'))
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select client_reg.client_name," \
                "client_reg.mobile_number," \
                "land_owner_payment.date," \
                "land_owner_payment.time," \
                "land_owner_payment.amount " \
                "from login_table " \
                "join land_owner_reg on land_owner_reg.login_id = login_table.login_id " \
                "join land_owner_payment on land_owner_payment.owner_id  = land_owner_reg.land_owner_id " \
                "join client_reg on client_reg.client_id = land_owner_payment.id_client_foreign  " \
                "where land_owner_payment.status = 'paid' and login_table.login_id = %d;" %(login_id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'landowner_payment.html', {'data': rows})

def catering_owner_payment(request):
    if request.session.get('login_id') is not None:
        login_id = int(request.session.get('login_id'))
        conn = giveconnect(request)
        cursor = conn.cursor()
        query = "select client_reg.client_name," \
                "client_reg.mobile_number," \
                "caterer_owner_payment.date," \
                "caterer_owner_payment.time," \
                "caterer_owner_payment.amount " \
                "from login_table " \
                "join catering_owner_reg on catering_owner_reg.login_id = login_table.login_id " \
                "join caterer_owner_payment on caterer_owner_payment.caterer_id  = catering_owner_reg.catering_owner_id " \
                "join client_reg on client_reg.client_id = caterer_owner_payment.c_id " \
                "where login_table.login_id = %d; " %(login_id)
        cursor.execute(query)
        rows = cursor.fetchall()
        return render(request, 'cateringowner_payment.html', {'data': rows})
