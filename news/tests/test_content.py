from datetime import datetime, timedelta

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from news.models import News


class TestHomePage(TestCase):
    # Вынесем ссылку на домашнюю страницу в атрибуты класса.
    HOME_URL = reverse('news:home')

    # @classmethod
    # def setUpTestData(cls):
    #     all_news = []
    #     for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
    #         news = News(title=f'Новость {index}', text='Просто текст.')
    #         all_news.append(news)
    #     News.objects.bulk_create(all_news)
    #     print(all_news)    or ...

    @classmethod
    def setUpTestData(cls):
        # Вычисляем текущую дату.
        today = datetime.today()
        all_news = [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                # Для каждой новости уменьшаем дату на index дней от today,
                # где index - счётчик цикла.
                date=today - timedelta(days=index)
                )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
        News.objects.bulk_create(all_news)
         
    def test_news_count(self):
        # Загружаем главную страницу.
        response = self.client.get(self.HOME_URL)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        # Определяем длину списка.
        news_count = len(object_list)
        # Проверяем, что на странице именно 10 новостей.
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE) 
    
    def test_news_order(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        # Получаем даты новостей в том порядке, как они выведены на странице.
        all_dates = [news.date for news in object_list]
        # Сортируем полученный список по убыванию.
        sorted_dates = sorted(all_dates, reverse=True)
        print("sorted_dates:",sorted_dates)
        # Проверяем, что исходный список был отсортирован правильно.
        self.assertEqual(all_dates, sorted_dates) 
