from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from accounts.models import User


class RegisterViewTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.url = reverse('register')
		self.username = 'myuser'
		self.data = {
			'username':'myuser',
			'password1':'valid_password1',
			'password2':'valid_password1',
			'email':'example@test.com',
		}
		self.bad_data = self.data.copy()
		self.bad_data['password2'] = 'badpassword'

	def test_register_registers_valid_user(self):
		self.client.post(self.url, self.data)
		self.assertEqual(User.objects.count(),1)
		self.assertEqual(User.objects.first().username, self.username)

	def test_register_redirect_authenticated_user_after_registration(self):
		response = self.client.post(self.url, self.data, follow=True)
		self.assertRedirects(response,'/accounts/home/')

	def test_register_returns_form_for_get(self):
		response = self.client.get(self.url)
		self.assertTemplateUsed('register.html')

	def test_register_using_invalid_data(self):
		response = self.client.post(self.url, self.bad_data, follow=True)
		self.assertTemplateUsed('register.html')












