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
     ('news:detail', pytest.lazy_fixture('get_id_new')),
     )
)
def test_home_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK