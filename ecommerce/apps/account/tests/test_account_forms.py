import pytest
from ecommerce.apps.account.forms import RegistrationForm, UserAddressForm


@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        (
            "test",
            "11111111111",
            "address",
            "address2",
            "city",
            "postcode",
            True,
        ),
        (
            "",
            "22222222222",
            "address3",
            "address4",
            "town",
            "postcode2",
            False,
        ),
    ],
)
def test_user_add(
    full_name,
    phone,
    address_line,
    address_line2,
    town_city,
    postcode,
    validity,
):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode,
        }
    )
    assert form.is_valid() is validity


def test_user_add_address(client, user_base):
    user = user_base
    client.force_login(user)
    response = client.post(
        "/account/add_address/",
        data={
            "full_name": "test",
            "phone": "test",
            "address_line": "test",
            "address_line2": "test",
            "town_city": "test",
            "postcode": "test",
        },
    )
    assert response.status_code == 302


@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("test_user", "test@test.com", "tester", "tester", True),
        ("test_user", "test@test.com", "tester", "tester1", False),
        ("test_user", "test@.com", "tester", "tester", False),
        # ('test_user', 'test@test.com', '', 'tester', False),
        ("test_user", "test@test.com", "tester", "", False),
    ],
)
@pytest.mark.django_db
def test_create_account(user_name, email, password, password2, validity):
    form = RegistrationForm(
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("test_user", "test@test.com", "tester", "tester", 200),
        ("test_user", "test@test.com", "tester", "tester1", 400),
        ("test_user", "", "tester", "tester", 400),
    ],
)
@pytest.mark.django_db
def test_create_account_view(
    client, user_name, email, password, password2, validity
):
    response = client.post(
        "/account/register/",
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert response.status_code == validity


def test_user_register_redirect(client, user_base):
    user = user_base
    client.force_login(user)
    response = client.get("/account/register/")
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_register_render(client):
    response = client.get("/account/register/")
    assert response.status_code == 200
