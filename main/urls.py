from multiprocessing.spawn import import_main_path
from django.urls import path
from .views import Dash_View, baseview, deviceview, modelview, DeviceCreateView, CategoryCreateView, ResponsibleCreateView, ResponsibleDetailView, ModelCreateView, ModelUpdateView, DeviceDetailView, DeviceUpdateView, modelslist, newview, responsibleview

urlpatterns = [
    path('dashboard/', Dash_View, name='dashboard'),
    path('dashboard/modelslist/', modelslist, name='modelslist'),
    path('dashboard/models', modelview, name='models'),
    path('dashboard/<int:pk>/model-update', ModelUpdateView, name='model-update'),


    path('dashboard/table/<int:pk>', baseview, name='base'),
    path('dashboard/devices', deviceview, name='devices'),
    path('dashboard/scan-view/', newview, name='scan-view'),

    path('dashboard/<int:pk>/device-detail', DeviceDetailView, name='device-detail'),
    path('dashboard/<int:pk>/device-update', DeviceUpdateView, name='device-update'),


    path('dashboard/responsibles/', responsibleview, name='responsibles'),
    path('dashboard/<int:pk>/responsible-detail', ResponsibleDetailView, name='responsible-detail'),


    path('dashboard/add-device', DeviceCreateView.as_view(), name='device-create'),
    path('dashboard/category-create', CategoryCreateView.as_view(), name='category-create'),  
    path('dashboard/responsible-create', ResponsibleCreateView.as_view(), name='responsible-create'),
    path('dashboard/model-create', ModelCreateView.as_view(), name='model-create'),
]               