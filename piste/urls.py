from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('pistes/', views.listPisteList, name='pistes'),
    path("pistes/delete-piste/<int:id>", views.deletePisteView, name="delete_piste"),
    path("pistes/edit-piste/<int:id>", views.editPisteView, name="edit_piste"),
    path("pistes/create-piste/", views.createPisteView, name="create_piste"),
    path('pistes/detail-piste/<int:id>', views.pisteDetailsView, name='detail_piste'),

    path('pistes/<int:pk>/confirm/', views.confirmPiste, name='confirm_piste'),
    path('pistes/<int:pk>/cancel/', views.cancelPiste, name='cancel_piste'),

    path('live_search/', live_search, name='live_search'),
]