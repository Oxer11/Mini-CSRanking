from django.conf.urls import url
import CSRanking.views as views

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
	url(r'pro_edit',views.pro_edit,name='pro_edit'),
	url(r'paper',views.paper,name='paper'),
]