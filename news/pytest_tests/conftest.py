import pytest

from datetime import datetime, timedelta
from django.utils import timezone 
from news.models import Comment, News
from yanews import settings


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def new():
    new = News.objects.create(
        title='Заголовок',
        text='Текс',
    )
    return new


@pytest.fixture
def get_id_new(new):
    return new.id,


@pytest.fixture
def comment(new, author):
    comment = Comment.objects.create(
        news=new,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def get_id_comment(comment):
    return comment.id,


@pytest.fixture
def news_list():
    news_list = News.objects.bulk_create(
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=datetime.today()-timedelta(days=index),
                )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )
    return news_list


@pytest.fixture
def comments_list(new, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=new,
            author=author,
            text=f'Текст {index}',
        )
    comment.created = now + timedelta(days=index)
    comment.save()


@pytest.fixture
def form_data(author):
    return {
        'title': 'Новый заголовок',
        'author': author,
        'text': 'New text'
    }