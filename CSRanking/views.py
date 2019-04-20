from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import Permission, User
from django.contrib.auth import *
from django.contrib.auth.decorators import *
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area, Scholar_Area, Conference_Area, Scholar_Paper, Profile, User_Scholar, User_Area, User_Institution, User_Conference

dict = {
	'Artificial intelligence': 'AI',
	'Computer vision': 'Vision',
	'Machine learning': 'ML',
	'Data mining': 'DM',
	'Natural language processing': 'NLP',
	'The Web & information retrieval': 'Web+IR',
	'Computer architecture': 'Arch',
	'Computer networks': 'Networks',
	'Computer security': 'Security',
	'Databases': 'DB',
	'Design automation': 'EDA',
	'Embedded & real-time systems': 'Embedded',
	'High-performance computing': 'HPC',
	'Mobile computing': 'Mobile',
	'Measurement & perf. analysis': 'Metrics',
	'Operating systems': 'OS',
	'Programming languages': 'PL',
	'Software engineering': 'SE',
	'Algorithms & complexity': 'Theory',
	'Cryptography': 'Crypto',
	'Logic & verification': 'Logic',
	'Comp. bio & bioinformatics': 'Comp. Bio',
	'Computer graphics': 'Graphics',
	'Economics & computation': 'ECom',
	'Human-computer interaction': 'HCI',
	'Robotics': 'Robotics',
	'Visualization': 'Visualization',
}

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
		if request.user.is_authenticated:
			type = request.POST.get('type', "NONE")
			if type == 'Follow':
				User_Scholar.objects.get_or_create(user=user, sch=person)
				return JsonResponse({"Type":"Unfollow"})
			elif type == 'Unfollow':
				User_Scholar.objects.get(user=user, sch=person).delete()
				return JsonResponse({"Type": "Follow"})
			else: print("Follow Type Error!")
	Type = "Follow"
	if request.user.is_authenticated:
		if len(User_Scholar.objects.filter(user=user, sch=person))>=1: Type = "Unfollow"
	areas = Scholar_Area.objects.filter(scholar_name=person)
	areas = [x.area for x in areas]
	paper_list = Scholar_Paper.objects.filter(scholar_name=person)
	paper_list = [x.paper_title for x in paper_list]
	pub_year_cnt = []
	for i in range(2010, 2020):
		pub_year_cnt.append((i, len(Scholar_Paper.objects.filter(scholar_name=person, paper_title__year=i))))
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
		'pub_year_cnt': pub_year_cnt,
	}
	return render(request, "scholar.html", context)

def conference(request):
	user = request.user
	abbr, year = request.GET.get("name", "NONE"), request.GET.get("year", 0)
	try:
		conf = Conference.objects.get(abbr=abbr, year=year)
	except Conference.DoesNotExist:
		return HttpResponse("This conference does not exist!")
	if request.method == "POST":
		if request.user.is_authenticated:
			type = request.POST.get('type', "NONE")
			if type == 'Follow':
				User_Conference.objects.get_or_create(user=user, conf=conf)
				return JsonResponse({"Type":"Unfollow"})
			elif type == 'Unfollow':
				User_Conference.objects.get(user=user, conf=conf).delete()
				return JsonResponse({"Type": "Follow"})
			else: print("Follow Type Error!")
	Type = "Follow"
	if request.user.is_authenticated:
		if len(User_Conference.objects.filter(user=user, conf=conf)) >= 1:
			Type = "Unfollow"
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
		"Type": Type,
	}
	return render(request, "conference.html", context)

def institution(request):
	user = request.user
	name = request.GET.get("name", "NONE")
	try:
		Ins = Institution.objects.get(name=name)
	except Institution.DoesNotExist:
		return HttpResponse("This institution does not exist!")
	if request.method == "POST":
		if request.user.is_authenticated:
			type = request.POST.get('type', "NONE")
			if type == 'Follow':
				User_Institution.objects.get_or_create(user=user, ins=Ins)
				return JsonResponse({"Type":"Unfollow"})
			elif type == 'Unfollow':
				User_Institution.objects.get(user=user, ins=Ins).delete()
				return JsonResponse({"Type": "Follow"})
			else: print("Follow Type Error!")
	Type = "Follow"
	if request.user.is_authenticated:
		if len(User_Institution.objects.filter(user=user, ins=Ins)) >= 1:
			Type = "Unfollow"
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
	area_papers = []
	for area in Area.objects.all():
		cnt = 0
		for conf in Conference_Area.objects.filter(area=area):
			conf = conf.conf_id
			papers = Scholar_Paper.objects.filter(scholar_name__in=scholar_list, paper_title__conf_id=conf)
			papers = [x.paper_title for x in papers]
			papers = list(set(papers))
			cnt += len(papers)
		area_papers.append((dict[area.name], cnt))
	context = {
		"ins": Ins,
		"area_list": area_list,
		"scholar_list": scholar_list,
		"paper_list": paper_list,
		"Type": Type,
		"area_papers":area_papers,
	}
	return render(request, "institution.html", context)

def area(request):
	user = request.user
	name = request.GET.get("name", "NONE")
	try:
		area = Area.objects.get(name=name)
	except Area.DoesNotExist:
		return HttpResponse("This Area does not exist!")
	if request.method == "POST":
		if request.user.is_authenticated:
			type = request.POST.get('type', "NONE")
			if type == 'Follow':
				User_Area.objects.get_or_create(user=user, area=area)
				return JsonResponse({"Type":"Unfollow"})
			elif type == 'Unfollow':
				User_Area.objects.get(user=user, area=area).delete()
				return JsonResponse({"Type": "Follow"})
			else: print("Follow Type Error!")
	Type = "Follow"
	if request.user.is_authenticated:
		if len(User_Area.objects.filter(user=user, area=area)) >= 1:
			Type = "Unfollow"
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
		"Type": Type,
	}
	return render(request, "area.html", context)
	
def Login(request):	
	if 'submit' in request.POST and request.POST.get('submit')=='signup':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		if username.strip()=='' or email.strip()=='' or password.strip()=='':
			return render(request,'login.html',{'signup_error':'Incomplete form'})
		if len(User.objects.filter(username=username))>=1:
			return render(request,'login.html',{'signup_error':'Username already exits'})
		user = User.objects.create_user(username,email,password)
		login(request,user)
		return HttpResponseRedirect(reverse('index'))
	elif 'submit' in request.POST and request.POST.get('submit')=='signin':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username.strip()=='' or password.strip()=='':
			return render(request,'login.html',{'signin_error':'Incomplete form'})
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request,'login.html',{'signin_error':'Wrong username or password'})
	elif 'submit' in request.POST and request.POST.get('submit')=='signout':
		logout(request)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request,'login.html',{})

@login_required
def profile(request):
	user = request.user
	return render(request, 'profile.html', {'user':user})
	
@login_required
def pro_edit(request):
	user = request.user
	if 'submit' in request.POST and request.POST.get('submit')=='save':
		old_pw = request.POST.get('old_pw')
		user_ = authenticate(username=user.username,password=old_pw)
		if user_ is not None:
			new_pw = request.POST.get('new_pw')
			cfm_pw = request.POST.get('cfm_pw')
			if new_pw != cfm_pw:
				return render(request,'pro_edit.html',{'user':user,'error':'Passwords do not match'})
			else:
				user.set_password(new_pw)
		else:
			return render(request,'pro_edit.html',{'user':user,'error':'Wrong password'})
				
		identity = request.POST.get('identity')
		if identity.strip()!='':
			print(identity)
			user.profile.identity = identity
		
		gender = request.POST.get('gender')
		if gender.strip()!='':
			print(gender)
			user.profile.gender = gender
			
		email = request.POST.get('email')
		if email.strip()!='':
			user.email = email
		
		institution = request.POST.get('institution')
		if institution.strip()!='':
			user.profile.institution = institution
		
		user.save()
		login(request,user)
		return HttpResponseRedirect(reverse('profile'))
	return render(request,'pro_edit.html',{'user':user})

@login_required
def follow(request):
	user = request.user
	sch = User_Scholar.objects.filter(user=user)
	schs = [s.sch for s in sch]
	ins = User_Institution.objects.filter(user=user)
	inss = [s.ins for s in ins]
	area = User_Area.objects.filter(user=user)
	areas = [s.area for s in area]
	conf = User_Conference.objects.filter(user=user)
	confs = [s.conf for s in conf]
	context = {
		'sch': schs,
		'ins': inss,
		'area': areas,
		'conf': confs,
	}
	return render(request,'follow.html',context)