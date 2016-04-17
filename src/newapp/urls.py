from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.redirect),
	url(r'^signup$', views.signup),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^history$', views.history),
	url(r'^traininfo$', views.traininfo),
	url(r'^reserve$', views.reserve),
	url(r'^checkout$', views.checkout),
	url(r'^booklist$', views.booklist),
	url(r'^cancelled$', views.cancelled),
	url(r'^confirmed$', views.confirmed),
	url(r'^created$', views.created),
]