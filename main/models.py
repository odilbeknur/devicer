from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image
import qrcode
from devicer_admin.models import Responsible
from rooms.models import Room

class Category(models.Model):
    category_choices = [
        ('computer', 'Стационарный ПК'),
        ('monitor', 'Монитор'),
        ('laptop', 'Ноутбук'),
        ('monoblock', 'Моноблок'),
        ('printer', 'Принтер'),
        ('phone', 'Телефон'),
        ('fax', 'Факс'),
        ('shredder', 'Шредер'),
        ('router', 'Роутер'),
        ('hard_disk', 'Хард'),
        ('usb', 'Флешка'),                          
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images')
    
    def __str__(self) -> str:
        return self.name

    
class Model(models.Model):
    category_id = models.ForeignKey(Category, related_name='devices_model', on_delete=models.PROTECT, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images')

    def __str__(self) -> str:
        return self.name

class Device(models.Model):
    category_id = models.ForeignKey(Category, related_name='device_category', on_delete=models.PROTECT, blank=True)
    model_id = models.ForeignKey(Model, on_delete=models.PROTECT, blank=True)
    responsible_id = models.ForeignKey(Responsible, on_delete=models.PROTECT)
    #username = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #processor = models.CharField(max_length=70, blank=True)
    #memory = models.CharField(max_length=70, blank=True)
    mac_address = models.CharField(max_length=50, blank=True)
    #ip_address = models.CharField(max_length=50, blank=True)
    inventory_number = models.CharField(max_length=10, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    qr_code = models.ImageField(blank=True, upload_to='qr-code')
    
    def generate_inventory_number(self):
        category_code = self.category_id.id if self.category_id else ""
        model_code = self.model_id.id if self.model_id else ""
        room_number = self.room if self.room else ""
        last_increment = Device.objects.aggregate(models.Max('id'))['id__max'] or 0
        increment = str(last_increment + 1).zfill(4) 
        return f"{category_code}{model_code}{room_number}{increment}"

    def generate_qr_code(self):
        qr_data = f'http://10.40.9.135:8000/main/dashboard/{self.inventory_number}/device-detail'
        try:
            return qrcode.make(qr_data)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    def save_qr_code_image(self, qr_image):
        if qr_image:
            try:
                filename = f'{self.inventory_number}--{self.responsible_id.fullname}--qrcode.png'
                qr_offset = Image.new('RGB', (600, 600), 'white')
                qr_offset.paste(qr_image)
                with BytesIO() as stream:
                    qr_offset.save(stream, 'PNG')
                    self.qr_code.save(filename, File(stream), save=False)
            except Exception as e:
                print(f"Error saving QR code image: {e}")

    def save(self, *args, **kwargs):
        if not self.inventory_number:
            self.inventory_number = self.generate_inventory_number()
        if not self.qr_code:
            qr_image = self.generate_qr_code()
            self.save_qr_code_image(qr_image)
        super().save(*args, **kwargs)
