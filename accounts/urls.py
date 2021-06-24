from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="accounts/changepassword.html"),name='changepassword'),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/change_password_success.html"),name='changepassword_done'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
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
