# Generated by Django 3.1.5 on 2021-01-16 08:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=30)),
                ('area', models.FloatField()),
                ('currentCrops', models.CharField(blank=True, default='', max_length=30)),
                ('address', models.CharField(blank=True, default='', max_length=50)),
                ('farmer', models.ManyToManyField(related_name='lands', to='core.Farmer')),
            ],
        ),
        migrations.CreateModel(
            name='SoilData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time', models.IntegerField()),
                ('N', models.IntegerField()),
                ('P', models.IntegerField()),
                ('K', models.IntegerField()),
                ('S', models.IntegerField()),
                ('pH', models.FloatField()),
                ('moisture', models.IntegerField()),
                ('land', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.land')),
            ],
        ),
    ]
