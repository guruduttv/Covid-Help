from django.urls import path
from .  import views
from .views import *
urlpatterns=[ path('',covid,name='covid'),
    path('covid',covid,name='covid'),

    path('index',index,name='index'),
    path('selfs',selfs,name='selfs'),
    path('karnataka',karnataka,name='karnatka'),
path('banghosp',banghosp,name='banghosp'),


path('bangrural',bangrural,name='bangrural'),
path('bangurban',bangurban,name='bangurban'),
path('more',more,name='more'),

]