import pytest

from django.urls import reverse
from yanews import settings
from news.forms import CommentForm

HOME_URL = 'news:home'


@pytest.mark.django_db
def test_news_count(news_list, client):
    url = reverse(HOME_URL)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count <= settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_comments_sorted(client, new, comments_list):
    url = reverse('news:detail', args=(new.id,))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_dates = [comment.created for comment in all_comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates

@pytest.mark.django_db
@pytest.mark.parametrize(
        'parametrized_client, form_in_context',
        (
            (pytest.lazy_fixture('client'), False),
            (pytest.lazy_fixture('admin_client'), True),
        ),
)
def test_form_for_user_on_deteil(
        new, parametrized_client, form_in_context):
    url = reverse('news:detail', args=(new.id,))
    response = parametrized_client.get(url)
    have_form = 'form' in response.context
    assert have_form == form_in_context
    if have_form:
        assert isinstance(response.context.get('form'), CommentForm)