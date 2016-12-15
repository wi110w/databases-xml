from django.conf.urls import url
from . import views

app_name = 'library'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<record_num>[0-9]+)/$', views.detail, name='detail'),
    url(r'^reader/(?P<reader_id>[A-Za-z]+)/$', views.detail_reader, name='detail_reader'),
    url(r'^librarian/(?P<lib_id>[A-Za-z]+)/$', views.detail_librarian, name='detail_librarian'),
    url(r'^book/(?P<book_id>[ A-Z a-z ]+)/$', views.detail_book, name='detail_book'),
    url(r'^add/$', views.add_record, name='add'),
    url(r'^edit/(?P<record_num>[0-9]+)/$', views.edit_record, name='edit'),
    url(r'^delete/(?P<record_num>[0-9]+)/$', views.delete_record, name='delete'),
    url(r'^reset/$', views.reset_data, name='reset'),
    url(r'^sort/$', views.sort_data, name='sort'),
    url(r'^statistics/$', views.statistics, name='statistics')
]