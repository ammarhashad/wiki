from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/",views.topic, name = "topic"),
    path('search/', views.search, name = 'search'),
    path('create/', views.create, name='create'),
    path('save_create/', views.save_create, name='save_create'),
    path("edit/", views.edit, name='edit'),
    path("save/", views.save, name='save'),
    path('rondom/', views.random_func, name='rondom'),
]

# for topic in topics:
#     urlpatterns.append(path(<str:name>topic+'/',views.topic, name = topic))
