from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mysite import views
#import pytest

"""
@pytest.mark.parametrize('param', [
    ('pricing-start'),
    ('login'),
    ('logout'),
    ('register'),
    ])
def test_render_urls(client, param):
    temp_url = reverse(param)
    response = client.get(temp_url)
    assert response.status_code == 200

"""
class TestUrls(SimpleTestCase):
    def test_pricing_start_resolves(self):
        url = reverse('pricing-start')
        self.assertEquals(resolve(url).func, views.pricing_start)
    def test_login_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, views.login_user)
    def test_logout_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logout_user)
    def test_register_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, views.register_user)
    def test_pricing_delete_resolves(self):
        url = reverse('pricing-delete', args=['pk', 'pricing-endtry-id'])
        self.assertEquals(resolve(url).func, views.pricing_entry_delete)
    def test_pricing_duplicate_resolves(self):
        url = reverse('pricing-duplicate', args=['pk','pricing-endtry-id'])
        self.assertEquals(resolve(url).func, views.pricing_entry_duplicate)

    def test_generate_pdf_resolves(self):
        url = reverse('generate-pdf', args=['pk'])
        self.assertEquals(resolve(url).func.view_class, views.GeneratePDF)

    def test_pricing_resolves(self):
        url = reverse('pricing', args=['pk'])
        self.assertEquals(resolve(url).func, views.pricing)
    def test_pricing_dynamic_form_resolves(self):
        url = reverse('pricing', args=['pk','selected-shade-type'])
        self.assertEquals(resolve(url).func, views.pricing)
    def test_pricing_history_delete_resolves(self):
        url = reverse('pricingName_entry_delete', args=['pk'])
        self.assertEquals(resolve(url).func, views.pricing_name_entry_delete)
    def test_pricing_history_resolves(self):
        url = reverse('pricing-history')
        self.assertEquals(resolve(url).func, views.pricing_history)
    def test_currency_exchange_rate_resolves(self):
        url = reverse('currency-exchange-rate')
        self.assertEquals(resolve(url).func, views.currency_exchange_rate)
