from django.shortcuts import HttpResponse, render
import pymongo

uri = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(uri)
mydb = myclient['ToDodb']
# def_mycol is default collection
def_mycol = []
# Create your views here.

def coll_access():
    collist = mydb.list_collection_names()
    defaultcol = ['django_migrations', 'django_content_type', '__schema__', 'django_admin_log', 'auth_group',
                  'auth_user', 'auth_user_user_permissions',
                  'django_session', 'apptd_register', 'auth_permission', 'auth_group_permissions', 'auth_user_groups']

    # coll = collections in collist
    # Filtering the collections to avoid 'defaultcol'
    collist = [coll for coll in collist if coll not in defaultcol]
    collist.sort()
    return (collist)
    
def index(request):
    """This func used to show lists-names with number of tasks on main page"""
    collist = coll_access()
    pdict = {}  # has {collections : no. of tasks}

    for coll in collist:
        mycol = mydb[coll]
        pdict[coll] = mycol.count_documents({})

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

        collist = coll_access()

        if mlname not in collist:
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

def adview(request):
    collist = coll_access()
    if request.method=='POST':
        mlname = request.POST.get('listname', '')
        moption = request.POST.get('option', '')
        print("mlname=",mlname,"moption",moption)
        if mlname=='' or mlname not in collist:
            return render(request, 'apptd/adview.html')

        mycol = mydb[mlname]
        def_mycol.insert(0,mlname)

        if moption=='Priority':
            # All are lists of dicts according priority
            Hl = []
            Ml = []
            Ll = []
            for dict in mycol.find({}, {"_id" : 0, "Task" : 1, "Priority" : 1}):
                if dict['Priority'] == 'H':
                    Hl.append(dict)
                elif dict['Priority'] == 'M':
                    Ml.append(dict)
                else:
                    Ll.append(dict)
            #  pdict is a list sorted dicts according priority.
            pdict = []
            pdict.extend(Hl)
            pdict.extend(Ml)
            pdict.extend(Ll)
            params = {'List': pdict}
            return render(request, 'apptd/adview.html', params)

        if moption=='Duedate':
            #  pdict is a list sorted dicts according duedate.
            pdict = []
            for dict in mycol.find({}, {"_id" : 0, "Task" : 1, "Duedate" : 1}).sort('Duedate'):
               pdict.append(dict)

            params = {'List': pdict}
            return render(request, 'apptd/adview.html', params)

        if moption == 'Task-Only':
            #  pdict is a list sorted dicts according task-only.
            pdict = []
            for dict in mycol.find({},{'_id' : 0, 'Task' : 1}).sort('Task'):
                pdict.append(dict)

            params = {'List' : pdict}
            return render(request, 'apptd/adview.html', params)

    pdict = {}  # has {collections : no. of tasks}
    for coll in collist:
        mycol = mydb[coll]
        pdict[coll] = mycol.count_documents({})

    # parameters to pass in render()
    params = {'List': pdict}
    return render(request, 'apptd/adview.html', params)
