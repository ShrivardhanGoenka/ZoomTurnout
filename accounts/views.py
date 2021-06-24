from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render
from . import forms
from django.contrib.auth.decorators import login_required
from zoom.models import AuthIds,Files,StoreData,CurrentMeetinglog,Metrics
from django.http import HttpResponseRedirect
import pandas as pd

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

@login_required
def changeverificationtoken(request):
    if request.method == 'POST':
        try:
            a = AuthIds.objects.filter(username = request.user.username).get().authtoken
            CurrentMeetinglog.objects.filter(authtoken=a).delete()
            StoreData.objects.filter(authtoken=a).delete()
            AuthIds.objects.filter(username = request.user.username).delete()
        except:
            pass
        i = AuthIds(username=request.user.username,authtoken=request.POST.get('token'))
        i.save()

        return HttpResponseRedirect("/accounts/profile")
    return render(request,'accounts/verificationtoken.html',)

@login_required
def profile(request):
    a = AuthIds.objects.filter(username = request.user.username)
    if len(a) == 0:
        return render(request,'accounts/profile.html',{'token':'You have not added one yet'})
    else:
        return render(request,'accounts/profile.html',{'token':a.get(username=request.user.username).authtoken})

@login_required
def files(request):
    query = Files.objects.filter(username=request.user.username)
    list = []
    for i in query:
        list.append(i.name)

    return render(request, 'accounts/files.html',context = {'objects':list})

def deletefile(request,name):
    query1 = Files.objects.filter(username=request.user.username, name=name)
    Files.objects.filter(username=request.user.username, name=name).delete()
    return HttpResponseRedirect("/accounts/files")

@login_required
def addfile(request):
    if request.method == 'POST':
        excel_file = request.FILES["excel_file"]
        file = pd.read_excel(excel_file,header=None)
        data = file[0]
        x = ""
        for i in range(0,len(data)):
            if data.iloc[i] is not None:
                x+=data.iloc[i].strip()+","
        x=x[:-1]
        name = request.POST.get('name').replace(' ','')
        query1 = Files.objects.filter(username=request.user.username, name=name)
        if len(query1) == 0:
            inst = Files(username=request.user.username, name=name, content=x)
            inst.save()
        else:
            Files.objects.filter(username=request.user.username, name=name).delete()
            inst = Files(username=request.user.username, name=name, content=x)
            inst.save()

    return HttpResponseRedirect("/accounts/files")

def viewfile(request,name):
    query1 = Files.objects.filter(username=request.user.username, name=name)
    if len(query1) == 0:
        return render(request,'accounts/viewfile.html',{'name':'Not found'})
    else:
        list = query1.get().content
        list1 = list.split(',')
        return render(request,'accounts/viewfile.html',{'name':name, 'list':list1})

def metrics(request):
    try:
        if request.method == 'POST':
            print(request.POST.get('late'))
            try:
                Metrics.objects.filter(username = request.user.username).delete()
                Metrics.objects.create(username = request.user.username, late = request.POST.get('late'), leftearly=request.POST.get('leave'), minduration= request.POST.get('duration'))
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    try:
        query = Metrics.objects.filter(username = request.user.username)
        d1 = int(query.get().late)
        d2 = int(query.get().leftearly)
        d3 = int(query.get().minduration)
        return render(request,'accounts/metrics.html',{'l1':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],'d1': d1 ,
                                                       'l2':[1,2,3,4,5,6,7,8,9,10], 'd2':d2 ,
                                                       'l3':[0,5,10,15,20,25,27,30,33,35,37],'d3':d3})
    except Exception as e:
        print(e)
    return render(request,'accounts/metrics.html',{'l1':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] ,
                                                   'l2':[1,2,3,4,5,6,7,8,9,10],
                                                   'l3':[0,5,10,15,20,25,27,30,33,35,37]})

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'192.168.0.101:8000',
					'site_name': 'ZoomTurnout',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'changepass.zoomturnout@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/accounts/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})
