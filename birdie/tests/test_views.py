import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.http import Http404
from .. import views
from django.core import mail
from mock import patch

pytestmark = pytest.mark.django_db



class TestAdminView:

    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.AdminView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect to login'

    def test_superuser(self):
        user = mixer.blend('auth.User', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        resp = views.AdminView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by superuser'      


class TestPostUpdateView:
    def test_get(self):
        post = mixer.blend('birdie.Post')
        print('Post',post)
        req = RequestFactory().get('/')
        print('Request', req)
        resp = views.PostUpdateView.as_view()(req, pk=post.pk)
        assert resp.status_code == 200, 'Should be callable by anyone'

    # def test_post(self):
    #     # user = mixer.blend('auth.User', first_name='Martin')
    #     post = mixer.blend('birdie.Post')
    #     data = {'title': 'New Body Text!'}
    #     req = RequestFactory().post('/', data=data)
    #     print('Request', req)
    #     # req.user = user
    #     # print('new user', req.user)
    #     resp = views.PostUpdateView.as_view()(req, pk=post.pk)
    #     print('er', resp)
    #     assert resp.status_code == 302, 'Should redirect to success view'
    #     post.refresh_from_db()
    #     assert post.title == 'New Body Text!', 'Should update the post'


    def test_security(self):
        user = mixer.blend('auth.User', first_name='Newname')
        post = mixer.blend('birdie.Post')
        req = RequestFactory().post('/', data={})
        req.user = user
        with pytest.raises(Http404):
            views.PostUpdateView.as_view()(req, pk=post.pk)


class TestPaymentView:
    @patch('birdie.views.stripe')

    def test_payment(self, mock_stripe):
        mock_stripe.Charge.return_value = {'id': '234'}
        req = RequestFactory().post('/', data={'token': '123'})
        resp = views.PaymentView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect to success_url'
        assert len(mail.outbox) == 1, 'Should send an email'








