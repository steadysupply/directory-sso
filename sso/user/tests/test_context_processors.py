from unittest.mock import Mock

import pytest

from sso.user import context_processors


@pytest.fixture
def request_with_next(rf):
    request = rf.get('/', {'next': 'http://www.example.com'})
    request.user = Mock(is_authenticated=Mock(return_value=True))
    return request


@pytest.fixture
def request_without_next(rf):
    request = rf.get('/')
    request.user = Mock(is_authenticated=Mock(return_value=True))
    return request


def test_redirect_next_processor_installed(settings):
    context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
    expected = 'sso.user.context_processors.redirect_next_processor'

    assert expected in context_processors


def test_redirect_next_processor_appends_next_param(request_with_next):
    context = context_processors.redirect_next_processor(request_with_next)

    assert context['redirect_field_name'] == 'next'
    assert context['redirect_field_value'] == 'http://www.example.com'
    assert context['sso_logout_url'] == (
        '/accounts/logout/?next=http%3A%2F%2Fwww.example.com'
    )
    assert context['sso_login_url'] == (
        '/accounts/login/?next=http%3A%2F%2Fwww.example.com'
    )
    assert context['sso_reset_password_url'] == (
        '/accounts/password/reset/?next=http%3A%2F%2Fwww.example.com'
    )
    assert context['sso_register_url'] == (
        '/accounts/signup/?next=http%3A%2F%2Fwww.example.com'
    )


def test_redirect_next_processor_handles_no_next_param(
    request_without_next, settings
):
    context = context_processors.redirect_next_processor(request_without_next)

    assert context['redirect_field_name'] == 'next'
    assert context['redirect_field_value'] == settings.DEFAULT_REDIRECT_URL
    assert context['sso_logout_url'] == (
        '/accounts/logout/?'
        'next=http%3A%2F%2Fbuyer.trade.great.dev%3A8001'
    )
    assert context['sso_login_url'] == (
        '/accounts/login/?'
        'next=http%3A%2F%2Fbuyer.trade.great.dev%3A8001'
    )
    assert context['sso_reset_password_url'] == (
        '/accounts/password/reset/?'
        'next=http%3A%2F%2Fbuyer.trade.great.dev%3A8001'
    )
    assert context['sso_register_url'] == (
        '/accounts/signup/?'
        'next=http%3A%2F%2Fbuyer.trade.great.dev%3A8001'
    )
