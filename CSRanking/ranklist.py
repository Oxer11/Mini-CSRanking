from django.shortcuts import render, render_to_response
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

def ranklist(request):
	if request.method == "POST":
		pagenum = request.POST.get('page', "1")
		checkID = request.POST.getlist('checkID[]', [])
	else:
		pagenum = 1
		checkID = dict.values()
	ins_list = paginate(pagenum, Institution.objects.all(), 20)
	index = ins_list.start_index()
	Ins_list = []
	for ins in ins_list:
		sch_list = Scholar.objects.filter(affiliation=ins).order_by("-pub_cnt")
		Sch_list = []
		for sch in sch_list:
			area_list = Scholar_Area.objects.filter(scholar_name=sch)
			area_list = [dict[x.area.name] for x in area_list]
			if (len(list(set(checkID).intersection(set(area_list))))):
				Sch_list.append((sch, area_list))
		Ins_list.append((ins, len(sch_list), Sch_list, index))
		index += 1
	context = {
		"Ins_list": Ins_list,
		"Previous": max(ins_list.number - 1, 1),
		"Next": min(ins_list.number + 1, ins_list.paginator.num_pages)
	}
	if request.method == 'POST':
		return render_to_response("rank.html", context)
	else:
		return render(request, "ranklist.html", context)