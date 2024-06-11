from django.urls import path
from . import views

urlpatterns = [
    path('create-save/', views.SaveViews.as_view(), name='create-save'),
    path('get-save/', views.GetSaveViews.as_view(), name='get-save')
]
