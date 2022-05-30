from django.contrib import admin

from .models import Shade, ShadeData, Pricing, PricingName

admin.site.register(Shade)
admin.site.register(ShadeData)
admin.site.register(Pricing)
admin.site.register(PricingName)