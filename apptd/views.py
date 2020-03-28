from django.shortcuts import HttpResponse, render
import pymongo

uri = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(uri)
mydb = myclient['ToDodb']
# def_mycol is default collection
def_mycol = []
# Create your views here.
def index(request):
    """This func used to show lists-names with number of tasks on main page"""
    dblist = mydb.list_collection_names()
    defaultdb = ['django_migrations', 'django_content_type', '__schema__', 'django_admin_log', 'auth_group', 'auth_user', 'auth_user_user_permissions',
                 'django_session', 'apptd_register', 'auth_permission', 'auth_group_permissions', 'auth_user_groups']

    # coll = collextions in dblist
    dblist = [coll for coll in dblist if coll not in defaultdb]
    dblist.sort()
    pdict = {} # has collections : tasks

    for coll in dblist:
        mycol = mydb[coll]
        doc = mycol.find()
        l = [i for i in doc]
        pdict[coll]= len(l)

    # parameters to pass in render()
    params = {'List' : pdict}
    return render(request, 'apptd/index.html', params)

def createtask(request):
    """This func used to create tasks with specific list name"""
    if request.method=="POST":
        mtask = request.POST.get('task', '')
        mduedate = request.POST.get('duedate', '')
        mpriority = request.POST.get('priority', '')
        maddlist = request.POST.get('addlist', '')

        if mtask=='' or mduedate=='' or maddlist=='' or maddlist=='apptd_register' or mpriority=='':
            return render(request, 'apptd/createtask.html')

        if mpriority!='H' and mpriority!='M'and mpriority!='L':
            return render(request, 'apptd/createtask.html')

        else:
            # Collection define here------
            mycol = mydb[maddlist]
            myquery = {"Task" : mtask, "Duedate" : mduedate, "Priority" : mpriority}
            mycol.insert_one(myquery)
            return HttpResponse("Task created.......")
    return render(request, 'apptd/createtask.html')

def tasklist(request):
    """This func used to show 'Task-list' on 'task.html' """
    if request.method=='POST':
        # mlname is list name of 'task'
        mlname = request.POST.get('list', '')

        if mlname=='':
            return render(request, 'apptd/')

        dblist = mydb.list_collection_names()
        defaultdb = ['django_migrations', 'django_content_type', '__schema__', 'django_admin_log', 'auth_group',
                     'auth_user', 'auth_user_user_permissions',
                     'django_session', 'apptd_register', 'auth_permission', 'auth_group_permissions', 'auth_user_groups']

        # coll = collextions in dblist
        dblist = [coll for coll in dblist if coll not in defaultdb]
        dblist.sort()

        if mlname not in dblist:
            return render(request, 'apptd/index.html')

        else:
            # Collection define here------
            pdoc=[]
            mycol = mydb[mlname]
            def_mycol.insert(0,mlname)
            x = mycol.find({}, {"_id":0, "Task":1, "Duedate":1, "Priority":1})

            for i in x:
                pdoc.append(i)
            params = {'Lists':pdoc}
            return render(request, 'apptd/tasklist.html', params)
    return render(request, 'apptd/tasklist.html')

def deltasks(request):
    """This func is used to delete completed tasks"""
    if request.method=='POST':
        mdeltasks = request.POST.get('deltasks','')

        if mdeltasks=='':
            return render(request, 'apptd/tasklist.html')

        else:
            deltasks = mdeltasks.split(',')
            mycol = mydb[def_mycol[0]]
            list = []
            for i in range(len(deltasks)):
                myquery = {'Task' : deltasks[i]}
                x = mycol.delete_one(myquery)
                list.insert(0,x)
            print(f"{list[0].deleted_count} tasks deleted......")
            return render(request, 'apptd/index.html')
    return render(request, 'apptd/tasklist.html')

def dellist(request):
    if request.method=='POST':
        mdellist = request.POST.get('dellist','')

        if mdellist=='':
            return render(request, 'apptd/index.html')

        else:
            mycol = mydb[mdellist]
            mycol.drop()
            return render(request, 'apptd/index.html')
    return render(request, 'apptd/index.html')