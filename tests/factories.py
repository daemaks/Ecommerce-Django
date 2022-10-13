import factory
from ecommerce.apps.account.models import (
    Address,
    CustomAccountManager,
    UserBase,
)
from ecommerce.apps.catalog.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)
from faker import Faker

fake = Faker()

# Catalog


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "category_test"
    slug = "category_test"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = "product_type_test"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "product_specification_test"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product_test"
    slug = "product_test"
    regular_price = 2.00
    discount_price = 1.00


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "value_test"


# Account


class UserBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserBase

    email = "test@test.com"
    name = "user_test"
    mobile = "mobile_test"
    password = "testtest"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(UserBaseFactory)
    full_name = fake.name()
    phone = fake.phone_number()
    postcode = fake.postcode()
    address_line = fake.street_address()
    address_line2 = fake.street_address()
    town_city = fake.city_suffix()
