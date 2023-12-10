import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_user_can_create_comment(author_client, form_data, new):
    url = reverse('news:detail', args=(new.id,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.news == new
    assert new_comment.text == form_data['text']
    assert new_comment.author == form_data['author']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, new):
    start_comment = Comment.objects.count()
    url = reverse('news:detail', args=(new.id,))
    client.post(url, data=form_data)
    finish_comment = Comment.objects.count()
    assert start_comment == finish_comment

def test_author_can_edit_note(author,
                              author_client,
                              new,
                              comment,
                              form_data,
                              ):
    edit_url = reverse('news:edit', args=(comment.id,))
    url = reverse('news:detail', args=(new.id,))
    url_comments = url + '#comments'
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, url_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.news == new
    assert comment.author == author

def test_other_user_cant_edit_comment(author,
                                      admin_client,
                                      new,
                                      comment,
                                      form_data):
    comment_text = comment.text
    edit_url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(edit_url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
    assert comment.news == new
    assert comment.author == author


def test_author_can_delete_comment(author_client, comment, new):
    comment_first = Comment.objects.count()
    url_delete = reverse('news:delete', args=(comment.id,))
    url = reverse('news:detail', args=(new.id,))
    url_comments = url + '#comments'
    response = author_client.post(url_delete)
    assertRedirects(response, url_comments)
    comment_last = Comment.objects.count()
    assert comment_last == comment_first - 1

def test_other_user_cant_delete_comment(admin_client, comment):
    comment_first = Comment.objects.count()
    url_delete = reverse('news:delete', args=(comment.id,))
    response = admin_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_last = Comment.objects.count()
    assert comment_first == comment_last

def test_user_cant_use_badwords_(author_client, new):
    bad_text = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    comment_first = Comment.objects.count()
    url = reverse('news:detail', args=(new.id,))
    response = author_client.post(url, data=bad_text)
    assert response.context['form'].errors.get('text') == [WARNING]
    comment_last = Comment.objects.count()
    assert comment_first == comment_last