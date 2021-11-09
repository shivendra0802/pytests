from .. import forms
import pytest
pytestmark = pytest.mark.django_db


class TestPostForm:
    def test_form(self):
        form = forms.PostForm(data={})
        assert form.is_valid() is False, (
        'Should be invalid if no data is given')

        # data = {'title': 'Hello world!!!!!!!!'}
        # form = forms.PostForm(data=data)
        # assert form.is_valid() is False, (
        # 'Should be invalid if title text is less than 10 characters')
        # assert 'title' in form.errors, 'Should return field error for `title`'

        data = {'title': 'Hello World!!!!!'}
        form = forms.PostForm(data=data)
        assert form.is_valid() is True, 'Should be valid when data is given'