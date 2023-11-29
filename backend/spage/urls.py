from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="test"),
    path("<int:num>", views.section, name="section")
]
