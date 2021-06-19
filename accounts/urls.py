from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('changeverificationtoken/',views.changeverificationtoken,name='changeverificationtoken'),
    path('profile/',views.profile,name = 'profile'),
    path('files/',views.files, name = 'files'),
    path("deletefile/<slug:name>",views.deletefile, name = "deletefile"),
    path("deletefile/",views.deletefile, name = "deletefile"),
    path("addfile/",views.addfile, name="addfile"),
    path("viewfile/<slug:name>",views.viewfile, name = "viewfile"),
    path("viewfile/",views.viewfile, name = "viewfile"),
    path('metrics/',views.metrics,name='metrics')
]
