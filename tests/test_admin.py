import pytest

from tests.utils import randstring


def test_accounts_list(client):
    accounts = client.admin.list_accounts()
    assert len(accounts) > 0


def test_server_info(client):
    info = client.admin.server_info()
    assert 'version' in info


@pytest.mark.parametrize('password', [randstring(6)])
@pytest.mark.parametrize('name', [randstring(6)])
@pytest.mark.parametrize('email', ['{}@test.com'.format(randstring(6))])
def test_cud_account(client, email, password, Account, name):
    # create account
    test_account = client.admin.create_account(email, password)
    assert isinstance(test_account, Account)
    assert client.admin.get_account(test_account.email) == test_account

    # upadte account fields
    test_account.name = name
    test_account.is_staff = True
    test_account.is_active = True
    #test_account.update()
    assert test_account.name == name
    assert test_account in client.admin.list_accounts(start=-1, limit=-1)
    test_account.set_quota(999)
    assert test_account.get_info()['total'] == 999 * 1000000

    # delete account
    test_account.delete()
    assert test_account not in client.admin.list_accounts(start=-1, limit=-1)
