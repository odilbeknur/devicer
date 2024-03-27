from dataclasses import fields
from django import forms
from .models import Device, Category, Responsible, Model
from django.core.exceptions import ValidationError
from django.utils.safestring import SafeString

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
        
position_choices = (
        ('', 'Выберите должность'),
        ('Тех.персонал', 'Тех.персонал'),
        ('Ведущий специалист', 'Ведущий специалист'),
        ('Главный специалист', 'Главный специалист'),
        ('Начальник отдела', 'Начальник отдела'),
        ('Начальник управления', 'Начальник управления'),

    )         

class ResponsibleCreateForm(forms.ModelForm):
    position = forms.ChoiceField(choices=position_choices)
    class Meta:
        model = Responsible
        fields = ['fullname', 'position', 'image']
        labels = {
            'fullname': 'Ф.И.О. ответственного',
            'position':'Должность',
            'image': 'Фото'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.initial['position'] = ''




status_choices = (
       ('True', 'В сети'),
       ('False', 'Не в сети'),
    )    

class DeviceCreateForm(forms.ModelForm):
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', 
                                         widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4", 'hx-get': 'models_view/', 'hx-target': '#models'}))
    model_id = forms.ModelChoiceField(queryset=Model.objects.none(), label='Модель', 
                                      widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4", 'id':"models"}))
    responsible_id = forms.ModelChoiceField(queryset=Responsible.objects.all(), label='Ответственный', widget=forms.Select(attrs={'class': "form-floating form-floating-outline mb-4"}))
    
    class Meta:
        model = Device
        fields = ['category_id', 'model_id', 'responsible_id', 'username', 'room', 'processor', 'memory', 'mac_address', 'ip_address', 'inventar_number', 'serial_number', 'description']
        labels = {
            'category_id': 'Категория',
            'model_id': 'Модель',
            'responsible_id': 'Ответственный',
            'username': 'Наименование',
            'room': 'Комната',
            'processor': 'Процессор',
            'memory': 'Память',
            'mac_address': 'MAC-адрес',
            'ip_address': 'IP-адрес',
            'inventar_number': 'Инвентарный номер',
            'serial_number': 'Серийный номер',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        if "category_id" in self.data:
            category_id = int(self.data.get("category_id"))
            self.fields['model_id'].queryset = Model.objects.filter(category_id=category_id)
        
        
        




