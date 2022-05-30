# Generated by Django 3.2.3 on 2022-05-04 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SheetData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.sheet')),
            ],
        ),
        migrations.CreateModel(
            name='PricingName',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('adjustment', models.FloatField(default=100)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('windowName', models.CharField(max_length=200)),
                ('shadeType', models.CharField(max_length=200)),
                ('shadeColor', models.CharField(max_length=200)),
                ('shadeWidth', models.FloatField(default=0)),
                ('shadeHeight', models.FloatField(default=0)),
                ('shadePrice', models.FloatField(default=0)),
                ('shadePriceAdjusted', models.FloatField(default=0)),
                ('sessionId', models.CharField(default=0, max_length=250)),
                ('pricingName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.pricingname')),
            ],
        ),
    ]
