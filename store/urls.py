from django.conf.urls import url
from . import views

app_name = 'store'
urlpatterns = [
    url(r'^cart/$',views.cart,name="cart"),
    url(r'^checkout/$',views.checkout,name="checkout"),
    url(r'^updateitem/$', views.updateitem, name="updateitem"),
    url(r'^processorder/$', views.processorder, name="processorder"),
    url(r'^search/$',views.searchitem,name="searchitem"),
    url(r'^filter/$',views.filteritem,name="filteritem"),
    url(r'^detail/(?P<id>\d+)/$',views.detailitem,name="detailitem"),
    url(r'^$',views.store,name="store"),
]