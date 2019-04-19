from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import Permission, User
from django.contrib.auth import *
from django.contrib.auth.decorators import *
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area, Scholar_Area, Conference_Area, Scholar_Paper, Profile, User_Scholar, User_Area, User_Institution, User_Conference

def paginate(page, out_list, num):
    paginator = Paginator(out_list, num)
    try:
        out_list = paginator.page(page)
    except PageNotAnInteger:
        out_list = paginator.page(1)
    except EmptyPage:
        out_list = paginator.page(paginator.num_pages)
    return out_list

def index(request):
	return render(request, "index.html", {})

def main(request):
	if 'key' in request.GET and 'type' in request.GET:
		key = request.GET.get('key')
		if key.strip() == '':
			return HttpResponseRedirect(reverse('index'))
		else:
			type = request.GET.get('type')
			ctx = {}
			ctx['type'] = type
			ctx['key'] = key
			pagenum = request.GET.get('page')
			if type == 'scholar':
				sch_lst = paginate(pagenum, Scholar.objects.filter(name__contains=key), 10)
				ctx['out_lst'] = sch_lst
			elif type == 'paper':
				paper_lst = paginate(pagenum, Paper.objects.filter(title__contains=key), 20)
				ctx['out_lst'] = paper_lst
				author_lst = []
				for paper in paper_lst:
					authors = Scholar_Paper.objects.filter(paper_title=paper)
					authors = [x.scholar_name for x in authors]
					author_lst.append(authors)
				ctx['author_lst'] = author_lst
			elif type == 'institution':
				ins_lst = paginate(pagenum, Institution.objects.filter(name__contains=key), 10)
				print(ins_lst[0].homepage)
				ctx['out_lst'] = ins_lst
			elif type == 'conference':
				conf_lst = Conference.objects.filter(name__contains=key)
				conf_lst = conf_lst|Conference.objects.filter(abbr__contains=key)
				conf_lst = list(set(conf_lst))
				conf_lst = paginate(pagenum, conf_lst, 10)
				ctx['out_lst'] = conf_lst
			else:
				area_lst = Area.objects.filter(name__contains=key)
				area_lst = paginate(pagenum, area_lst, 10)
				ctx['out_lst'] = area_lst
			P = ctx['out_lst']
			page_range = range(max(P.number - 3, 1), min(P.number + 3, P.paginator.num_pages) + 1)
			ctx['page_range'] = page_range
			return render(request,"main.html",ctx)
	else:
		return HttpResponseRedirect(reverse('index'))
	
def scholar(request):
	user = request.user
	person_name = request.GET.get('name', "NONE")
	try:
		person = Scholar.objects.get(name=person_name)
	except Scholar.DoesNotExist:
		return HttpResponse("This person does not exist!")
	if request.method == "POST":
		if user:
			type = request.POST.get('type', "NONE")
			if type == 'Follow':
				User_Scholar.objects.get_or_create(user=user, sch=person)
				print("Follow Successfully!")
				return JsonResponse({"Type":"Unfollow"})
			elif type == 'Unfollow':
				User_Scholar.objects.get(user=user, sch=person).delete()
				print("Unfollow Successfully!")
				return JsonResponse({"Type": "Follow"})
			else: print("Follow Type Error!")
	Type = ""
	if len(User_Scholar.objects.filter(user=user, sch=person))>=1: Type = "Unfollow"
	else: Type = "Follow"
	areas = Scholar_Area.objects.filter(scholar_name=person)
	areas = [x.area for x in areas]
	paper_list = Scholar_Paper.objects.filter(scholar_name=person)
	paper_list = [x.paper_title for x in paper_list]
	author_list = []
	co_authors = []
	for paper in paper_list:
		authors = Scholar_Paper.objects.filter(paper_title=paper)
		authors = [x.scholar_name for x in authors]
		co_authors += authors
		author_list.append(authors)
	co_authors = list(set(co_authors))
	if len(co_authors)>=1: co_authors.remove(person)
	co_authors.sort(key=lambda co_author: co_author.pub_cnt, reverse=True)
	context = {
		'scholar': person,
		'areas': areas,
		'paper_list': paper_list,
		'author_list': author_list,
		'co_authors': co_authors,
		'Type': Type,
	}
	return render(request, "scholar.html", context)

def conference(request):
	abbr, year = request.GET.get("name", "NONE"), request.GET.get("year", 0)
	#try:
	conf = Conference.objects.get(abbr=abbr, year=year)
	#except Conference.DoesNotExist:
		#return HttpResponse("This conference does not exist!")
	areas = Conference_Area.objects.filter(conf_id=conf)
	areas = [x.area for x in areas]
	paper_list = Paper.objects.filter(conf_id=conf)
	author_list = []
	for paper in paper_list:
		authors = Scholar_Paper.objects.filter(paper_title=paper)
		authors = [x.scholar_name for x in authors]
		author_list.append(authors)
	context = {
		'conf': conf,
		'area_list': areas,
		'paper_list': paper_list,
		'author_list': author_list,
	}
	return render(request, "conference.html", context)

def institution(request):
	name = request.GET.get("name", "NONE")
	try:
		Ins = Institution.objects.get(name=name)
	except Institution.DoesNotExist:
		return HttpResponse("This institution does not exist!")
	scholar_list = Scholar.objects.filter(affiliation=Ins)
	area_list = []
	paper_list = []
	for scholar in scholar_list:
		areas = Scholar_Area.objects.filter(scholar_name=scholar)
		areas = [x.area for x in areas]
		area_list.append(areas)
		papers = Scholar_Paper.objects.filter(scholar_name=scholar)
		papers = [x.paper_title for x in papers]
		if len(papers)>=5: papers = papers[0:5]
		paper_list.append(papers)
	context = {
		"ins": Ins,
		"area_list": area_list,
		"scholar_list": scholar_list,
		"paper_list": paper_list,
	}
	return render(request, "institution.html", context)

def area(request):
	name = request.GET.get("name", "NONE")
	try:
		area = Area.objects.get(name=name)
	except Area.DoesNotExist:
		return HttpResponse("This institution does not exist!")
	conf_list = Conference_Area.objects.filter(area=area)
	conf_list = [c.conf_id for c in conf_list]
	scholar_list = Scholar_Area.objects.filter(area=area)
	scholar_list = [s.scholar_name for s in scholar_list][0:5]
	paper_list = []
	for scholar in scholar_list:
		papers = Scholar_Paper.objects.filter(scholar_name=scholar)
		papers = [x.paper_title for x in papers]
		if len(papers)>=5: papers = papers[0:5]
		paper_list.append(papers)
	context = {
		"area": area,
		"conf_list": conf_list,
		"scholar_list": scholar_list,
		"paper_list": paper_list,
	}
	return render(request, "area.html", context)
	
def Login(request):	
	if 'submit' in request.GET and request.GET.get('submit')=='signup':
		username = request.GET.get('username')
		email = request.GET.get('email')
		password = request.GET.get('password')
		if username.strip()=='' or email.strip()=='' or password.strip()=='':
			return render(request,'login.html',{})
		user = User.objects.create_user(username,email,password)
		login(request,user)
		print("Successfully create user:")
		print(user.profile)
		return HttpResponseRedirect(reverse('index'))
	elif 'submit' in request.GET and request.GET.get('submit')=='signin':
		username = request.GET.get('username')
		password = request.GET.get('password')
		if username.strip()=='' or password.strip()=='':
			return render(request,'login.html',{})
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			print('Successfully log in:')
			print(user.profile)
			return HttpResponseRedirect(reverse('index'))
		else:
			return HttpResponseRedirect(reverse('login'))
	elif 'submit' in request.GET and request.GET.get('submit')=='signout':
		logout(request)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request,'login.html',{})

@login_required
def profile(request):
	user = request.user
	sch = User_Scholar.objects.filter(user=user)
	schs = [s.sch for s in sch]
	print(len(schs))
	return render(request,'profile.html',{'user':user, 'sch':schs})