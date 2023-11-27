# Импортируем класс HTTPStatus.
from http import HTTPStatus
import unittest
from django.test import TestCase
# Импортируем функцию reverse().
from django.urls import reverse

@unittest.skip
class TestRoutes(TestCase):

    def test_home_page(self):
        # Вместо прямого указания адреса 
        # получаем его при помощи функции reverse().
        url = reverse('news:home')
        response = self.client.get(url)
        # Проверяем, что код ответа равен статусу OK (он же 200).
        self.assertEqual(response.status_code, HTTPStatus.OK)