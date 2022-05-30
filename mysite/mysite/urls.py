from django.contrib import admin
#from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pricing-start/', views.pricing_start, name='pricing-start'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('pricing/delete/<str:pk>/<str:pricing_entry_id>/', views.pricing_entry_delete, name='pricing-delete'),
    path('pricing/duplicate/<str:pk>/<str:pricing_entry_id>/', views.pricing_entry_duplicate, name='pricing-duplicate'),
    path('pricing/generate-pdf/<str:pk>/', views.GeneratePDF.as_view(), name='generate-pdf'),
    path('pricing/<str:pk>/', views.pricing, name='pricing'),
    path('pricing/<str:pk>/<str:selected_shade_type>/', views.pricing, name='pricing'),
    path('pricing-history/', views.pricing_history, name='pricing-history'),
    path('pricing-history/delete/<str:pk>/', views.pricing_name_entry_delete, name='pricingName_entry_delete'),
    path('currency-exchange-rate/', views.currency_exchange_rate, name='currency-exchange-rate'),
    path('', views.login_user ),
]
