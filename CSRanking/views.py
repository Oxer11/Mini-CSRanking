from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area

def main(request):
	ctx = {}
	if request.GET and 'key' in request.GET and request.GET['key'] != request.GET['key'].strip() and  request.GET['type'] != request.GET['type'].strip():
		ctx['type'] = 'scholar'
		if ctx['type'] == 'scholar':
			ctx['sch_lst']=[]
	return render(request,"main.html",ctx)
	
def scholar(request):
	if request.POST:
		ctx = {}
		ctx["scholar_page"] = 
		print(ctx)
		return render(request,"scholar.html",ctx)
	else:
		return render(request,"scholar.html",{})