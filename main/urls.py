from multiprocessing.spawn import import_main_path
from django.urls import path
from .views import Dash_View, baseview, DeviceCreateView, CategoryCreateView, ResponsibleCreateView, ModelCreateView, DeviceDetailView, models_view, newview
from . import views

urlpatterns = [
    path('dashboard/', Dash_View, name='dashboard'),
    path('dashboard/models_view/', models_view, name='models_view'),
    path('dashboard/<int:pk>/device-detail', DeviceDetailView, name='device-detail'),
    path('dashboard/table/<int:pk>', baseview, name='base'),
    path('dashboard/new_view/', newview, name='new_view'),


    path('dashboard/add-device', DeviceCreateView.as_view(), name='device-create'),
    path('dashboard/category-create', CategoryCreateView.as_view(), name='category-create'),  
    path('dashboard/responsible-create', ResponsibleCreateView.as_view(), name='responsible-create'),
    path('dashboard/model-create', ModelCreateView.as_view(), name='model-create'),
]               