from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from CSRanking.models import Scholar, Institution, Paper, Conference, Area

def main(request):
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