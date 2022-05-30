from django.db import models
from django.contrib.auth.models import User
import uuid



class Shade(models.Model):
    name = models.CharField(max_length=200)
    colors = models.TextField(null=True, blank=True)
    min_width = models.IntegerField(default=0)
    max_width = models.IntegerField(default=0)
    min_height = models.IntegerField(default=0)
    max_height = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                            primary_key=True, editable=False)
    def __str__(self):
        return self.name

class ShadeData(models.Model):
    shade = models.ForeignKey(Shade, on_delete=models.CASCADE)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    def __str__(self):
        return str(self.width) + "x" + str(self.height) + "-" + str(self.price)



class PricingName(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    adjustment = models.FloatField(default=100)
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField( unique=True,primary_key=True, editable=True)
    def __str__(self):
        return self.name + "-" + str(self.id)

class Pricing(models.Model):
    pricingName = models.ForeignKey(PricingName, on_delete=models.CASCADE)
    windowName = models.CharField(max_length=200)
    shadeType = models.CharField(max_length=200)
    shadeColor  = models.CharField(max_length=200)
    shadeWidth = models.FloatField(default=0)
    shadeHeight = models.FloatField(default=0)
    shadePrice = models.FloatField(default=0)
    shadePriceAdjusted = models.FloatField(default=0)
    sessionId = models.CharField(max_length=250, default=0)
    def __str__(self):
        return self.windowName + self.shadeType + self.shadeColor + str(self.shadeWidth) + "x" + str(self.shadeHeight) + "-" + str(self.shadePrice)
