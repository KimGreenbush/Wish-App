from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('wishes/', views.dashboard),
    path('wishes/stats/', views.stats),
    path('wishes/new/', views.new_wish),
    path('wishes/new/add', views.add_a_wish),
    path('wishes/edit/<int:wish_id>/', views.edit_wish),
    path('wishes/edit/<int:wish_id>/update/', views.update_wish),
    path('wishes/delete/<int:wish_id>/', views.delete_wish),
    path('wishes/<int:wish_id>/granted/', views.grant_wish),
    path('wishes/<int:wish_id>/like/', views.like_wish)
]
