from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

import pytest

from django.test import Client
from django.core.urlresolvers import reverse

from sso.user.models import User
from sso.oauth2.tests.factories import AccessTokenFactory, ApplicationFactory


@pytest.mark.django_db
class DownloadCaseStudyCSVTestCase(TestCase):

    header = (
        'created,date_joined,email,id,is_active,is_staff,is_superuser,'
        'last_login,modified,oauth2_provider_application,utm'
    )

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email='admin@example.com', password='test'
        )
        self.client = Client()
        self.client.force_login(self.superuser)

    def test_download_csv_single_user(self):
        data = {
            'action': 'download_csv',
            '_selected_action': User.objects.all().values_list(
                'pk', flat=True
            )
        }
        response = self.client.post(
            reverse('admin:user_user_changelist'),
            data,
            follow=True
        )

        row_one = (
            "{created},{date_joined},admin@example.com,{id},True,True,True,"
            "{last_login},{modified},,{utm}"
        ).format(
            created=self.superuser.created,
            date_joined=self.superuser.date_joined,
            id=self.superuser.id,
            last_login=self.superuser.last_login,
            modified=self.superuser.modified,
            utm=self.superuser.utm,
        )
        actual = str(response.content, 'utf-8').split('\r\n')

        assert actual[0] == self.header
        assert actual[1] == row_one

    def test_download_csv_multiple_multiple_users(self):

        for x in range(2):
            User.objects.create(email=x)

        data = {
            'action': 'download_csv',
            '_selected_action': User.objects.all().values_list(
                'pk', flat=True
            )
        }
        response = self.client.post(
            reverse('admin:user_user_changelist'),
            data,
            follow=True
        )

        user_one = User.objects.all()[2]
        row_one = (
            '{created},{date_joined},{email},{id},{is_active},{is_staff},'
            '{is_superuser},,{modified},,{utm}'
        ).format(
            created=user_one.created,
            date_joined=user_one.date_joined,
            email=user_one.email,
            id=user_one.id,
            is_active=user_one.is_active,
            is_staff=user_one.is_staff,
            is_superuser=user_one.is_superuser,
            modified=user_one.modified,
            utm=user_one.utm,
        )

        user_two = User.objects.all()[1]
        row_two = (
            '{created},{date_joined},{email},{id},{is_active},{is_staff},'
            '{is_superuser},,{modified},,{utm}'
        ).format(
            created=user_two.created,
            date_joined=user_two.date_joined,
            email=user_two.email,
            id=user_two.id,
            is_active=user_two.is_active,
            is_staff=user_two.is_staff,
            is_superuser=user_two.is_superuser,
            modified=user_two.modified,
            utm=user_two.utm,
        )

        user_three = User.objects.all()[0]
        row_three = (
            '{created},{date_joined},{email},{id},{is_active},{is_staff},'
            '{is_superuser},{last_login},{modified},,{utm}'
        ).format(
            created=user_three.created,
            date_joined=user_three.date_joined,
            email=user_three.email,
            id=user_three.id,
            is_active=user_three.is_active,
            is_staff=user_three.is_staff,
            is_superuser=user_three.is_superuser,
            last_login=user_three.last_login,
            modified=user_three.modified,
            utm=user_three.utm,
        )

        actual = str(response.content, 'utf-8').split('\r\n')

        assert actual[0] == self.header
        assert actual[1] == row_one
        assert actual[2] == row_two
        assert actual[3] == row_three


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        email='admin@example.com', password='test'
    )


@pytest.fixture
def superuser_client(superuser):
    client = Client()
    client.force_login(superuser)
    return client


@pytest.mark.django_db
@patch('sso.user.admin.UserAdmin.get_fab_user_ids')
def test_download_csv_exops_not_fab(
    mock_get_fab_user_ids, settings, superuser_client
):

    settings.EXOPS_APPLICATION_CLIENT_ID = 'debug'
    application = ApplicationFactory(client_id='debug')
    user_one = AccessTokenFactory.create(
        application=application
    ).user  # should be in the csv
    user_two = AccessTokenFactory.create(
        application=application
    ).user  # should not be in the csv
    AccessTokenFactory.create().user  # should not be in the csv

    mock_get_fab_user_ids.return_value = [user_two.pk]
    data = {
        'action': 'download_csv_exops_not_fab',
        '_selected_action': User.objects.all().values_list(
            'pk', flat=True
        )
    }
    response = superuser_client.post(
        reverse('admin:user_user_changelist'),
        data,
        follow=True
    )

    expected_row = OrderedDict([
        ('created', user_one.created),
        ('date_joined', user_one.date_joined),
        ('email', user_one.email),
        ('id', user_one.id),
        ('is_active', user_one.is_active),
        ('is_staff', user_one.is_staff),
        ('is_superuser', user_one.is_superuser),
        ('last_login', user_one.last_login),
        ('modified', user_one.modified),
        ('oauth2_provider_application', ''),
        ('utm', user_one.utm),
    ])

    actual = str(response.content, 'utf-8').split('\r\n')

    assert actual[0] == ','.join(expected_row.keys())
    assert actual[1] == ','.join(map(str, expected_row.values()))


@pytest.mark.django_db
@patch('sso.user.admin.UserAdmin.get_fab_user_ids')
def test_download_csv_exops_not_fab_distinct(
    mock_get_fab_user_ids, settings, superuser_client
):

    settings.EXOPS_APPLICATION_CLIENT_ID = 'debug'
    application = ApplicationFactory(client_id='debug')
    # given a user has created multiple tokens
    token_one = AccessTokenFactory.create(
        application=application,
    )
    AccessTokenFactory.create(
        application=application,
        user=token_one.user,
    )

    mock_get_fab_user_ids.return_value = []
    data = {
        'action': 'download_csv_exops_not_fab',
        '_selected_action': User.objects.all().values_list(
            'pk', flat=True
        )
    }
    # when the export csv is created
    response = superuser_client.post(
        reverse('admin:user_user_changelist'),
        data,
        follow=True
    )

    rows = str(response.content, 'utf-8').strip().split('\r\n')
    # then the user is listed only once, not once per token created
    assert len(rows) == 2  # header and single row
