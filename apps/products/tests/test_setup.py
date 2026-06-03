from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.products.models import Product, ProductCategory
from apps.common.choices import UserRole


class TestSetUp(APITestCase):

    def setUp(self):

        self.products_url = reverse("products-list")

        self.admin = User.objects.create_user(
            username="admin",
            password="admin123",
            role=UserRole.ADMIN
        )

        self.client_user = User.objects.create_user(
            username="client",
            password="client123",
            role=UserRole.CLIENT
        )

        self.category = ProductCategory.objects.create(
            name="Fast Food"
        )

        self.product = Product.objects.create(
            name="Burger",
            price=12,
            category=self.category
        )

    def authenticate_admin(self):
        refresh = RefreshToken.for_user(self.admin)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def authenticate_client(self):
        refresh = RefreshToken.for_user(self.client_user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )