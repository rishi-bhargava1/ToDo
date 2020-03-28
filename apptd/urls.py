from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('createtask', views.createtask, name='createtask'),
    path('tasklist', views.tasklist, name='tasklist'),
    path('deltasks', views.deltasks, name='deltasks'),
    path('dellist', views.dellist, name='dellist'),
]