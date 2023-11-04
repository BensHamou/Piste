from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('pistes/', views.listPisteList, name='pistes'),
    path("pistes/delete-piste/<int:id>", views.deletePisteView, name="delete_piste"),
    path("pistes/edit-piste/<int:id>", views.editPisteView, name="edit_piste"),
    path("pistes/create-piste/", views.createPisteView, name="create_piste"),
]