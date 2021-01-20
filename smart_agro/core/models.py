from django.db import models
from datetime import datetime
from django.utils.timezone import now
import uuid

# Create your models here

class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.EmailField(blank=True)

    def __str__(self):
        return str(self.name) + " (" + str(self.phone) + ")"

class Land(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    farmer = models.ManyToManyField(Farmer, related_name="lands")
    name = models.CharField(max_length=30, blank=True, default='')
    area = models.FloatField()
    currentCrops = models.CharField(max_length=30, blank=True, default='')
    address = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return str(self.name) + " (" + str(self.id) + ")"

class SoilData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    N = models.IntegerField()
    P = models.IntegerField()
    K = models.IntegerField()
    S = models.IntegerField()
    pH = models.FloatField()
    moisture = models.IntegerField()


    def __str__(self):
        return self.land.__str__() +" (" + self.time.strftime('%I:%M:%S %p, %d-%m-%Y') +")"

class CropsData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    crops_name = models.CharField(max_length=30, blank=True, default='')
    N = models.IntegerField()
    t_N = models.IntegerField()
    P = models.IntegerField()
    t_P = models.IntegerField()
    K = models.IntegerField()
    t_K = models.IntegerField()
    S = models.IntegerField()
    t_S = models.IntegerField()
    pH = models.FloatField()
    t_pH = models.FloatField()
    moisture = models.IntegerField()
    t_moisture = models.IntegerField()

    def __str__(self):
        return str(self.crops_name) + " (" + str(self.id) + ")"