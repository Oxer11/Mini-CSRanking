from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import Permission, User
from django.contrib.auth import *
from django.contrib.auth.decorators import *
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area, Scholar_Area, Conference_Area, Scholar_Paper, Profile, User_Scholar, User_Area, User_Institution, User_Conference

@login_required
def addpaper(request):
    user = request.user

    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        conf_id = request.POST.get('conf_id')
        href = request.POST.get('href')
        authors = request.POST.get('authors')
        authors = authors.split(",")
        try:
            conf = Conference.objects.get(abbr=conf_id, year=year)
        except Conference.DoesNotExist:
            return HttpResponse("This Conference Does Not Exist!")

    return render(request, 'addpaper.html', {'user':user})
