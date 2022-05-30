from django.test import TestCase, Client
from django.urls import reverse
from mysite import views, models, urls
import unittest
#import pytest
from selenium import webdriver
from django.contrib.auth.models import User
import json


class TestLogin(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_if_login_form_works(self):
        self.driver.get("https://rysiekmirek.pythonanywhere.com/login/")
        self.driver.find_element_by_id('f_username').send_keys("testuser")
        self.driver.find_element_by_id('f_password').send_keys("tstpass1122")
        self.driver.find_element_by_id('submit').click()
        self.assertIn("https://rysiekmirek.pythonanywhere.com/pricing-start/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.pricing_start_url = reverse('pricing-start')
        models.PricingName.objects.create(name = 'test_pricing', id='c959e8ca-5c12-4eb0-9085-a35a2375ea03')
        self.pricing_url = reverse('pricing', args=['c959e8ca-5c12-4eb0-9085-a35a2375ea03'])
        self.pricing_with_shade_selected_url = reverse('pricing', args=['c959e8ca-5c12-4eb0-9085-a35a2375ea03', 'Grupa_A_Vegas'])
        models.Shade.objects.create(name='Grupa_A_Vegas', id='473ad9b397fb4d74bddc6df1c7edb235', colors='Black, White')
        models.ShadeData.objects.create(width=50, height=50, price=99, shade_id='473ad9b397fb4d74bddc6df1c7edb235')
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed('login-register.html')

    def test_pricing_start_adding_new_pricing_POST(self):
        response = self.client.post(self.pricing_start_url, {
        'f_pricing_name': 'test_pricing_name',
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(models.PricingName.objects.first().name, 'test_pricing_name' )

    def test_pricing_page_GET(self):
        response = self.client.get(self.pricing_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('pricing.html')

    def test_pricing_page_with_shade_selected_dynamic_form_POST(self):
        response = self.client.get(self.pricing_with_shade_selected_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('pricing.html')

    def test_pricing_adding_entry_POST(self):
        response = self.client.post(self.pricing_with_shade_selected_url, {
        'f_window_name': 'test_window_name',
        'f_shade': 'Grupa_A_Vegas',
        'f_color': 'Black',
        'f_width': 50,
        'f_height': 50,
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(models.Pricing.objects.first().shadePrice, 99 )

    def test_pricing_adding_price_adjustment_POST(self):
        response = self.client.post(self.pricing_url, {
        'f_adjustment': 110,
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(models.PricingName.objects.first().adjustment, 110 )

    def test_pricing_adding_comment_POST(self):
        response = self.client.post(self.pricing_url, {
        'f_pricing_comment': 'test_comment',
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(models.PricingName.objects.first().comment, 'test_comment' )




