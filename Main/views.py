from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from zoom.models import AuthIds,Metrics

@login_required
def TestPage(request):
    a = AuthIds.objects.filter(username=request.user.username)
    try:
        b = Metrics.objects.filter(username=request.user.username)
        if len(b) == 0:
            inst = Metrics.objects.create(username=request.user,late='5',leftearly='2',minduration='25')
    except Exception as e:
        print(e)
    return render(request,'test.html',{'auth':len(a)})


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

from django.http import HttpResponseRedirect
from django.urls import reverse

class HomePage(TemplateView):
    template_name = "index.html"

def setup(request):
    return render(request,'setup.html',{})

def about(request):
    return render(request,'about.html')
