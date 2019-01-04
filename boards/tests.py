from django.test import TestCase
from django.urls import reverse, resolve
from .views import home
# Create your tests here.

class HomeTest(TestCase):
  def test_home_view_status_code(self):
    url = reverse('home')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

  def test_home_url_resolve_homeview(self):
    view = resolve('/')
    self.assertEquals(view.func, home)
