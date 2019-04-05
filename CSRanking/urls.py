from django.conf.urls import url
import CSRanking.views as views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	url(r'scholar', views.scholar, name='scholar'),
	url(r'conference', views.conference, name='conference'),
	url(r'institution', views.institution, name='institution'),
]