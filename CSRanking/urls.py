from django.conf.urls import url
import CSRanking.views as views
import CSRanking.ranklist as ranklist
import CSRanking.addpaper as addpaper

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'main', views.main, name='main'),
	url(r'scholar', views.scholar, name='scholar'),
	url(r'conference', views.conference, name='conference'),
	url(r'institution', views.institution, name='institution'),
	url(r'area', views.area, name='area'),
	url(r'login',views.Login,name='login'),
	url(r'profile',views.profile,name='profile'),
	url(r'follow',views.follow,name='follow'),
	url(r'mynote',views.mynote,name='mynote'),
	url(r'myremark',views.myremark,name='myremark'),
	url(r'pro_edit',views.pro_edit,name='pro_edit'),
	url(r'^paper',views.paper,name='paper'),
	url(r'ranklist', ranklist.ranklist, name='ranklist'),
	url(r'addpaper', addpaper.addpaper, name='addpaper'),
	url(r'^note/',views.note,name='note'),
	url(r'editnote/',views.editnote,name='editnote'),	
]