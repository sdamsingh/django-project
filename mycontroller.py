from django.shortcuts import *
from django.http import *
from connectionfile import *
from django.views.decorators.csrf import *
from django.core.files.storage import FileSystemStorage
from datetime import *
import http.client
import smtplib

def indexpage(request):
    return render(request,'index.html')

def addcategorypage(request):
    return render(request, 'addcategorypage.html')


def addcategoryaction(request):
    conn = connection.connection('')
    cname = request.GET['cname']
    description = request.GET['description']
    cr = conn.cursor()
    s = "insert into categorytable values ('" + cname + "','" + description + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Data not saved"
    return JsonResponse(d, safe=False)


def viewcategorypage(request):
    return render(request, 'viewcategorypage.html')


def viewcategoryaction(request):
    conn = connection.connection('')
    s = "select * from categorytable"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['cname'] = p[0]
        d['description'] = p[1]
        x.append(d)
    return JsonResponse(x, safe=False)


def deletecategoryaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    cname = request.GET['cname']
    s = "delete from categorytable where categoryname='" + cname + "'"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    return HttpResponseRedirect('/viewcategorypage')


def usersignuppage(request):
    return render(request, 'usersignuppage.html')


def usersignupaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    fullname = request.GET['fullname']
    mobileno = request.GET['mobileno']
    address = request.GET['address']
    city = request.GET['city']
    email = request.GET['email']
    password = request.GET['password']
    s = "insert into usersignup values ('" + email + "','" + fullname + "','" + mobileno + "','" + address + "','" + city + "','" + password + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    if result == 1:
        d['message'] = "Data saved"
    else:
        d['message'] = "Data not saved"
    return JsonResponse(d, safe=False)


def addproductpage(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d['categoryname'] = p[0]
        x.append(d)
    return render(request, 'addproductpage.html', {'mydata': x})


@csrf_exempt
def addproductaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    categoryname = request.POST['categoryname']
    pname = request.POST['pname']
    price = request.POST['price']
    mrp = request.POST['mrp']
    description = request.POST['description']
    photo = request.FILES['photo']
    fs = FileSystemStorage()
    filename = fs.save(photo.name, photo)
    location = fs.url(filename)
    s = "insert into producttable values (null,'" + pname + "','" + description + "','" + price + "','" + mrp + "','" + filename + "','" + categoryname + "')"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    d = {}
    d['message'] = "Data saved"
    return JsonResponse(d, safe=False)


def viewproductpage(request):
    return render(request, 'viewproductpage.html')


def viewproductaction(request):
    conn = connection.connection('')
    s = "select * from producttable"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    return JsonResponse(x, safe=False)


def deleteproductaction(request):
    conn = connection.connection('')
    pid = request.GET['pid']
    cr = conn.cursor()
    s = "delete from producttable where pid='" + str(pid) + "'"
    result = cr.execute(s)
    conn.commit()
    conn.close()
    return HttpResponseRedirect('/viewproductpage')


def showallproductpage(request):
    return render(request, 'showallproductpage.html')


def showallproductaction(request):
    conn = connection.connection('')
    s = "select * from producttable"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    print(x)
    return JsonResponse(x, safe=False)


def addtocartaction(request):
    CARTLIST1 = []
    if request.session.has_key('MYCART'):
        CARTLIST1 = request.session['MYCART']
    pid = request.GET['pid']
    qty = request.GET['qty']
    conn = connection.connection('')
    s = "select * from producttable where pid = '" + str(pid) + "'"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        d['qty'] = qty
        d['total'] = float(p[3]) * float(qty)

    flag = False
    for i in range(0, len(CARTLIST1)):
        ar = CARTLIST1
        if (int(ar[i]['pid']) == int(pid)):
            ar[i]['qty'] = int(ar[i]['qty']) + int(qty)
            ar[i]['total'] = float(ar[i]['price']) * float(ar[i]['qty'])
            flag = True
            break
    if flag == False:
        CARTLIST1.append(d)
    print(CARTLIST1)
    request.session['MYCART'] = CARTLIST1
    return JsonResponse(request.session['MYCART'], safe=False)


def deletefromcart(request):
    templst = []
    itemid = request.GET['pid']
    for i in request.session['MYCART']:
        if int(itemid) != int(i['pid']):
            templst.append(i)
            # print("I am not equal ")

    request.session['MYCART'] = templst
    return JsonResponse(request.session['MYCART'],safe=False)


def mycart(request):
    return render(request, 'mycart.html')


def mycartaction(request):
    if request.session.has_key('MYCART'):
        k = request.session['MYCART']
    else:
        k = []
    return JsonResponse(k, safe=False)


def proceedtopay(request):
    if request.session.has_key('USEREMAIL'):
        k = "/billinginfo"
    else:
        k = "/userlogin"

    return HttpResponseRedirect(k)


def userlogin(request):
    return render(request, 'userlogin.html')


@csrf_exempt
def userloginaction(request):
    email = request.POST['email']
    password = request.POST['password']
    conn = connection.connection('')
    cr = conn.cursor()
    flag = False
    s = "select * from usersignup"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        if p[0] == email and p[5] == password:
            request.session['USEREMAIL'] = email
            flag = True
            break

    d = {}
    if flag == False:
        d['message'] = "Invalid Login"
    else:
        d['message'] = "Login Success"

    return JsonResponse(d, safe=False)


def userhomepage(request):
    return render(request, 'userhomepage.html')


def billinginfo(request):
    conn = connection.connection('')
    cr = conn.cursor()
    flag = False
    s = "select * from usersignup where email='" + request.session['USEREMAIL'] + "'"
    cr.execute(s)
    result = cr.fetchall()
    d = {}
    for p in result:
        d['fullname'] = p[1]
        d['mobileno'] = p[2]
        d['address'] = p[3]
        d['city'] = p[4]
    netamount = 0
    for i in range(0, len(request.session['MYCART'])):
        ar = request.session['MYCART']
        netamount = netamount + ar[i]['total']

    d['netamount'] = netamount
    return render(request, 'billinginfo.html', d)


def userlogout(request):
    del request.session['USEREMAIL']
    del request.session['MYCART']
    # CARTLIST1.clear()
    return HttpResponseRedirect('/userlogin')


@csrf_exempt
def checkoutaction(request):
    email = request.POST['email']
    fullname = request.POST['fullname']
    netamount = request.POST['netamount']
    mobileno = request.POST['mobileno']
    address = request.POST['address']
    city = request.POST['city']
    paymentmode = request.POST['paymentmode']
    conn = connection.connection('')
    dt = datetime.now().date()
    s = "insert into ordertable values (null,'" + email + "','" + fullname + "','" + mobileno + "','" + address + "','" + city + "','" + str(
        netamount) + "','" + str(dt) + "','Pending','" + paymentmode + "')"
    # print(s)
    cr = conn.cursor()
    result = cr.execute(s)
    conn.commit()
    orderid = cr.lastrowid
    # print(orderid)
    for i in range(0, len(request.session['MYCART'])):
        ar = request.session['MYCART']
        s1 = "insert into orderdetail values (null,'" + str(orderid) + "','" + str(ar[i]['pid']) + "','" + ar[i][
            'pname'] + "','" + str(ar[i]['price']) + "','" + str(ar[i]['qty']) + "','" + str(ar[i]['total']) + "')"
        print(s1)
        cr1 = conn.cursor()
        res = cr1.execute(s1)
        conn.commit()
    conn.close()
    msg = "Your Order has been placed for Rs." + str(
        netamount) + " .Your order will be delivered after order approval. Thank You"
    msg = msg.replace(" ", "%20")
    conn1 = http.client.HTTPConnection("server1.vmm.education")
    conn1.request('GET',
                  "/VMMCloudMessaging/AWS_SMS_Sender?username=ExamSystem&password=S4J5LT3C&message=" + msg + "&phone_numbers=" + mobileno)
    response = conn1.getresponse()
    print(response.read())
    sender = 'tania.vmmteachers23@gmail.com'
    receiver = 'monika.vmm1989@gmail.com'
    password = 'Teachers@123'
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender, password)
        body = "\nYour Order has been placed for Rs." + str(
            netamount) + " .Your order will be delivered after order approval. Thank You\n\n"
        subject = "Subject:Django Shopping "
        msg = subject + body
        # msg='Subject:Demo <h1>This is a test e-mail message.</h1>'
        smtpserver.sendmail(sender, receiver, msg)
        print('Sent')
        smtpserver.close()
    except smtplib.SMTPException:
        print("Not Sent")
    del request.session['MYCART']
    # CARTLIST1.clear()
    d = {}
    d['message'] = "Data Saved"
    return JsonResponse(d, safe=False)


def thankspage(request):
    return render(request, 'thankspage.html')


def pendingorderpage(request):
    return render(request, 'pendingorderpage.html')


def pendingordersaction(request):
    conn = connection.connection('')
    s = "select * from ordertable where status='Pending' order by id DESC"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['id'] = p[0]
        d['email'] = p[1]
        d['fullname'] = p[2]
        d['mobileno'] = p[3]
        d['address'] = p[4]
        d['city'] = p[5]
        d['netamount'] = p[6]
        d['dateoforder'] = p[7]
        d['paymentmode'] = p[9]
        x.append(d)
    return JsonResponse(x, safe=False)


def approve_reject_action(request):
    orderid = request.GET['orderid']
    status = request.GET['status']
    mobileno = request.GET['mobileno']
    conn = connection.connection('')
    s = "update ordertable set status='" + status + "' where id='" + str(orderid) + "'"
    cr = conn.cursor()
    result = cr.execute(s)
    conn.commit()
    conn.close()
    msg = "Your Order has been " + status + ". Thank You"
    msg = msg.replace(" ", "%20")
    conn1 = http.client.HTTPConnection("server1.vmm.education")
    conn1.request('GET',
                  "/VMMCloudMessaging/AWS_SMS_Sender?username=ExamSystem&password=S4J5LT3C&message=" + msg + "&phone_numbers=" + mobileno)
    response = conn1.getresponse()
    print(response.read())

    sender = 'tania.vmmteachers23@gmail.com'
    receiver = 'monika.vmm1989@gmail.com'
    password = 'Teachers@123'
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(sender, password)
        body = "\nYour Order has been " + status + ". Thank You\n\n"
        subject = "Subject:Django Shopping - Order Status"
        msg = subject + body
        # msg='Subject:Demo <h1>This is a test e-mail message.</h1>'
        smtpserver.sendmail(sender, receiver, msg)
        print('Sent')
        smtpserver.close()
    except smtplib.SMTPException:
        print("Not Sent")

    d = {}
    d['message'] = "Order Updated"
    return JsonResponse(d, safe=False)


def myorders(request):
    return render(request, 'myorders.html')


def myordersaction(request):
    email = request.GET['email']
    conn = connection.connection('')
    s = "select * from ordertable where email='" + email + "' order by id DESC"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['id'] = p[0]
        d['email'] = p[1]
        d['fullname'] = p[2]
        d['mobileno'] = p[3]
        d['address'] = p[4]
        d['city'] = p[5]
        d['netamount'] = p[6]
        d['dateoforder'] = p[7]
        d['status'] = p[8]
        d['paymentmode'] = p[9]
        x.append(d)
    return JsonResponse(x, safe=False)

def showproductbycategorypage(request):
    d = {}
    categoryname = request.GET['cname']
    d['categoryname'] = categoryname
    return render(request,'showproductbycategory.html',d)

def viewproductbycategory(request):
    categoryname = request.GET['categoryname']
    conn = connection.connection('')
    s = "select * from producttable where categoryname='"+categoryname+"'"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    print(x)
    return JsonResponse(x, safe=False)

