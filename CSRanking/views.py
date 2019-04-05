from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area

class paper(object):
	def __init__(self,p_year,title):
		self.p_year = p_year
		self.title = title

def main(request):
	ctx = {}
	print(request.GET)
	if request.GET and 'key' in request.GET:
		p1 = paper('2018','ABC')
		p2 = paper('2019','DEF')
		ctx = {'p_lst':[p1,p2]}
	return render(request,"main.html",ctx)
	
def scholar(request):
	if request.POST:
		ctx = {}
		ctx["scholar_page"] = '''<div class="scholar" class="container-fluid">
		<h1>ZZB</h1>			
		<p>DBLP</p>
		<p>affiliation</p>
	</div>
	<div class="scholar" class="container-fluid">
		<h1 style="display:inline-block;margin-bottom:25px;">Papers</h1>
		<div class="scholar_paper">
			<p class="paper_year">paper's year</p>
			<h2>paper title</h2>
			<p><pre>scholar</pre></p>
			<p><pre>conference's name	year	DBLP	Href</pre></p>
		</div>
		<div class="scholar_paper">
			<p class="paper_year">paper's year</p>
			<h2>paper title</h2>
			<p><pre>scholar</pre></p>
			<p><pre>conference's name	year	DBLP	Href</pre></p>
		</div>
		<div class="scholar_paper">
			<p class="paper_year">paper's year</p>
			<h2>paper title</h2>
			<p><pre>scholar</pre></p>
			<p><pre>conference's name	year	DBLP	Href</pre></p>
		</div>
	</div>
		'''
		print(ctx)
		return render(request,"scholar.html",ctx)
	else:
		return render(request,"scholar.html",{})