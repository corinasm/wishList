from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^create_item$', views.create_item),
    url(r'^delete_item/(?P<item_id>\d+)$', views.delete_item),
    url(r'^add_item/(?P<item_id>\d+)$', views.addToMyWishlist),
    url(r'^remove_item/(?P<item_id>\d+)$', views.removeFromMyWishlist),
    url(r'^wish_items/(?P<item_id>\d+)$', views.show)

]    