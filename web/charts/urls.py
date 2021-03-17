from django.conf.urls import url
from . import movie,book,music

urlpatterns = [
    url(r'^movie/$', movie.ChartView.as_view(), name='charts'),
    url(r'^book/$', book.ChartView.as_view(), name='charts'),
    url(r'^music/$', music.ChartView.as_view(), name='charts'),
]