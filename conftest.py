import pytest
from pytest_factoryboy import register

from tests.factories import (
    AddressFactory,
    CategoryFactory,
    ProductFactory,
    ProductSpecificationFactory,
    ProductSpecificationValueFactory,
    ProductTypeFactory,
    UserBaseFactory,
)

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductFactory)
register(ProductSpecificationValueFactory)
register(UserBaseFactory)
register(AddressFactory)


@pytest.fixture
def product_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()
    return product_type


@pytest.fixture
def product_specification(db, product_specification_factory):
    product_specification = product_specification_factory.create()
    return product_specification


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def product_specification_value(db, product_specification_value_factory):
    product_specification_value = product_specification_value_factory.create()
    return product_specification_value


@pytest.fixture
def user_base(db, user_base_factory):
    user = user_base_factory.create()
    return user


@pytest.fixture
def admin_user_base(db, user_base_factory):
    user = user_base_factory.create(
        name="admin_user", is_staff=True, is_superuser=True
    )
    return user


@pytest.fixture
def address(db, address_factory):
    address = address_factory.create()
    return address
