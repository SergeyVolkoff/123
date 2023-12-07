import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('news:home', None),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),
     ('news:detail', pytest.lazy_fixture('get_id_new'),)
     )
)
def test_home_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('get_id_comment')),
     ('news:delete', pytest.lazy_fixture('get_id_comment')),),
)
def test_pages_availability_for_auth_user(author_client, page, args):
    url = reverse(page, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('get_id_comment')),
     ('news:delete', pytest.lazy_fixture('get_id_comment')),),
)
@pytest.mark.django_db
def test_redirects(client, page, args):
    login_url = reverse('users:login')
    url = reverse(page, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
@pytest.mark.django_db
@pytest.mark.parametrize('page', ('news:edit', 'news:delete'))
def test_pages_availability_for_different_users(
        page, get_id_comment, admin_client
):
    url = reverse(page, args=get_id_comment)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND