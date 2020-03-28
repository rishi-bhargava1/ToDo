import pymongo
from django.shortcuts import  HttpResponse, render

uri = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(uri)
mydb = myclient['ToDodb']
mycol1 = mydb['apptd_register']

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def regsave(request):
    name = ""
    password = ""

    if request.method=="POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')

    if name=='' or password=='':
        return render(request, 'register.html')

    else:
        mydict_regsv = {'Uname' : name, 'Upaswd' : password}
        obj_regsv = mycol1.insert_one(mydict_regsv)
        print(obj_regsv)
        return HttpResponse("Registration Done.....")

def loginchck(request):
    name = ""
    password = ""

    if request.method=="POST":
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')

    if name=="" or password=="":
        return render(request, 'index.html')

    else:
        myquery = {'Uname' : name, 'Upaswd' : password}
        uval = mycol1.find(myquery)

        for i in uval:
            if i['Uname']==name and i['Upaswd']==password:
                return render(request, 'apptd/preindex.html')
        return HttpResponse("login faild.....")