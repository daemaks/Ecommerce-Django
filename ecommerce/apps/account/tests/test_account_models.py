import pytest


def test_user_base_str(user_base):
    assert user_base.__str__() == "user_test"


def test_admin_user_base_str(admin_user_base):
    assert admin_user_base.__str__() == "admin_user"


def test_user_base_email_no_input(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(email="")
    assert str(error.value) == "You must provide an email address"


def test_user_base_email_incorrect(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(email="test.com")
    assert str(error.value) == "You must provide an valid email address"


def test_admin_user_base_email_no_input(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(
            email="", is_superuser=True, is_staff=True
        )
    assert str(error.value) == "You must provide an email address"


def test_admin_user_base_email_incorrect(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(
            email="test.com", is_superuser=True, is_staff=True
        )
    assert str(error.value) == "You must provide an valid email address"


###


def test_admin_user_base_email_not_staff(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(is_superuser=True, is_staff=False)
    assert str(error.value) == "Superuser must be assigned to is_staff=True"


def test_admin_user_base_email_not_superuser(user_base_factory):
    with pytest.raises(ValueError) as error:
        user = user_base_factory.create(is_superuser=False, is_staff=True)
    assert (
        str(error.value) == "Superuser must be assigned to is_superuser=True"
    )


def test_address_str(address):
    name = address.full_name
    assert address.__str__() == f"{name} Address"
