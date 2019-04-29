from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import Permission, User
from django.contrib.auth import *
from django.contrib.auth.decorators import *
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area, Scholar_Area, Conference_Area, Scholar_Paper, Profile, User_Scholar, User_Area, User_Institution, User_Conference, Remark

@login_required
def addpaper(request):
    context = {'user':request.user}
    unchecked = len(Remark.objects.filter(note__author=request.user).filter(checked=False))
    unchecked_schs = len(User_Scholar.objects.filter(user=request.user, new_paper=True))
    context['unchecked_schs'] = unchecked_schs
    context['unchecked'] = unchecked
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        year = int(year)
        conf_id = request.POST.get('conf_id')
        href = request.POST.get('href')
        authors = request.POST.get('authors')
        authors = authors.split(",")
        try:
            conf = Conference.objects.get(abbr=conf_id, year=year)
        except Conference.DoesNotExist:
            context['log'] = "Conference %s %d Does Not Exist!"%(conf_id, year)
            return render(request, 'addpaper.html', context)
        author = []
        for i in authors:
            try:
                a = Scholar.objects.get(name=i)
            except Scholar.DoesNotExist:
                context['log'] = "Scholar %s Does Not Exist!"%(i)
                return render(request, 'addpaper.html', context)
            author.append(a)
        if request.user.profile.scholar not in author:
            context['log'] = "You can only add your own paper!"
            return render(request, 'addpaper.html', context)
        p = Paper.objects.get_or_create(title=title, conf_id__year=year, href=href, conf_id=conf)
        if p[1]:
            area = Conference_Area.objects.get(conf_id=conf).area
            for a in author:
                Scholar_Paper.objects.get_or_create(scholar_name=a, paper_title=p[0])
                Scholar_Area.objects.get_or_create(scholar_name=a, area=area)
                a.pub_cnt += 1
                a.save()
                ins = a.affiliation
                ins.pub_cnt += 1
                ins.save()
                followers = User_Scholar.objects.filter(sch=a)
                for f in followers:
                    f.new_paper = True
                    f.save()
            context['log'] = "Add Paper %s Successfully!" % (title)
        else:
            context['log'] = "Paper %s has already been added!" % (title)
    return render(request, 'addpaper.html', context)
