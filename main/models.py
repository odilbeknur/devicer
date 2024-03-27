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
    username = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    processor = models.CharField(max_length=70, blank=True)
    memory = models.CharField(max_length=70, blank=True)
    mac_address = models.CharField(max_length=50, blank=True)
    ip_address = models.CharField(max_length=50, blank=True)
    inventar_number = models.IntegerField(unique=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    qr_code = models.ImageField(blank=True, upload_to='qr-code')
    
    def generate_qr_code(self):
        qr_data = f'Номер инвентаризации: {self.room}\n Модель: {self.id} \n Ответственный: {self.responsible_id.fullname} \n Комната: {self.room.name} \n MAC-адрес: {self.mac_address}'
        try:
            qr_image = qrcode.make(qr_data)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
        return qr_image

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_image = self.generate_qr_code()
            if qr_image:
                files_name = f'{self.id}--{self.responsible_id.fullname}--qrcode.png'
                try:
                    qr_offset = Image.new('RGB', (600, 600), 'white')
                    qr_offset.paste(qr_image)
                    stream = BytesIO()
                    qr_offset.save(stream, 'PNG')
                    self.qr_code.save(files_name, File(stream), save=False)
                    qr_offset.close()
                except Exception as e:
                    print(f"Error saving QR code image: {e}")
        super().save(*args, **kwargs)