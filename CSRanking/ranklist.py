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

def ranklist(request):
    pagenum = request.GET.get('page')
    ins_list = paginate(pagenum, Institution.objects.all(), 50)
    Ins_list = []
    for ins in ins_list:
        sch_list = Scholar.objects.filter(affiliation=ins).order_by("-pub_cnt")
        Ins_list.append((ins, len(sch_list), sch_list))
    context = {
        "Ins_list": Ins_list,
    }
    return render(request, "ranklist.html", context)