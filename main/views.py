from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Category, Model, Device
from devicer_admin.models import Responsible
from django.db.models import Count, Q
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CategoryCreateForm, DeviceCreateForm, ResponsibleCreateForm, ModelCreateForm
from django.contrib import messages



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

def models_view(request):
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
    query = Device.objects.filter(id=pk)
    responsible = Responsible.objects.filter(id=pk)
    #form = ProductDetailUpdateForm(request.POST or None, instance=eq)
    #if request.method == 'POST' and form.is_valid():
    #    form.save()
    #    return redirect('device-detail', pk=eq.pk)
    return render(request, 'admin/admin-detail.html', {'query': query ,'responsible':responsible})