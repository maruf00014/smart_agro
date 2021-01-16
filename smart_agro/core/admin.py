from django.contrib import admin
from .models import Farmer, Land, SoilData

admin.site.site_header = "smart_agro Admin"
admin.site.site_title = "smart_agro Admin"
admin.site.index_title = "Welcome to smart_agro"

models = (Farmer, Land, SoilData)
# Register your models here.
for model in models:
    admin.site.register(model)
