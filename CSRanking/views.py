from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area, Scholar_Area, Conference_Area, Scholar_Paper

def main(request):
	scholar = Scholar.objects.get(name="Xipeng Qiu")
	return render(request, "main.html", {'scholar': scholar})
	if request.POST:
		ctx = {}
		ctx["search_r"] = '''<div>
			<p class="paper_year">2018</p>
			<h2>Title</h2>
			<p><a class="sch_href" href="main">zzb</a></p>
			<p><pre>conference's name	year	DBLP	Href</pre></p>
		</div>
		'''
		return JsonResponse(ctx)
	else:
		return render(request,"main.html",{})
	
def scholar(request):
	person_name = request.GET.get('name', "NONE")
	try:
		person = Scholar.objects.get(name=person_name)
	except Scholar.DoesNotExist:
		return HttpResponse("This person does not exist!")
	areas = Scholar_Area.objects.filter(scholar_name=person)
	areas = [x.area for x in areas]
	paper_list = Scholar_Paper.objects.filter(scholar_name=person)
	paper_list = [x.paper_title for x in paper_list]
	author_list = []
	for paper in paper_list:
		authors = Scholar_Paper.objects.filter(paper_title=paper)
		authors = [x.scholar_name for x in authors]
		author_list.append(authors)
	context = {
		'scholar': person,
		'areas': areas,
		'paper_list': paper_list,
		'author_list': author_list,
	}
	return render(request, "scholar.html", context)

def conference(request):
	abbr, year = request.GET.get("name", "NONE"), request.GET.get("year", 0)
	try:
		conf = Conference.objects.get(abbr=abbr, year=year)
	except Conference.DoesNotExist:
		return HttpResponse("This conference does not exist!")
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
	print(area_list)
	print(paper_list)
	context = {
		"ins": Ins,
		"area_list": area_list,
		"scholar_list": scholar_list,
		"paper_list": paper_list,
	}
	return render(request, "institution.html", context)
