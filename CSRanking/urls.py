from django.conf.urls import url
import CSRanking.views as views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	url(r'scholar', views.scholar, name='scholar'),
]