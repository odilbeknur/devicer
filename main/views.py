from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Category, Model, Device
from devicer_admin.models import Responsible
from django.db.models import Count, Q
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CategoryCreateForm, DeviceCreateForm, ResponsibleCreateForm, ModelCreateForm, NewDeviceForm
from django.contrib import messages
import requests



# Create your views here.
def Dash_View(request):
    categories = Category.objects.annotate(count=Count('name'))
    active_url = request.path
    return render(request, 'admin/admin-index.html', {'queryset': categories, 'active_url': active_url})

def baseview(request, pk):
    query = Device.objects.filter(category_id__id=pk)
    get_cat = Category.objects.filter(id=pk)
    active_url = request.path
    return render(request, 'admin/admin-base.html', {'query': query, 'get_cat': get_cat})

def newview(request):
    #pull data from third party rest api
    response = requests.get('http://10.40.9.25:8001/computers/')
    query = response.json()


    form = NewDeviceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('scan-view')
    
    return render(request, "admin/scan-view.html", {'query': query, 'form':form})

def get_device_list(request):
     
    response = requests.get('http://10.40.9.25:8001/computers/')
    query = response.json()


    return render(request, 'admin/scanlist.html', {'query': query, 'form':form})

def savescan(request):
    comp_name = request.POST.get('comp_name')
    user_name = request.POST.get('user_name')
    ram = request.POST.get('ram')
    ip_address = request.POST.get('ip_address')
    mac_address = request.POST.get('mac_address')

    # Create a new instance of your model and save it to the database
    new_device = Device(
        category_id = "Персональный компьютер",
        model_id = "Dell",
        responsible_id = "Дастан",
        username = user_name,
        room="200", 
        processor="Test", 
        memory=ram, 
        ip_address=ip_address, 
        mac_address=mac_address,
        description = "Test"
        )
    new_device.save()
    
    return render(request, "admin/scan-view.html", {'query': query, 'form':form})

def edit_student(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    context = {}
    context['student'] = student
    context['form'] = StudentForm(initial={
        'first_name':student.first_name,
        'last_name': student.last_name,
        'gender': student.gender,
        'age': student.age,
        'major': student.major
    })
    return render(request, 'partial/student/edit_student.html', context)

def edit_student_submit(request, student_pk):
    context = {}
    student = Student.objects.get(pk=student_pk)
    context['student'] = student
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'partial/student/edit_student.html', context)
    return render(request, 'partial/student/student_row.html', context)    



def models_view(request):
    category_id = request.GET.get('category_id')
    models  = Model.objects.filter(category_id=category_id)
    return render(request, 'admin/model-options.html', {"models": models})

def add_selected_devices(request):
    if request.method == 'POST':
        selected_device_ids = request.POST.getlist('selected_devices')
        if selected_device_ids:
            try:
                # Retrieve the selected devices from the database
                selected_devices = Device.objects.filter(id__in=selected_device_ids)
                
                # Add any additional processing logic here if needed
                for device in selected_devices:
                    # Example additional processing: Update status or perform validation
                    device.is_selected = True
                    device.save()

                return JsonResponse({'success': True})
            except Device.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'One or more devices not found.'})
        else:
            return JsonResponse({'success': False, 'error': 'No devices selected.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})


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
   
    print(responsible.image)
    return render(request, 'admin/admin-detail.html', {'d': device ,'responsible':responsible, 'm':model})



def edit_device(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    context = {}
    context['student'] = student
    context['form'] = StudentForm(initial={
        'first_name':student.first_name,
        'last_name': student.last_name,
        'gender': student.gender,
        'age': student.age,
        'major': student.major
    })
    return render(request, 'partial/student/edit_student.html', context)

def edit_device_submit(request, student_pk):
    context = {}
    student = Student.objects.get(pk=student_pk)
    context['student'] = student
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'partial/student/edit_student.html', context)
    else:
        return render(request, 'partial/student/student_row.html', context)
