from django.urls import path,include
from . import views

app_name = 'zoom'

urlpatterns = [
    path('',views.zoom,name='zoom'),
    path('currentmeeting/',views.currentmeeting,name='currentmeeting'),
    path('reports',views.reports,name='reports'),
    path('viewreport/<str:name>',views.viewreport,name = 'viewreport'),
    path('viewreport/',views.viewreport_norequest,name='viewreport'),
    path('currentmeeting/<str:name>',views.currentmeeting_condition,name='currentmeeting_multiple'),
]
