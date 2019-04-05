from django.urls import path
import CSRanking.views as views
urlpatterns = [
    path('', views.index, name='index'),
]