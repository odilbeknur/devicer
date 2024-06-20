from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Category, Model, Device
from devicer_admin.models import Responsible
from django.db.models import Count, Q
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CategoryCreateForm, DeviceCreateForm, ResponsibleCreateForm, ModelCreateForm, NewDeviceForm, DeviceUpdateForm, ModelUpdateForm
from django.contrib import messages
import requests
import os



# Create your views here.
def Dash_View(request):
    categories = Category.objects.annotate(device_count=Count('device_category'))
    return render(request, 'admin/admin-index.html', {'queryset': categories})

def baseview(request, pk):
    query = Device.objects.filter(category_id__id=pk)
    get_cat = Category.objects.filter(id=pk)
    return render(request, 'admin/admin-base.html', {'query': query, 'get_cat': get_cat})

def deviceview(request):
    query = Device.objects.all()
    return render(request, 'admin/admin-device.html', {'query': query})


def modelview(request):
    query = Model.objects.all()
    return render(request, 'admin/admin-model.html', {'query': query})


def responsibleview(request):
    responsibles = Responsible.objects.all()
    return render(request, 'admin/responsible-base.html', {'responsibles': responsibles})

def newview(request):
    #pull data from third party rest api
    #response = requests.get('http://10.20.6.60:8000/computers')
    response = requests.get('http://10.40.9.134:8000/computers')
    query = response.json()


    device_data = Device.objects.values_list('mac_address', 'responsible_id')
    responsible_mapping = {responsible.id: responsible.username for responsible in Responsible.objects.all()}
    saved_data = [(mac_address, responsible_mapping.get(responsible_id)) for mac_address, responsible_id in device_data]


    context = {
        'saved_data' : saved_data
    }

    form = NewDeviceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('scan-view')
    
    return render(request, "admin/scan-view.html", {'query': query, 'context': context, 'form':form})


def modelslist(request):
    category_id = request.GET.get('category_id')
    models  = Model.objects.filter(category_id=category_id)
    return render(request, 'admin/model-options.html', {"models": models})

class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin/category-create.html'
    login_url = 'login'
    success_url = reverse_lazy('category-create')
    success_message = "Категория успешно добавлена"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_url'] = self.request.path
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error: {e}')
            return self.form_invalid(form)

class ModelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Model
    form_class = ModelCreateForm
    template_name = 'admin/model-create.html'
    login_url = 'login'
    success_url = reverse_lazy('model-create')
    success_message = "Mодель успешно добавлена"

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error: {e}')
            return self.form_invalid(form)
        

class ResponsibleCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Responsible
    form_class = ResponsibleCreateForm
    template_name = 'admin/responsible-create.html'
    login_url = 'login'
    success_url = reverse_lazy('responsible-create')
    success_message = "Ответственный успешно добавлен"

    def form_valid(self, form):
         form.instance.author = self.request.user
         try:
                return super().form_valid(form)
         except Exception as e:
                messages.error(self.request, f'Error: {e}')
                return self.form_invalid(form)


class DeviceCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceCreateForm
    template_name = 'admin/device-create.html'
    login_url = 'login'
    success_url = reverse_lazy('device-create')
    success_message = "Устройство успешно добавлено"

    def form_valid(self, form):
         form.instance.author = self.request.user
         try:
                return super().form_valid(form)
         except Exception as e:
                messages.error(self.request, f'Error: {e}')
                print(f'Error: {e}')
                return self.form_invalid(form)
         

def DeviceDetailView(request, pk):
    device = get_object_or_404(Device, inventory_number=pk)
    responsible = get_object_or_404(Responsible, id=device.responsible_id.id)
    model = get_object_or_404(Model, id=device.model_id.id)

    # Get the fullname from the device
        #form = ProductDetailUpdateForm(request.POST or None, instance=eq)
        #if request.method == 'POST' and form.is_valid():
        #    form.save()
        #    return redirect('device-detail', pk=eq.pk)
   
    return render(request, 'admin/admin-detail.html', {'d': device ,'responsible':responsible, 'm':model})

def ResponsibleDetailView(request, pk):
    responsible = get_object_or_404(Responsible, id=pk)
    device = Device.objects.filter(responsible_id=responsible.id)

    response = requests.get('http://10.20.6.60:8000/computers')
    query = response.json()

    address = [item for item in query if item['user_name'] == responsible.username]


    return render(request, 'admin/responsible-detail.html', {'responsible':responsible, 'device': device, 'address': address})

def ModelUpdateView(request, pk):
    model_instance = get_object_or_404(Model, pk=pk)
    images = Model.objects.filter(image=model_instance.image)
     
    if request.method == 'POST':
        form = ModelUpdateForm(request.POST, request.FILES, instance=model_instance)
        if form.is_valid():
            # Check if a new image has been uploaded
            if 'image' in request.FILES:
                # Delete old image if it exists
                if model_instance.image:
                    old_image_path = model_instance.image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
            form.save()
            return redirect('models')  # Assuming 'models' is the URL name for the model list view
    else:
        form = ModelUpdateForm(instance=model_instance)

    return render(request, 'admin/model-update.html', {'form': form, 'images':images})

def DeviceUpdateView(request, pk):
    device = get_object_or_404(Device, pk=pk)
    key = device.category_id.id
    form = DeviceUpdateForm(request.POST or None, instance=device)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('base', pk=key)  
    else:
        form = DeviceUpdateForm(instance=device)

    return render(request, 'admin/device-update.html', {'form': form})


      

