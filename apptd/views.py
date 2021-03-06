from django.shortcuts import HttpResponse, render
import pymongo

uri = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(uri)
mydb = myclient['ToDodb']
# def_mycol is default collection
def_mycol = ['default_value']
# def-task is default taskname
def_task = ['default_name']
# This list contains dictionary having task : name, duedate, priority
dftask_detail = ['default']
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
            return render(request, 'apptd/index.html')

        collist = coll_access()

        if mlname not in collist:
            return render(request, 'apptd/index.html')

        else:
            # Collection define here------
            pdoc=[]
            mycol = mydb[mlname]
            """ def_mycol get the collection name (list name) for recorded to what list name
            we had selected to see it's tasks"""
            def_mycol.clear()
            def_mycol.append(mlname)
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
            return render(request, 'apptd/index.html')

        else:
            deltasks = mdeltasks.split(',')
            mycol = mydb[def_mycol[0]]
            list = []
            for i in range(len(deltasks)):
                myquery = {'Task' : deltasks[i]}
                x = mycol.delete_one(myquery)
                list.insert(0,x)
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

        if mlname=='' or mlname not in collist:
            return render(request, 'apptd/adview.html')

        mycol = mydb[mlname]
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

def edittask(request):
    if request.method=='POST':
        mycol = mydb[def_mycol[0]]
        mtask = request.POST.get('mtask', '')
        if mtask == '' or mycol.find_one({'Task' : mtask}) == None:

            return render(request, 'apptd/index.html')

        # To update def_task
        def_task.clear()
        def_task.append(mtask)
        doc = mycol.find_one({'Task' : mtask})
        params = {'name' : doc['Task'], 'duedate' : doc['Duedate'], 'priority' : doc['Priority']}
        # To update list dftask_detail
        dftask_detail.clear()
        dftask_detail.append(params)
        return render(request, 'apptd/edittask.html', params)

def editdone(request):
    mycol = mydb[def_mycol[0]]
    mtask = def_task[0]
    # dict containing all details of selected task to edit.
    dict = dftask_detail[0]

    if request.method=='POST':
        tname = request.POST.get('tname', '')
        tdate = request.POST.get('tdate', '')
        tpriority = request.POST.get('tpriority', '')

        if tname == '': tname = dict['name']
        if tdate == '': tdate = dict['duedate']
        if tpriority == '': tpriority = dict['priority']
        update = {'Task' : tname, 'Duedate' : tdate, 'Priority' : tpriority}
        mycol.update_one({'Task' : mtask}, {'$set' : update})
    return HttpResponse('Task Updated...')






