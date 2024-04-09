from dataclasses import fields
from django import forms
from .models import Device, Category, Responsible, Model
from rooms.models import Room
from django.core.exceptions import ValidationError
from django.utils.safestring import SafeString


department_choices = (
        ('', 'Выберите отдел'),
        ('Отдел цифровизации', 'Отдел цифровизации'),
        ('Отдел инвестиций', 'Отдел инвестиций'),
        ('Международный отдел', 'Международный отдел')

)
                
position_choices = (
        ('', 'Выберите должность'),
        ('Тех.персонал', 'Тех.персонал'),
        ('Ведущий специалист', 'Ведущий специалист'),
        ('Главный специалист', 'Главный специалист'),
        ('Начальник отдела', 'Начальник отдела'),
        ('Начальник управления', 'Начальник управления'),

) 
status_choices = (
       ('True', 'В сети'),
       ('False', 'Не в сети'),
    )    



class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        labels = {
            'name': 'Категория',
            'image': 'Категория (фото)',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ModelCreateForm(forms.ModelForm):
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    class Meta:
        model = Model
        fields = ['category_id', 'name', 'description', 'image']
        labels = {
            'category': 'Категория',
            'name':'Модель', 
            'description':'Описание', 
            'image': 'Фото'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.initial['position'] = ''

class ModelUpdateForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['category_id', 'name', 'description', 'image']
        labels = {
            'category_id': 'Категория',
            'name': 'Модель',
            'description': 'Описание',
            'image': 'Фото'
        }
        widgets = {
            'category_id': forms.Select(attrs={'class': "form-control"}),
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control", 'rows': 3}),
            'image': forms.FileInput(attrs={'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        

class ResponsibleCreateForm(forms.ModelForm):
    position = forms.ChoiceField(choices=position_choices, label='Должность')
    department = forms.ChoiceField(choices=department_choices, label='Отдел')

    class Meta:
        model = Responsible
        fields = ['fullname', 'username', 'department', 'position', 'image']
        labels = {
            'fullname': 'Ф.И.О. ответственного',
            'username':'Логин',
            'department': 'Отдел',
            'position':'Должность',
            'image': 'Фото'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.initial['position'] = ''





class DeviceCreateForm(forms.ModelForm):
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', 
                                         widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4", 'hx-get': 'modelslist/', 'hx-target': '#models'}))
    model_id = forms.ModelChoiceField(queryset=Model.objects.none(), label='Модель', 
                                      widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4", 'id':"models"}))
    responsible_id = forms.ModelChoiceField(queryset=Responsible.objects.all(), label='Ответственный', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Комната', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    
    class Meta:
        model = Device
        fields = ['category_id', 'model_id', 'responsible_id', 'room', 'mac_address', 'description']
        labels = {
            'category_id': 'Категория',
            'model_id': 'Модель',
            'responsible_id': 'Ответственный',
            #'username': '',
            'room': 'Комната',
            #'processor': 'Процессор',
            #'memory': 'Память',
            'mac_address': 'MAC-адрес',
            #'ip_address': 'IP-адрес',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        if "category_id" in self.data:
            category_id = int(self.data.get("category_id"))
            self.fields['model_id'].queryset = Model.objects.filter(category_id=category_id)
        
class DeviceUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Device
        fields = ['category_id', 'model_id', 'responsible_id', 'room', 'mac_address', 'description']
        labels = {
            'category_id': 'Категория',
            'model_id': 'Модель',
            'responsible_id': 'Ответственный',
            'room': 'Комната',
            'mac_address': 'MAC-адрес',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
class NewDeviceForm(forms.ModelForm): 
    responsible_id = forms.ModelChoiceField(queryset=Responsible.objects.all(), label='Ответственный', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Комната', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    class Meta:
        model = Device
        fields = ['responsible_id', 'room']        
    labels = {
            'responsible_id': 'Категория',
            'room': 'Модель',
        }



